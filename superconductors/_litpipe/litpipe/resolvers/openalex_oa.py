"""OpenAlex 记录里自带的开放获取位置。抓取阶段常常已经填好了。"""

from __future__ import annotations

from ..config import Config
from ..http import Client
from ..model import Paper

API = "https://api.openalex.org/works/doi:{doi}"


def resolve(paper: Paper, cfg: Config, client: Client) -> str:
    if not paper.doi:
        return ""
    params = {"mailto": client.email} if client.email else None
    data = client.get_json(API.format(doi=paper.doi), params=params)
    if not data:
        return ""
    for key in ("best_oa_location", "primary_location"):
        loc = data.get(key) or {}
        if loc.get("pdf_url"):
            return loc["pdf_url"]
    for loc in data.get("locations") or []:
        if loc.get("is_oa") and loc.get("pdf_url"):
            return loc["pdf_url"]
    return ""
