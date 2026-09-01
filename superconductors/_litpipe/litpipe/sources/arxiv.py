"""arXiv Atom API。cond-mat 的预印本覆盖率接近满，是这条管道的主力源。"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

from ..config import Config
from ..http import Client
from ..model import Paper

API = "http://export.arxiv.org/api/query"
_VERSION = re.compile(r"v\d+$")
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
PAGE = 100


def fetch(cfg: Config, client: Client, lookback_days: int | None = None) -> list[Paper]:
    arx = cfg.profile.get("arxiv", {})
    primary = arx.get("primary_categories") or []
    if not primary:
        return []

    fetch_cfg = cfg.section("fetch")
    lookback = lookback_days if lookback_days is not None else fetch_cfg.get("lookback_days", 7)
    cap = fetch_cfg.get("max_per_source", 300)
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback)

    query = " OR ".join(f"cat:{c}" for c in primary)
    papers: list[Paper] = []
    start = 0
    while start < cap:
        params = {
            "search_query": query,
            "start": start,
            "max_results": min(PAGE, cap - start),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        resp = client.get(API, params=params)
        if resp is None or resp.status_code != 200:
            break
        try:
            root = ET.fromstring(resp.content)
        except ET.ParseError:
            break

        entries = root.findall("a:entry", NS)
        if not entries:
            break

        stop = False
        for entry in entries:
            paper = _parse(entry)
            if paper is None:
                continue
            published = _published(entry)
            if published and published < cutoff:
                stop = True
                break
            papers.append(paper)
        if stop or len(entries) < params["max_results"]:
            break
        start += len(entries)

    print(f"  [arxiv] 近 {lookback} 天取回 {len(papers)} 条")
    return papers


def _published(entry: ET.Element) -> datetime | None:
    node = entry.find("a:published", NS)
    if node is None or not node.text:
        return None
    try:
        return datetime.fromisoformat(node.text.replace("Z", "+00:00"))
    except ValueError:
        return None


def _parse(entry: ET.Element) -> Paper | None:
    def text(tag: str) -> str:
        node = entry.find(tag, NS)
        return (node.text or "").strip() if node is not None else ""

    raw_id = text("a:id")
    if not raw_id:
        return None
    # 去掉版本后缀：同一篇的 v1/v2 应该是同一条记录，不是两篇
    arxiv_id = _VERSION.sub("", raw_id.rsplit("/abs/", 1)[-1])

    published = text("a:published")
    year = int(published[:4]) if published[:4].isdigit() else None

    doi_node = entry.find("arxiv:doi", NS)
    journal_node = entry.find("arxiv:journal_ref", NS)

    return Paper(
        title=_squash(text("a:title")),
        abstract=_squash(text("a:summary")),
        authors=[
            _squash(n.text or "")
            for n in entry.findall("a:author/a:name", NS)
            if (n.text or "").strip()
        ],
        year=year,
        doi=(doi_node.text or "").strip() if doi_node is not None else "",
        arxiv_id=arxiv_id,
        journal=(journal_node.text or "").strip() if journal_node is not None else "",
        url=raw_id,
        categories=[
            c.attrib["term"] for c in entry.findall("a:category", NS) if "term" in c.attrib
        ],
        source="arxiv",
    )


def _squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
