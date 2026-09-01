"""文献收件箱：review 档的人工裁决队列。

分数落在 review 和 auto_accept 之间的文献不自动入库，在这里列成复选框等你勾。
勾完跑 `python run.py accept`，勾中的进入待同步队列。

每条末尾有个 HTML 注释 <!--key:...-->，预览模式下不显示，是回读时的锚点。
删掉它那条就认不出来了，所以别手改那部分；其他内容随便改。
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from .model import Paper

FILENAME = "文献收件箱.md"

_ENTRY = re.compile(r"^\s*-\s*\[(?P<mark>[ xX])\].*<!--key:(?P<key>[^>]+?)-->", re.M)

_ABSTRACT_CHARS = 220


def path_for(moc_dir: Path) -> Path:
    return moc_dir / FILENAME


def read_marks(path: Path) -> tuple[set[str], set[str]]:
    """返回 (勾选的 key, 未勾选的 key)。文件不存在则都为空。"""
    if not path.exists():
        return set(), set()
    text = path.read_text(encoding="utf-8")
    checked, unchecked = set(), set()
    for match in _ENTRY.finditer(text):
        key = match.group("key").strip()
        (checked if match.group("mark").lower() == "x" else unchecked).add(key)
    return checked, unchecked


def render(path: Path, papers: list[Paper], checked: set[str] | None = None) -> int:
    """重写收件箱。checked 里的 key 会保持勾选状态，不会因为重新抓取而丢。"""
    checked = checked or set()
    papers = sorted(papers, key=lambda p: p.score, reverse=True)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "---",
        "tags:",
        "  - 文献管道",
        "---",
        "",
        "# 文献收件箱",
        "",
        f"> 更新于 {datetime.now():%Y-%m-%d %H:%M}，待裁决 **{len(papers)}** 篇。",
        "> 勾选想要的，然后在 `_litpipe` 目录下跑 `python run.py accept`。",
        "> 想把没勾的一并否掉（下次不再出现），加 `--drop-unchecked`。",
        "",
        "---",
        "",
    ]

    if not papers:
        lines += ["队列是空的。跑 `python run.py fetch` 抓一轮。", ""]
    else:
        for paper in papers:
            lines += _entry(paper, paper.key in checked)

    path.write_text("\n".join(lines), encoding="utf-8")
    return len(papers)


def _entry(paper: Paper, is_checked: bool) -> list[str]:
    mark = "x" if is_checked else " "
    year = paper.year or "n.d."
    title = paper.title.replace("\n", " ").strip()

    lines = [
        f"- [{mark}] **{title}** "
        f"`{paper.score}` <!--key:{paper.key}-->",
        f"    - {_authors(paper)} · {year} · {paper.journal or paper.source}",
    ]

    hits = _hits(paper)
    if hits:
        lines.append(f"    - 命中：{hits}")

    abstract = (paper.abstract or "").strip().replace("\n", " ")
    if abstract:
        if len(abstract) > _ABSTRACT_CHARS:
            abstract = abstract[:_ABSTRACT_CHARS] + "…"
        lines.append(f"    - {abstract}")

    link = _link(paper)
    if link:
        lines.append(f"    - {link}")
    lines.append("")
    return lines


def _authors(paper: Paper) -> str:
    authors = [a for a in (paper.authors or []) if a.strip()]
    if not authors:
        return "作者未知"
    if len(authors) <= 3:
        return ", ".join(authors)
    return f"{authors[0]} 等 {len(authors)} 人"


def _hits(paper: Paper) -> str:
    terms: list[str] = []
    for group, info in (paper.score_detail or {}).items():
        if not isinstance(info, dict):
            continue
        for term in list(info.get("title") or []) + list(info.get("abstract") or []):
            if term not in terms:
                terms.append(term)
    return "、".join(f"`{t}`" for t in terms[:8])


def _link(paper: Paper) -> str:
    if paper.arxiv_id:
        return f"[arXiv:{paper.arxiv_id}](https://arxiv.org/abs/{paper.arxiv_id})"
    if paper.doi:
        return f"[doi:{paper.doi}](https://doi.org/{paper.doi})"
    return f"[原文]({paper.url})" if paper.url else ""
