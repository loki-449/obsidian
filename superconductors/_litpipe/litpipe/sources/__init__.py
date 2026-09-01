"""文献来源。每个模块暴露 fetch(cfg, client, **kw) -> list[Paper]。"""

from . import arxiv, openalex

REGISTRY = {
    "arxiv": arxiv.fetch,
    "openalex": openalex.fetch,
}

__all__ = ["REGISTRY", "arxiv", "openalex"]
