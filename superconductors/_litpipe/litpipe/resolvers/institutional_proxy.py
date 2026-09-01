"""机构订阅代理（EZproxy 之类）。默认关闭，需要在 settings.yaml 里配。

物理所 / 中科院文献情报中心对 PRB、PRL、Nature 系、Science 系的订阅覆盖很全，
这条链路拿到的是正刊排版版本，而且完全合规。
"""

from __future__ import annotations

import re

from ..config import Config
from ..http import Client
from ..model import Paper

_PDF_LINK = re.compile(
    r'<(?:a|meta)[^>]+(?:href|content)=["\']([^"\']+\.pdf[^"\']*)["\']', re.IGNORECASE
)
_CITATION_PDF = re.compile(
    r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)


def resolve(paper: Paper, cfg: Config, client: Client) -> str:
    conf = cfg.section("resolve").get("institutional_proxy") or {}
    if not conf.get("enabled") or not conf.get("url_template") or not paper.doi:
        return ""

    landing = conf["url_template"].format(doi=paper.doi)
    headers = {}
    if conf.get("cookie"):
        headers["Cookie"] = conf["cookie"]

    resp = client.get(landing, headers=headers)
    if resp is None or resp.status_code != 200:
        return ""

    if "pdf" in resp.headers.get("Content-Type", "").lower():
        return resp.url

    html = resp.text
    match = _CITATION_PDF.search(html) or _PDF_LINK.search(html)
    if not match:
        return ""
    return _absolutize(match.group(1), resp.url)


def _absolutize(href: str, base: str) -> str:
    from urllib.parse import urljoin

    return urljoin(base, href)
