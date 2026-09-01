"""PDF 解析链。按 settings.yaml 的 resolve.chain 顺序尝试，第一个拿到就停。

每个 resolver 是一个函数：(paper, cfg, client) -> str | ""，返回可直接下载的 PDF URL。
要加自己的 resolver，见本目录 README.md。
"""

from __future__ import annotations

from typing import Callable

from ..config import Config
from ..http import Client
from ..model import Paper
from . import arxiv, institutional_proxy, openalex_oa, unpaywall

Resolver = Callable[[Paper, Config, Client], str]

BUILTIN: dict[str, Resolver] = {
    "arxiv": arxiv.resolve,
    "unpaywall": unpaywall.resolve,
    "openalex_oa": openalex_oa.resolve,
    "institutional_proxy": institutional_proxy.resolve,
}

_EXTRA: dict[str, Resolver] = {}


def register(name: str, fn: Resolver) -> None:
    """注册自定义 resolver。"""
    _EXTRA[name] = fn


def resolve(paper: Paper, cfg: Config, client: Client) -> Paper:
    if paper.pdf_url:
        return paper
    chain = cfg.section("resolve").get("chain") or []
    for name in chain:
        fn = _EXTRA.get(name) or BUILTIN.get(name)
        if fn is None:
            print(f"  [resolve] 未知 resolver: {name}（已跳过）")
            continue
        try:
            url = fn(paper, cfg, client)
        except Exception as exc:                      # resolver 各自为政，别互相拖累
            print(f"  [resolve] {name} 出错: {exc}")
            continue
        if url:
            paper.pdf_url = url
            paper.pdf_via = name
            return paper
    return paper
