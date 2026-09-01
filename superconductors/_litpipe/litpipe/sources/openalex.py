"""OpenAlex works API。补正刊文献 + 提供开放获取链接。"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from ..config import Config
from ..http import Client
from ..model import Paper, strip_markup

API = "https://api.openalex.org/works"
PAGE = 100


def fetch(cfg: Config, client: Client, lookback_days: int | None = None) -> list[Paper]:
    oa = cfg.profile.get("openalex", {})
    fetch_cfg = cfg.section("fetch")
    lookback = lookback_days if lookback_days is not None else fetch_cfg.get("lookback_days", 7)
    cap = fetch_cfg.get("max_per_source", 300)
    since = (datetime.now(timezone.utc) - timedelta(days=lookback)).date().isoformat()

    # 用 core + adjacent 关键词做检索式，避免把整个 cond-mat 拉下来
    terms = _search_terms(cfg)
    if not terms:
        return []

    filters = [f"from_publication_date:{since}", "type:article"]
    concepts = oa.get("concepts") or []
    if concepts:
        filters.append("concepts.id:" + "|".join(concepts))

    papers: list[Paper] = []
    cursor = "*"
    while len(papers) < cap and cursor:
        params = {
            "filter": ",".join(filters),
            "search": " OR ".join(f'"{t}"' for t in terms),
            "per-page": min(PAGE, cap - len(papers)),
            "cursor": cursor,
        }
        email = client.email
        if email:
            params["mailto"] = email

        data = client.get_json(API, params=params)
        if not data:
            break
        results = data.get("results") or []
        for item in results:
            paper = _parse(item)
            if paper:
                papers.append(paper)
        cursor = (data.get("meta") or {}).get("next_cursor")
        if not results:
            break

    print(f"  [openalex] 近 {lookback} 天取回 {len(papers)} 条")
    return papers


def _search_terms(cfg: Config, cap: int = 24) -> list[str]:
    """检索式长度有上限，core 和 adjacent 交替取，别让长的那组把另一组挤没。"""
    kw = cfg.profile.get("keywords", {})
    groups = [list(kw.get(g, {}).get("terms") or []) for g in ("core", "adjacent")]
    terms: list[str] = []
    for i in range(max((len(g) for g in groups), default=0)):
        for group in groups:
            if i < len(group) and len(terms) < cap:
                terms.append(group[i])
    return terms


def _parse(item: dict) -> Paper | None:
    title = strip_markup(item.get("title") or "")
    if not title:
        return None

    doi = (item.get("doi") or "").replace("https://doi.org/", "")
    host = (item.get("primary_location") or {}).get("source") or {}

    best_oa = item.get("best_oa_location") or {}
    pdf_url = best_oa.get("pdf_url") or ""

    return Paper(
        title=title,
        abstract=strip_markup(_inverted_to_text(item.get("abstract_inverted_index"))),
        authors=[
            (a.get("author") or {}).get("display_name", "")
            for a in (item.get("authorships") or [])
            if (a.get("author") or {}).get("display_name")
        ],
        year=item.get("publication_year"),
        doi=doi,
        journal=host.get("display_name") or "",
        url=item.get("id") or "",
        categories=[
            c.get("display_name", "") for c in (item.get("concepts") or [])[:5]
        ],
        source="openalex",
        pdf_url=pdf_url,
        pdf_via="openalex_oa" if pdf_url else "",
    )


def _inverted_to_text(index: dict | None) -> str:
    """OpenAlex 出于版权原因只给倒排索引，还原成正文。"""
    if not index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, spots in index.items():
        positions.extend((spot, word) for spot in spots)
    positions.sort()
    return " ".join(word for _, word in positions)
