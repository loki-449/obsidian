"""用 LLM 给文献打正交标签。走 OpenAI 兼容的 chat completions 接口。

只读标题和摘要，不读全文 —— 这是刻意的：全文成本高，而 role/system/method
这三个轴从摘要就能判得八九不离十，拿不准的本来也该你自己读。

模型返回的值会拿 taxonomy.yaml 的 values 校验：
  - 闭合轴（role、stage）越界的值直接丢弃，不硬塞
  - 开放轴（system、method）允许新值，只做去空白和长度检查
校验失败不影响其他轴，也不影响其他文献 —— 一批里坏一条不该拖垮整批。
"""

from __future__ import annotations

import json
import os
import re
import time
from typing import Any

import requests

from .config import Config
from .model import Paper

# 让模型填的轴。stage 不给模型碰（新抓的一律"未读"）。
TAGGED_AXES = ("role", "system", "method")

_MAX_OPEN_VALUE_LEN = 24


class TaggerUnavailable(RuntimeError):
    """配置缺失或 key 没设。调用方据此决定是跳过打标签还是中止。"""


# ============================================================ 对外入口
def tag_papers(papers: list[Paper], cfg: Config, verbose: bool = True) -> int:
    """就地给 papers 填 tags。返回成功打上标签的篇数。"""
    conf = _check(cfg)
    if not papers:
        return 0

    batch_size = int(conf.get("batch_size", 8) or 8)
    system_prompt = _system_prompt(cfg)
    tagged = 0

    for start in range(0, len(papers), batch_size):
        batch = papers[start : start + batch_size]
        try:
            raw = _call(system_prompt, _user_prompt(batch, conf), conf)
        except Exception as exc:
            print(f"  [tagger] 第 {start // batch_size + 1} 批失败，跳过: {exc}")
            continue

        results = _extract_results(raw)
        if not results:
            print(f"  [tagger] 第 {start // batch_size + 1} 批返回无法解析，跳过")
            continue

        for entry in results:
            idx = _as_index(entry.get("id"), len(batch))
            if idx is None:
                continue
            if _apply(batch[idx], entry, cfg):
                tagged += 1

        if verbose:
            print(f"  [tagger] {min(start + batch_size, len(papers))}/{len(papers)}")

    return tagged


def available(cfg: Config) -> bool:
    try:
        _check(cfg)
    except TaggerUnavailable:
        return False
    return True


def _check(cfg: Config) -> dict[str, Any]:
    conf = cfg.section("tagger")
    if not conf.get("enabled", True):
        raise TaggerUnavailable("tagger.enabled = false")
    if not conf.get("base_url") or not conf.get("model"):
        raise TaggerUnavailable("settings.yaml 的 tagger.base_url / model 没填")
    env_name = conf.get("api_key_env") or "DEEPSEEK_API_KEY"
    if not os.environ.get(env_name):
        raise TaggerUnavailable(
            f"环境变量 {env_name} 没设。PowerShell 里临时设置："
            f'$env:{env_name}="sk-..."；要长期生效用 '
            f'[Environment]::SetEnvironmentVariable("{env_name}","sk-...","User")'
        )
    return conf


# ============================================================ 提示词
def _system_prompt(cfg: Config) -> str:
    axes = cfg.taxonomy.get("axes", {})
    hint = (cfg.taxonomy.get("tagger_hint") or "").strip()

    lines = [hint, "", "为每篇文献判断以下几个轴："]
    for name in TAGGED_AXES:
        spec = axes.get(name) or {}
        values = spec.get("values") or []
        multi = "可多选" if spec.get("multi") else "单选"
        openness = "允许使用列表外的新值" if spec.get("open") else "只能从列表里选"
        lines.append(f"- {name}（{multi}，{openness}）：{' / '.join(values)}")

    rel = axes.get("relevance") or {}
    lo, hi = (rel.get("range") or [1, 5])[:2]
    lines.append(f"- relevance（整数 {lo}-{hi}）：与她课题的相关度")

    lines += [
        "",
        "输出严格的 JSON，形如：",
        '{"results":[{"id":1,"role":["方法"],"system":["镍氧化物"],'
        '"method":["DMFT"],"relevance":4}]}',
        "id 必须对应输入里的编号。拿不准的轴给空数组，不要硬填。",
        "只输出 JSON，不要任何解释文字。",
    ]
    return "\n".join(lines)


def _user_prompt(batch: list[Paper], conf: dict[str, Any]) -> str:
    limit = int(conf.get("max_abstract_chars", 1800) or 1800)
    blocks = []
    for i, paper in enumerate(batch, 1):
        abstract = (paper.abstract or "").strip()
        if len(abstract) > limit:
            abstract = abstract[:limit] + " ..."
        blocks.append(
            f"[{i}] 标题：{paper.title}\n"
            f"    摘要：{abstract or '（无摘要）'}"
        )
    return "\n\n".join(blocks)


# ============================================================ 调用
def _call(system_prompt: str, user_prompt: str, conf: dict[str, Any]) -> str:
    base = str(conf["base_url"]).rstrip("/")
    url = f"{base}/chat/completions" if not base.endswith("/chat/completions") else base
    key = os.environ[conf.get("api_key_env") or "DEEPSEEK_API_KEY"]

    payload = {
        "model": conf["model"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0,
        "max_tokens": int(conf.get("max_tokens", 2048) or 2048),
        "response_format": {"type": "json_object"},
    }

    last: Exception | None = None
    for attempt in range(3):
        try:
            resp = requests.post(
                url,
                json=payload,
                headers={"Authorization": f"Bearer {key}"},
                timeout=180,
            )
        except requests.RequestException as exc:
            last = exc
        else:
            if resp.status_code == 200:
                msg = resp.json()["choices"][0]["message"]
                content = (msg.get("content") or "").strip()
                if content:
                    return content
                # 推理模型有时只把结果写进 reasoning_content
                reasoning = (msg.get("reasoning_content") or msg.get("reasoning") or "").strip()
                if reasoning:
                    return reasoning
                last = RuntimeError("模型返回空 content")
            # 400 多半是 response_format 不被支持，退化成纯提示词约束再试一次
            elif resp.status_code == 400 and "response_format" in payload:
                payload.pop("response_format")
                continue
            else:
                last = RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        time.sleep(2**attempt)
    raise RuntimeError(str(last))


_JSON_BLOCK = re.compile(r"\{.*\}", re.DOTALL)


def _extract_results(raw: str) -> list[dict[str, Any]]:
    """模型偶尔会包一层 ```json 或加寒暄，兜住这些情况。"""
    text = (raw or "").strip()
    data: Any = None
    try:
        data = json.loads(text)
    except ValueError:
        match = _JSON_BLOCK.search(text)
        if match:
            try:
                data = json.loads(match.group(0))
            except ValueError:
                return []
    if isinstance(data, list):
        return [d for d in data if isinstance(d, dict)]
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                return [d for d in value if isinstance(d, dict)]
    return []


def _as_index(raw_id: Any, size: int) -> int | None:
    try:
        idx = int(raw_id) - 1
    except (TypeError, ValueError):
        return None
    return idx if 0 <= idx < size else None


# ============================================================ 校验
def _apply(paper: Paper, entry: dict[str, Any], cfg: Config) -> bool:
    axes = cfg.taxonomy.get("axes", {})
    touched = False

    for name in TAGGED_AXES:
        spec = axes.get(name) or {}
        values = _clean_axis(entry.get(name), spec)
        if values:
            paper.tags[name] = values if spec.get("multi") else values[0]
            touched = True

    relevance = _clean_relevance(entry.get("relevance"), axes.get("relevance") or {})
    if relevance is not None:
        paper.tags["relevance"] = relevance
        touched = True

    paper.tags.setdefault("stage", "未读")
    return touched


def _clean_axis(raw: Any, spec: dict[str, Any]) -> list[str]:
    if raw is None:
        return []
    items = raw if isinstance(raw, list) else [raw]
    allowed = {str(v).strip(): str(v).strip() for v in (spec.get("values") or [])}
    lowered = {k.lower(): v for k, v in allowed.items()}
    is_open = bool(spec.get("open"))

    out: list[str] = []
    for item in items:
        value = str(item).strip()
        if not value:
            continue
        canonical = lowered.get(value.lower())
        if canonical:
            value = canonical
        elif not is_open:
            continue                       # 闭合轴越界，丢掉而不是硬塞
        elif len(value) > _MAX_OPEN_VALUE_LEN:
            continue                       # 开放轴也别让模型塞一整句进来
        if value not in out:
            out.append(value)
    return out


def _clean_relevance(raw: Any, spec: dict[str, Any]) -> int | None:
    if raw is None or isinstance(raw, bool):
        return None
    try:
        value = int(float(raw))
    except (TypeError, ValueError):
        return None
    lo, hi = (spec.get("range") or [1, 5])[:2]
    return value if int(lo) <= value <= int(hi) else None
