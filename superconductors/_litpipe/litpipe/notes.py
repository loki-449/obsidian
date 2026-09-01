"""生成 Obsidian 文献卡片。扁平结构：一篇文章 = 一个 {citekey}.md。

两条铁律：
  1. 绝不覆盖已存在的卡片 —— 里面可能有你手写的笔记。同名不同文时自动加后缀。
  2. frontmatter 用 yaml.safe_dump 生成 —— 标题里的冒号引号会把手拼的 YAML 搞坏。

正文小节沿用 Templates/literature-note-template.md 的结构，手动建卡和管道建卡
长得一样，Dataview 查询不用分两套。
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from .model import Paper

_ILLEGAL = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

# 作者太多的话卡片头会很难看，正刊大合作组动辄上百人
_MAX_AUTHORS = 8

SECTIONS = (
    "🔬 研究问题",
    "⚙️ 主要方法",
    "📊 关键结果",
    "💡 核心结论",
    "🔗 与我研究的关联",
    "❓ 问题与待深入理解",
)


def write_card(paper: Paper, notes_dir: Path, zotero_key: str = "") -> Path | None:
    """写一张卡片。已存在同一篇的卡片则返回 None（不动它）。"""
    notes_dir.mkdir(parents=True, exist_ok=True)
    path = _resolve_path(paper, notes_dir)
    if path is None:
        return None
    path.write_text(_render(paper, zotero_key), encoding="utf-8")
    return path


def _resolve_path(paper: Paper, notes_dir: Path) -> Path | None:
    """定位可写的文件名。同名且是同一篇 -> None；同名但是别的文章 -> 加后缀。"""
    stem = _ILLEGAL.sub("-", paper.citekey()).strip() or "unknown"
    candidate = notes_dir / f"{stem}.md"
    suffix = 0
    while candidate.exists():
        if _is_same_paper(candidate, paper):
            return None
        suffix += 1
        candidate = notes_dir / f"{stem}{chr(ord('a') + suffix - 1)}.md"
        if suffix > 25:
            return None
    return candidate


def _is_same_paper(path: Path, paper: Paper) -> bool:
    """靠 frontmatter 的 doi / arxiv 判同一篇，判不出就当作不同，宁可多建也不覆盖。"""
    meta = read_frontmatter(path)
    if not meta:
        return False
    if paper.doi and str(meta.get("doi", "")).lower() == paper.doi.lower():
        return True
    if paper.arxiv_id and str(meta.get("arxiv", "")).lower() == paper.arxiv_id.lower():
        return True
    return False


def read_frontmatter(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


# ============================================================ 渲染
def _render(paper: Paper, zotero_key: str) -> str:
    body = [
        _frontmatter(paper, zotero_key),
        f"# {paper.title}",
        "",
        _header_block(paper, zotero_key),
        "",
        "## 摘要",
        "",
        paper.abstract.strip() or "（源站未提供摘要）",
        "",
    ]
    for section in SECTIONS:
        body += [f"## {section}", "", ""]
    body += ["---", "", _provenance(paper), ""]
    return "\n".join(body)


def _frontmatter(paper: Paper, zotero_key: str) -> str:
    tags = paper.tags or {}
    meta: dict[str, Any] = {
        "title": paper.title,
        "authors": _authors(paper),
        "year": paper.year or "",
        "journal": paper.journal,
        "doi": paper.doi,
        "arxiv": paper.arxiv_id,
        "citekey": paper.citekey(),
        "zotero": f"zotero://select/library/items/{zotero_key}" if zotero_key else "",
        "url": paper.url,
        "source": paper.source,
        # -- 正交轴，Dataview 靠这几个字段做交叉筛选
        "role": _as_list(tags.get("role")),
        "system": _as_list(tags.get("system")),
        "method": _as_list(tags.get("method")),
        "stage": tags.get("stage") or "未读",
        "relevance": tags.get("relevance") or 1,
        "score": paper.score,
        "added": date.today().isoformat(),
        "tags": ["文献"],
    }
    dumped = yaml.safe_dump(
        meta, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000
    )
    return f"---\n{dumped}---\n"


def _header_block(paper: Paper, zotero_key: str) -> str:
    lines = ["> [!info] 基本信息"]
    authors = _authors(paper)
    if authors:
        shown = ", ".join(authors[:_MAX_AUTHORS])
        if len(authors) > _MAX_AUTHORS:
            shown += f" 等 {len(authors)} 人"
        lines.append(f"> - 作者：{shown}")
    if paper.journal:
        lines.append(f"> - 期刊：{paper.journal}")
    if paper.year:
        lines.append(f"> - 年份：{paper.year}")
    if paper.doi:
        lines.append(f"> - DOI：[{paper.doi}](https://doi.org/{paper.doi})")
    if paper.arxiv_id:
        lines.append(
            f"> - arXiv：[{paper.arxiv_id}](https://arxiv.org/abs/{paper.arxiv_id})"
        )
    if zotero_key:
        lines.append(
            f"> - [在 Zotero 中打开](zotero://select/library/items/{zotero_key})"
            "（全文用 Zotero 的 Find Available PDF 抓）"
        )
    else:
        lines.append("> - 尚未入 Zotero")
    return "\n".join(lines)


def _provenance(paper: Paper) -> str:
    lines = [
        "> [!abstract]- 抓取信息",
        f"> 来源 `{paper.source}`，打分 **{paper.score}**，判定 `{paper.verdict}`。",
    ]
    detail = paper.score_detail or {}
    if "excluded_by" in detail:
        lines.append(f"> 被排除词命中：`{detail['excluded_by']}`")
    else:
        for group, info in detail.items():
            if not isinstance(info, dict):
                continue
            hits = list(info.get("title") or []) + list(info.get("abstract") or [])
            if hits:
                terms = "、".join(f"`{h}`" for h in hits)
                lines.append(f"> - {group} +{info.get('score', 0)}：{terms}")
    if paper.categories:
        lines.append(f"> - 分类：{', '.join(paper.categories[:6])}")
    return "\n".join(lines)


def _authors(paper: Paper) -> list[str]:
    return [a.strip() for a in (paper.authors or []) if a and a.strip()]


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    return [text] if text else []
