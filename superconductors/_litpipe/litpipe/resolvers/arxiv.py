"""arXiv 全文。cond-mat 方向命中率最高的一条，优先级放第一。"""

from __future__ import annotations

import re

from ..config import Config
from ..http import Client
from ..model import Paper

ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5}(?:v\d+)?|[a-z\-]+/\d{7})", re.IGNORECASE)


def resolve(paper: Paper, cfg: Config, client: Client) -> str:
    ident = paper.arxiv_id
    if not ident and paper.url and "arxiv.org" in paper.url:
        match = ARXIV_ID.search(paper.url)
        ident = match.group(1) if match else ""
    if not ident and paper.doi.lower().startswith("10.48550/arxiv."):
        ident = paper.doi.split(".", 2)[-1]
    if not ident:
        ident = _lookup_by_title(paper, client)
    return f"https://arxiv.org/pdf/{ident}" if ident else ""


def _lookup_by_title(paper: Paper, client: Client) -> str:
    """正刊文献常有对应预印本，用标题反查一次。"""
    if not paper.title:
        return ""
    import xml.etree.ElementTree as ET

    escaped = paper.title.replace('"', "")
    resp = client.get(
        "http://export.arxiv.org/api/query",
        params={"search_query": f'ti:"{escaped}"', "max_results": 1},
    )
    if resp is None or resp.status_code != 200:
        return ""
    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError:
        return ""
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entry = root.find("a:entry", ns)
    if entry is None:
        return ""
    found_title = (entry.findtext("a:title", "", ns) or "").strip().lower()
    # 标题反查容易串到近似论文，要求高度吻合才认
    if _normalize(found_title) != _normalize(paper.title):
        return ""
    raw_id = entry.findtext("a:id", "", ns) or ""
    return raw_id.rsplit("/abs/", 1)[-1] if "/abs/" in raw_id else ""


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())
