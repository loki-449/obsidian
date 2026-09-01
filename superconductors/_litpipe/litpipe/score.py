"""关键词打分。field_profile.yaml 里的规则在这里被执行。

打分逻辑刻意保持透明：每篇文献都记下命中了哪些词、各得多少分，
写进卡片的 score_detail 里。看到误判时你能直接定位到是哪条关键词的问题。
"""

from __future__ import annotations

import re
from functools import lru_cache

from .config import Config
from .model import Paper

ACCEPT, REVIEW, REJECT = "accept", "review", "reject"


@lru_cache(maxsize=2048)
def _pattern(term: str) -> re.Pattern[str]:
    """词边界匹配，允许词内连字符/空格互换（electron-phonon ≈ electron phonon）。"""
    parts = [re.escape(p) for p in re.split(r"[\s\-]+", term.strip()) if p]
    body = r"[\s\-]+".join(parts)
    return re.compile(rf"(?<![A-Za-z0-9]){body}", re.IGNORECASE)


def score_paper(paper: Paper, cfg: Config) -> Paper:
    profile = cfg.profile
    keywords = profile.get("keywords", {})
    title_boost = float(profile.get("title_boost", 2.0))
    title = paper.title or ""
    abstract = paper.abstract or ""

    exclude_terms = (keywords.get("exclude") or {}).get("terms") or []
    for term in exclude_terms:
        if _pattern(term).search(title) or _pattern(term).search(abstract):
            paper.score = 0.0
            paper.score_detail = {"excluded_by": term}
            paper.verdict = REJECT
            return paper

    total = 0.0
    detail: dict[str, object] = {}
    for group, spec in keywords.items():
        if group == "exclude":
            continue
        weight = float(spec.get("weight", 1.0))
        hits_title: list[str] = []
        hits_abstract: list[str] = []
        for term in spec.get("terms") or []:
            pat = _pattern(term)
            if pat.search(title):
                hits_title.append(term)
            elif pat.search(abstract):
                hits_abstract.append(term)
        if not hits_title and not hits_abstract:
            continue
        # 同组内只按"命中与否"计分一次，标题命中吃 boost。
        # 否则堆同义词的组会无脑碾压别的组。
        group_score = weight * (title_boost if hits_title else 1.0)
        total += group_score
        detail[group] = {
            "score": round(group_score, 2),
            "title": hits_title,
            "abstract": hits_abstract,
        }

    total += _category_bonus(paper, cfg)

    paper.score = round(total, 2)
    paper.score_detail = detail
    auto_accept, review = cfg.thresholds
    paper.verdict = ACCEPT if total >= auto_accept else REVIEW if total >= review else REJECT
    if not paper.tags.get("relevance"):
        paper.tags["relevance"] = _to_relevance(total, auto_accept, review)
    return paper


def _category_bonus(paper: Paper, cfg: Config) -> float:
    arx = cfg.profile.get("arxiv", {})
    primary = set(arx.get("primary_categories") or [])
    secondary = set(arx.get("secondary_categories") or [])
    cats = set(paper.categories)
    if cats & primary:
        return 1.0
    if cats & secondary:
        return 0.3
    return 0.0


def _to_relevance(score: float, auto_accept: float, review: float) -> int:
    """把连续分数压到 1-5，作为 relevance 的初值。"""
    if score >= auto_accept * 1.5:
        return 5
    if score >= auto_accept:
        return 4
    if score >= review:
        return 3
    if score > 0:
        return 2
    return 1


def score_all(papers: list[Paper], cfg: Config) -> dict[str, list[Paper]]:
    buckets: dict[str, list[Paper]] = {ACCEPT: [], REVIEW: [], REJECT: []}
    for paper in papers:
        buckets[score_paper(paper, cfg).verdict].append(paper)
    for bucket in buckets.values():
        bucket.sort(key=lambda p: p.score, reverse=True)
    return buckets
