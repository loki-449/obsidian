"""Unpaywall：按 DOI 查合法开放获取版本。需要在 settings 里填 contact_email。"""

from __future__ import annotations

from ..config import Config
from ..http import Client
from ..model import Paper

API = "https://api.unpaywall.org/v2/{doi}"


def resolve(paper: Paper, cfg: Config, client: Client) -> str:
    if not paper.doi or not client.email:
        return ""
    data = client.get_json(API.format(doi=paper.doi), params={"email": client.email})
    if not data:
        return ""
    best = data.get("best_oa_location") or {}
    url = best.get("url_for_pdf") or ""
    if url:
        return url
    for loc in data.get("oa_locations") or []:
        if loc.get("url_for_pdf"):
            return loc["url_for_pdf"]
    return ""
