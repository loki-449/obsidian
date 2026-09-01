"""领域收敛：从导师 / 课题组论文里反推该往 field_profile 加哪些关键词。

做法是 n-gram 词频 + 通用词惩罚，不做 embedding。输出是"建议"而不是自动改配置 ——
关键词体系是这套系统的地基，值得你亲自过一遍眼。
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from .config import Config
from .http import Client
from .model import Paper, strip_markup

OPENALEX_WORKS = "https://api.openalex.org/works"
OPENALEX_AUTHORS = "https://api.openalex.org/authors"

# 物理摘要里到处都是、区分度为零的词
_GENERIC = {
    "we", "the", "of", "in", "a", "an", "and", "or", "to", "with", "for", "on",
    "is", "are", "be", "been", "that", "this", "these", "those", "which", "as",
    "by", "from", "at", "it", "its", "our", "can", "may", "also", "such", "here",
    "show", "shows", "shown", "study", "studies", "studied", "results", "result",
    "using", "used", "use", "based", "present", "presented", "report", "reported",
    "find", "found", "observe", "observed", "suggest", "suggests", "however",
    "further", "recent", "recently", "new", "novel", "well", "both", "between",
    "system", "systems", "material", "materials", "properties", "property",
    "state", "states", "effect", "effects", "model", "models", "method", "methods",
    "phase", "phases", "high", "low", "large", "small", "first", "two", "one",
    "not", "no", "than", "more", "most", "much", "have", "has", "was", "were",
    "paper", "work", "provide", "provides", "demonstrate", "demonstrated",
}

# 这些词单独出现毫无区分度（凝聚态摘要里人人都写），但作为词组的一部分很有用
# （fermi 没用，fermi surface 有用）。所以只在 n=1 时拦，不影响 n-gram。
_WEAK_ALONE = {
    "temperature", "temperatures", "quantum", "transition", "transitions",
    "magnetic", "magnetism", "electron", "electrons", "electronic",
    "superconductivity", "superconducting", "superconductor", "superconductors",
    "calculation", "calculations", "critical", "behavior", "behaviour",
    "structure", "structures", "structural", "fermi", "field", "fields",
    "order", "ordering", "energy", "energies", "spin", "spins", "band", "bands",
    "density", "theory", "theoretical", "experiment", "experiments",
    "experimental", "observation", "observations", "measurement", "measurements",
    "data", "physics", "physical", "coupling", "interaction", "interactions",
    "phenomena", "phenomenon", "mechanism", "mechanisms", "evidence",
    "temperature-dependent", "pressure", "doping", "doped", "crystal", "crystals",
    "lattice", "surface", "surfaces", "layer", "layers", "compound", "compounds",
}

_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9\-]+")


def collect(cfg: Config, client: Client) -> list[Paper]:
    """把 seeds 配置里的导师和论文都拉成 Paper 列表。"""
    seeds = cfg.profile.get("seeds") or {}
    papers: list[Paper] = []

    for advisor in seeds.get("advisors") or []:
        author_id = advisor.get("openalex_id") or _resolve_author(
            client, advisor.get("orcid"), advisor.get("name")
        )
        if not author_id:
            print(f"  [seeds] 未能定位作者：{advisor.get('name')}")
            continue
        papers.extend(_author_works(client, author_id))

    for ref in seeds.get("papers") or []:
        paper = _single_work(client, str(ref))
        if paper:
            papers.append(paper)

    return papers


def _resolve_author(client: Client, orcid: str | None, name: str | None) -> str:
    if orcid:
        data = client.get_json(f"{OPENALEX_AUTHORS}/orcid:{orcid}")
        if data and data.get("id"):
            return data["id"].rsplit("/", 1)[-1]
    if name:
        data = client.get_json(OPENALEX_AUTHORS, params={"search": name, "per-page": 1})
        results = (data or {}).get("results") or []
        if results:
            return results[0]["id"].rsplit("/", 1)[-1]
    return ""


def _author_works(client: Client, author_id: str, limit: int = 200) -> list[Paper]:
    from .sources.openalex import _parse

    data = client.get_json(
        OPENALEX_WORKS,
        params={"filter": f"author.id:{author_id}", "per-page": min(limit, 200)},
    )
    out = []
    for item in (data or {}).get("results") or []:
        paper = _parse(item)
        if paper:
            out.append(paper)
    return out


def _single_work(client: Client, ref: str) -> Paper | None:
    from .sources.openalex import _parse

    ref = ref.strip()
    if ref.lower().startswith("arxiv:"):
        ident = f"https://arxiv.org/abs/{ref.split(':', 1)[1]}"
        data = client.get_json(OPENALEX_WORKS, params={"filter": f"ids.openalex:{ident}"})
        results = (data or {}).get("results") or []
        return _parse(results[0]) if results else None
    data = client.get_json(f"{OPENALEX_WORKS}/doi:{ref}")
    return _parse(data) if data else None


def suggest_terms(papers: list[Paper], cfg: Config, top: int = 40) -> list[tuple[str, int]]:
    """从种子论文的标题+摘要里抽 1-3 gram，排掉已在配置里的和通用词。"""
    existing = _existing_terms(cfg)
    counts: Counter[str] = Counter()

    for paper in papers:
        text = strip_markup(f"{paper.title}. {paper.abstract}")
        tokens = [t.lower() for t in _TOKEN.findall(text)]
        seen_in_paper: set[str] = set()
        for n in (1, 2, 3):
            for i in range(len(tokens) - n + 1):
                gram = tokens[i : i + n]
                if gram[0] in _GENERIC or gram[-1] in _GENERIC:
                    continue
                if any(len(t) < 3 for t in gram):
                    continue
                if n == 1 and gram[0] in _WEAK_ALONE:
                    continue
                phrase = " ".join(gram)
                if phrase in existing or phrase in seen_in_paper:
                    continue
                seen_in_paper.add(phrase)
                # 词组越长越具体，值得的候选几乎全是二三元组，加权要够狠
                counts[phrase] += n * n
    return [(term, c) for term, c in counts.most_common(top * 4) if c >= 6][:top]


def _existing_terms(cfg: Config) -> set[str]:
    out: set[str] = set()
    for spec in (cfg.profile.get("keywords") or {}).values():
        for term in spec.get("terms") or []:
            out.add(term.lower())
    return out


def write_report(path: Path, papers: list[Paper], terms: list[tuple[str, int]]) -> None:
    lines = [
        "# 领域收敛建议",
        "",
        f"种子论文 {len(papers)} 篇，抽出 {len(terms)} 个候选术语。",
        "",
        "把你认可的词条复制到 `_litpipe/config/field_profile.yaml` 的 `keywords.core.terms`",
        "或 `adjacent.terms` 下面。**这里不会自动改配置。**",
        "",
        "## 候选术语",
        "",
        "| 术语 | 加权词频 |",
        "| --- | --- |",
    ]
    lines += [f"| {term} | {count} |" for term, count in terms]
    lines += ["", "## 种子论文", ""]
    for paper in sorted(papers, key=lambda p: p.year or 0, reverse=True):
        year = paper.year or "n.d."
        lines.append(f"- ({year}) {paper.title}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
