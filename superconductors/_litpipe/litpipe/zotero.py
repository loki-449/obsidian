"""Zotero 交互：读库（sqlite 只读快照）+ 入库（本地连接器 API）。

读：直接查 zotero.sqlite。为了不跟正在运行的 Zotero 抢锁，总是先复制到临时文件再查。
写：走 Zotero 本地连接器 http://127.0.0.1:23119/connector/saveItems，
    这是浏览器插件用的同一个接口，Zotero 会自己去下载 PDF 附件。
    Zotero 没开时退化成导出 .bib，手动拖进去。
"""

from __future__ import annotations

import re
import shutil
import sqlite3
import tempfile
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from .config import Config
from .http import Client
from .model import Paper, norm_title

BBT_FILES = ("better-bibtex.sqlite", "better-bibtex.migrated")

# Zotero itemTypeID 里这些不是"文献"
_NON_ITEM_TYPES = ("attachment", "note", "annotation")


@dataclass
class ZItem:
    """Zotero 库里已有的一条文献。回填卡片时用。"""

    key: str = ""
    citekey: str = ""
    item_type: str = ""
    title: str = ""
    abstract: str = ""
    authors: list[str] = field(default_factory=list)
    year: str = ""
    doi: str = ""
    journal: str = ""
    url: str = ""
    archive_id: str = ""
    date_added: str = ""
    date_modified: str = ""
    tags: list[str] = field(default_factory=list)
    collections: list[str] = field(default_factory=list)
    pdf_paths: list[str] = field(default_factory=list)

    @property
    def select_uri(self) -> str:
        return f"zotero://select/library/items/{self.key}"


# ============================================================ 读
@contextmanager
def _snapshot(path: Path) -> Iterator[sqlite3.Connection]:
    if not path.exists():
        raise FileNotFoundError(f"找不到 {path}")
    tmp = Path(tempfile.gettempdir()) / f"litpipe_{path.name}"
    shutil.copyfile(path, tmp)
    conn = sqlite3.connect(tmp)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def _load_citekeys(cfg: Config) -> dict[str, str]:
    """itemKey -> citationKey。Better BibTeX 7 把这张表挪到了 .migrated 文件里。"""
    for name in BBT_FILES:
        path = cfg.zotero_data_dir / name
        if not path.exists():
            continue
        try:
            with _snapshot(path) as conn:
                rows = conn.execute(
                    "SELECT itemKey, citationKey FROM citationkey"
                ).fetchall()
                if rows:
                    return {r["itemKey"]: r["citationKey"] for r in rows}
        except sqlite3.Error:
            continue
    return {}


def read_library(cfg: Config, limit: int | None = None) -> list[ZItem]:
    citekeys = _load_citekeys(cfg)

    with _snapshot(cfg.zotero_db) as conn:
        placeholders = ",".join("?" * len(_NON_ITEM_TYPES))
        sql = f"""
            SELECT i.itemID, i.key, i.dateAdded, i.dateModified, t.typeName
            FROM items i
            JOIN itemTypes t ON i.itemTypeID = t.itemTypeID
            WHERE t.typeName NOT IN ({placeholders})
              AND i.itemID NOT IN (SELECT itemID FROM deletedItems)
            ORDER BY i.dateAdded DESC
        """
        if limit:
            sql += f" LIMIT {int(limit)}"
        rows = conn.execute(sql, _NON_ITEM_TYPES).fetchall()
        ids = [r["itemID"] for r in rows]
        if not ids:
            return []

        fields = _fetch_fields(conn, ids)
        creators = _fetch_creators(conn, ids)
        tags = _fetch_tags(conn, ids)
        collections = _fetch_collections(conn, ids)
        pdfs = _fetch_pdfs(conn, ids, cfg.zotero_data_dir / "storage")

    out: list[ZItem] = []
    for row in rows:
        iid = row["itemID"]
        data = fields.get(iid, {})
        date = data.get("date", "")
        out.append(
            ZItem(
                key=row["key"],
                citekey=citekeys.get(row["key"], ""),
                item_type=row["typeName"],
                title=data.get("title", ""),
                abstract=data.get("abstractNote", ""),
                authors=creators.get(iid, []),
                year=_year(date),
                doi=data.get("DOI", ""),
                journal=data.get("publicationTitle", "") or data.get("proceedingsTitle", ""),
                url=data.get("url", ""),
                archive_id=data.get("archiveID", ""),
                date_added=row["dateAdded"],
                date_modified=row["dateModified"],
                tags=tags.get(iid, []),
                collections=collections.get(iid, []),
                pdf_paths=pdfs.get(iid, []),
            )
        )
    return out


def _chunks(seq: list[int], size: int = 900) -> Iterator[list[int]]:
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


def _fetch_fields(conn: sqlite3.Connection, ids: list[int]) -> dict[int, dict[str, str]]:
    wanted = ("title", "abstractNote", "date", "DOI", "publicationTitle",
              "proceedingsTitle", "url", "extra", "archiveID")
    out: dict[int, dict[str, str]] = {}
    for chunk in _chunks(ids):
        q = ",".join("?" * len(chunk))
        w = ",".join("?" * len(wanted))
        for row in conn.execute(
            f"""SELECT d.itemID, f.fieldName, v.value
                FROM itemData d
                JOIN fields f ON d.fieldID = f.fieldID
                JOIN itemDataValues v ON d.valueID = v.valueID
                WHERE d.itemID IN ({q}) AND f.fieldName IN ({w})""",
            (*chunk, *wanted),
        ):
            out.setdefault(row["itemID"], {})[row["fieldName"]] = row["value"]
    return out


def _fetch_creators(conn: sqlite3.Connection, ids: list[int]) -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    for chunk in _chunks(ids):
        q = ",".join("?" * len(chunk))
        for row in conn.execute(
            f"""SELECT ic.itemID, c.firstName, c.lastName
                FROM itemCreators ic
                JOIN creators c ON ic.creatorID = c.creatorID
                WHERE ic.itemID IN ({q})
                ORDER BY ic.itemID, ic.orderIndex""",
            chunk,
        ):
            name = " ".join(p for p in (row["firstName"], row["lastName"]) if p).strip()
            if name:
                out.setdefault(row["itemID"], []).append(name)
    return out


def _fetch_tags(conn: sqlite3.Connection, ids: list[int]) -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    for chunk in _chunks(ids):
        q = ",".join("?" * len(chunk))
        for row in conn.execute(
            f"""SELECT it.itemID, t.name FROM itemTags it
                JOIN tags t ON it.tagID = t.tagID
                WHERE it.itemID IN ({q})""",
            chunk,
        ):
            out.setdefault(row["itemID"], []).append(row["name"])
    return out


def _fetch_collections(conn: sqlite3.Connection, ids: list[int]) -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    for chunk in _chunks(ids):
        q = ",".join("?" * len(chunk))
        for row in conn.execute(
            f"""SELECT ci.itemID, c.collectionName FROM collectionItems ci
                JOIN collections c ON ci.collectionID = c.collectionID
                WHERE ci.itemID IN ({q})""",
            chunk,
        ):
            out.setdefault(row["itemID"], []).append(row["collectionName"])
    return out


def _fetch_pdfs(
    conn: sqlite3.Connection, ids: list[int], storage: Path
) -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    for chunk in _chunks(ids):
        q = ",".join("?" * len(chunk))
        for row in conn.execute(
            f"""SELECT ia.parentItemID, ia.path, i.key
                FROM itemAttachments ia
                JOIN items i ON ia.itemID = i.itemID
                WHERE ia.parentItemID IN ({q})
                  AND ia.contentType = 'application/pdf'
                  AND ia.path IS NOT NULL""",
            chunk,
        ):
            path = row["path"] or ""
            if path.startswith("storage:"):
                full = storage / row["key"] / path[len("storage:"):]
            else:
                full = Path(path)
            out.setdefault(row["parentItemID"], []).append(str(full))
    return out


def _year(date: str) -> str:
    return date[:4] if date[:4].isdigit() else ""


_ARXIV_IN_TEXT = re.compile(r"(\d{4}\.\d{4,5})")


def match_items(items: list[ZItem], papers: list[Paper]) -> dict[str, ZItem]:
    """把刚推进去的条目认回来，拿 itemKey 和 citekey 写进卡片。

    按 DOI -> arXiv 号 -> 归一化标题 三级匹配。Zotero 里可能本来就有同一篇
    （你之前手动存过），认到哪个都行，反正指向同一篇文章。
    """
    by_doi: dict[str, ZItem] = {}
    by_arxiv: dict[str, ZItem] = {}
    by_title: dict[str, ZItem] = {}

    for item in items:
        if item.doi:
            by_doi.setdefault(item.doi.strip().lower(), item)
        for text in (item.archive_id, item.url):
            found = _ARXIV_IN_TEXT.search(text or "")
            if found:
                by_arxiv.setdefault(found.group(1), item)
                break
        if item.title:
            by_title.setdefault(norm_title(item.title), item)

    out: dict[str, ZItem] = {}
    for paper in papers:
        hit = None
        if paper.doi:
            hit = by_doi.get(paper.doi.strip().lower())
        if hit is None and paper.arxiv_id:
            found = _ARXIV_IN_TEXT.search(paper.arxiv_id)
            if found:
                hit = by_arxiv.get(found.group(1))
        if hit is None and paper.title:
            hit = by_title.get(norm_title(paper.title))
        if hit is not None:
            out[paper.key] = hit
    return out


# ============================================================ 写
def connector_alive(cfg: Config, client: Client) -> bool:
    url = cfg.section("zotero").get("connector_url", "http://127.0.0.1:23119")
    resp = client.get(f"{url}/connector/ping")
    return resp is not None and resp.status_code == 200


def selected_collection(cfg: Config, client: Client) -> str:
    """连接器把条目存进 Zotero 界面里当前选中的分类，没法在请求里指定目标。
    所以这里只能读出来告诉你，选错了自己去 Zotero 里点一下。"""
    url = cfg.section("zotero").get("connector_url", "http://127.0.0.1:23119")
    try:
        resp = client.session.post(
            f"{url}/connector/getSelectedCollection",
            json={},
            headers={"Content-Type": "application/json"},
            timeout=client.timeout,
        )
    except Exception:
        return ""
    if resp.status_code != 200:
        return ""
    try:
        return (resp.json() or {}).get("name", "") or ""
    except ValueError:
        return ""


def push(papers: list[Paper], cfg: Config, client: Client) -> tuple[int, list[Paper]]:
    """推进 Zotero。返回 (成功数, 失败的条目)。"""
    zconf = cfg.section("zotero")
    base = zconf.get("connector_url", "http://127.0.0.1:23119")
    # 默认只推元数据。全文交给 Zotero 的 Find Available PDF，需要哪篇抓哪篇。
    attach = bool(zconf.get("attach_oa_pdf", False))

    ok, failed = 0, []
    for paper in papers:
        # 每篇独立 session：同一 session 连推容易触发 409
        payload = {
            "sessionID": uuid.uuid4().hex,
            "uri": paper.url or (f"https://doi.org/{paper.doi}" if paper.doi else ""),
            "items": [_to_connector_item(paper, attach)],
        }
        try:
            resp = client.session.post(
                f"{base}/connector/saveItems",
                json=payload,
                headers={"Content-Type": "application/json", "X-Zotero-Connector-API-Version": "3"},
                timeout=client.timeout,
            )
        except Exception as exc:
            print(f"  [zotero] 失败 {paper.citekey()}: {exc}")
            failed.append(paper)
            continue
        if resp.status_code in (200, 201, 409):
            # 409：偶发会话冲突或重复提交。后面靠回读匹配认领，不记失败。
            ok += 1
        else:
            print(f"  [zotero] 失败 {paper.citekey()}: HTTP {resp.status_code}")
            failed.append(paper)
    return ok, failed


def _to_connector_item(paper: Paper, attach: bool = False) -> dict:
    creators = []
    for name in paper.authors:
        parts = name.strip().rsplit(" ", 1)
        if len(parts) == 2:
            creators.append({"firstName": parts[0], "lastName": parts[1], "creatorType": "author"})
        else:
            creators.append({"lastName": name.strip(), "creatorType": "author", "fieldMode": 1})

    item: dict = {
        "itemType": "preprint" if paper.source == "arxiv" and not paper.journal else "journalArticle",
        "title": paper.title,
        "creators": creators,
        "abstractNote": paper.abstract,
        "date": str(paper.year or ""),
        "DOI": paper.doi,
        "url": paper.url,
        "tags": [{"tag": t} for t in _flat_tags(paper)],
    }
    if paper.journal:
        item["publicationTitle"] = paper.journal
    if paper.arxiv_id:
        item["repository"] = "arXiv"
        item["archiveID"] = f"arXiv:{paper.arxiv_id}"
    if attach and paper.pdf_url:
        item["attachments"] = [
            {
                "title": "Full Text PDF",
                "url": paper.pdf_url,
                "mimeType": "application/pdf",
                "snapshot": False,
            }
        ]
    return item


def _flat_tags(paper: Paper) -> list[str]:
    """Zotero 端只放少量定位用标签，正交轴的完整信息在 Obsidian 卡片里。"""
    out = ["litpipe"]
    for axis in ("role", "system", "method"):
        for value in _as_list(paper.tags.get(axis)):
            out.append(f"{axis}/{value}")
    return out


def _as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v]
    return [str(value)]


def write_bibtex(papers: list[Paper], path: Path) -> int:
    """连接器不可用时的兜底：导出 .bib，手动拖进 Zotero。"""
    lines = []
    for paper in papers:
        entry_type = "article" if paper.journal else "misc"
        fields = {
            "title": paper.title,
            "author": " and ".join(paper.authors),
            "year": str(paper.year or ""),
            "journal": paper.journal,
            "doi": paper.doi,
            "url": paper.pdf_url or paper.url,
            "abstract": paper.abstract,
        }
        if paper.arxiv_id:
            fields["eprint"] = paper.arxiv_id
            fields["archiveprefix"] = "arXiv"
        body = ",\n".join(
            f"  {k} = {{{_escape(v)}}}" for k, v in fields.items() if v
        )
        lines.append(f"@{entry_type}{{{paper.citekey()},\n{body}\n}}\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return len(papers)


def _escape(value: str) -> str:
    return value.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")
