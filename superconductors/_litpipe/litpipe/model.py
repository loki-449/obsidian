"""管道内部统一的文献记录。各个源都归一化成 Paper。"""

from __future__ import annotations

import hashlib
import html
import json
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator

_NON_WORD = re.compile(r"[^a-z0-9]+")
_VERSION = re.compile(r"v\d+$")
_STOPWORDS = {
    "a", "an", "the", "of", "in", "on", "for", "and", "or", "to", "with",
    "from", "at", "by", "as", "is", "are", "via",
}


@dataclass
class Paper:
    title: str = ""
    abstract: str = ""
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    doi: str = ""
    arxiv_id: str = ""
    journal: str = ""
    url: str = ""
    categories: list[str] = field(default_factory=list)
    source: str = ""                       # arxiv / openalex / ...
    pdf_url: str = ""                      # resolver 填
    pdf_via: str = ""                      # 哪个 resolver 拿到的
    score: float = 0.0
    score_detail: dict[str, Any] = field(default_factory=dict)
    verdict: str = ""                      # accept / review / reject
    tags: dict[str, Any] = field(default_factory=dict)   # 正交标签轴

    # -- 身份 ------------------------------------------------------------
    @property
    def key(self) -> str:
        """跨源去重用的稳定标识。"""
        if self.doi:
            return "doi:" + self.doi.lower()
        if self.arxiv_id:
            return "arxiv:" + _VERSION.sub("", self.arxiv_id.lower())
        digest = hashlib.sha1(norm_title(self.title).encode()).hexdigest()[:16]
        return "title:" + digest

    def citekey(self) -> str:
        """生成 Better-BibTeX 风格 citekey：surnameYearFirstword。"""
        surname = "anon"
        if self.authors:
            parts = [p for p in re.split(r"[,\s]+", self.authors[0].strip()) if p]
            if parts:
                surname = parts[-1]
        surname = _NON_WORD.sub("", _deaccent(surname).lower()) or "anon"
        year = str(self.year) if self.year else "nd"
        word = "x"
        for tok in norm_title(self.title).split():
            if tok not in _STOPWORDS and len(tok) > 2:
                word = tok
                break
        return f"{surname}{year}{word}"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Paper":
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in data.items() if k in known})


def _deaccent(text: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", text) if not unicodedata.combining(ch)
    )


def norm_title(title: str) -> str:
    return _NON_WORD.sub(" ", _deaccent(title).lower()).strip()


_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")
_MATH_BLOCK = re.compile(r"<(?:\w+:)?math\b.*?</(?:\w+:)?math>", re.DOTALL | re.I)

# 下标/上标元素，连同它两侧那些本不该有的空白一起匹配。
# 后面跟大写字母或左括号时说明化学式还没写完，把尾部空白也吃掉。
# 注意：标签名用 (?i:...) 局部忽略大小写，不能给整条加 re.I ——
# 否则 (?=[A-Z(]) 也会匹配 "under" 的 u，把化学式后面的空格吃掉。
_SUBSUP = re.compile(
    r"\s*<(?i:su[bp])\b[^>]*>\s*(.*?)\s*</(?i:su[bp])>(\s*)(?=[A-Z(])",
    re.DOTALL,
)
_SUBSUP_TAIL = re.compile(
    r"\s*<(?i:su[bp])\b[^>]*>\s*(.*?)\s*</(?i:su[bp])>",
    re.DOTALL,
)


def strip_markup(text: str) -> str:
    """去掉标题/摘要里的 XML / HTML 标记。

    两类常见污染：
      1. MathML 公式块（块内有换行缩进）—— 整块去标签并压掉空白，
         否则 La3Ni2O7 会散成 "La 3 Ni 2 O 7"。
      2. HTML <sub>/<sup>（空格在标签外）—— "CoBi <sub>2</sub> Te <sub>4</sub>"
         要收成 CoBi2Te4；下标后若还跟元素符号，尾部空白也吃掉。
    """
    if not text:
        return ""
    if "<" in text:
        text = _MATH_BLOCK.sub(_squash_math, text)
        text = _SUBSUP.sub(r"\1", text)
        text = _SUBSUP_TAIL.sub(r"\1", text)
        text = _TAG.sub("", text)
    return _WS.sub(" ", html.unescape(text)).strip()


def _squash_math(match: re.Match[str]) -> str:
    return _WS.sub("", html.unescape(_TAG.sub("", match.group(0))))


# -- jsonl 读写 ----------------------------------------------------------
def write_jsonl(path: Path, papers: Iterable[Paper]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as fh:
        for paper in papers:
            fh.write(json.dumps(paper.to_dict(), ensure_ascii=False) + "\n")
            count += 1
    return count


def read_jsonl(path: Path) -> Iterator[Paper]:
    if not path.exists():
        return
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield Paper.from_dict(json.loads(line))


def dedupe(papers: Iterable[Paper]) -> list[Paper]:
    """按 key 去重；同一篇优先保留信息更全的那份（有 DOI > 有摘要 > 更长）。"""
    best: dict[str, Paper] = {}
    for paper in papers:
        prev = best.get(paper.key)
        if prev is None or _richness(paper) > _richness(prev):
            best[paper.key] = paper
    return list(best.values())


def _richness(paper: Paper) -> tuple[int, int, int]:
    return (bool(paper.doi), bool(paper.abstract), len(paper.abstract))
