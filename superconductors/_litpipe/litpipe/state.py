"""跨轮次的处理状态。out/state.sqlite。

管道每周跑一次，同一篇文献会被 arXiv 和 OpenAlex 反复捞到。这里记住每篇的
Paper.key 处理到哪一步了，保证：
  - 已建卡的不重复建卡
  - 已经判过 reject 的不再进复核队列烦你
  - 你想回查"某篇为什么没进来"时，能查到当时的分数和命中详情

stage 的取值就是流水线的位置：
  seen     刚抓到，已打分，还没裁决（review 档在收件箱里等你）
  queued   你在收件箱勾选了，等下一次 sync 处理
  synced   已进 Zotero 并生成卡片，终态
  rejected 分数不够或你手动否掉，终态（但可以用 requeue 捞回来）
"""

from __future__ import annotations

import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .model import Paper

SEEN, QUEUED, SYNCED, REJECTED = "seen", "queued", "synced", "rejected"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    key          TEXT PRIMARY KEY,
    stage        TEXT NOT NULL,
    title        TEXT NOT NULL DEFAULT '',
    doi          TEXT NOT NULL DEFAULT '',
    arxiv_id     TEXT NOT NULL DEFAULT '',
    citekey      TEXT NOT NULL DEFAULT '',
    score        REAL NOT NULL DEFAULT 0,
    verdict      TEXT NOT NULL DEFAULT '',
    score_detail TEXT NOT NULL DEFAULT '',
    zotero_key   TEXT NOT NULL DEFAULT '',
    note_path    TEXT NOT NULL DEFAULT '',
    payload      TEXT NOT NULL DEFAULT '',
    first_seen   REAL NOT NULL DEFAULT 0,
    updated      REAL NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_stage ON papers(stage);
"""


class State:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(_SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    # -- 查询 ------------------------------------------------------------
    def known(self) -> set[str]:
        return {r["key"] for r in self.conn.execute("SELECT key FROM papers")}

    def stage_of(self, key: str) -> str:
        row = self.conn.execute(
            "SELECT stage FROM papers WHERE key = ?", (key,)
        ).fetchone()
        return row["stage"] if row else ""

    def counts(self) -> dict[str, int]:
        return {
            r["stage"]: r["n"]
            for r in self.conn.execute(
                "SELECT stage, COUNT(*) AS n FROM papers GROUP BY stage"
            )
        }

    def load(self, stage: str) -> list[Paper]:
        """把某个阶段的文献还原成 Paper。payload 存的是完整快照。"""
        out: list[Paper] = []
        for row in self.conn.execute(
            "SELECT payload FROM papers WHERE stage = ? AND payload != ''"
            " ORDER BY score DESC",
            (stage,),
        ):
            try:
                out.append(Paper.from_dict(json.loads(row["payload"])))
            except (ValueError, TypeError):
                continue
        return out

    def find(self, pattern: str, limit: int = 20) -> list[sqlite3.Row]:
        """按标题模糊查，用来回查某篇被怎么处理了。"""
        return list(
            self.conn.execute(
                "SELECT * FROM papers WHERE title LIKE ? ORDER BY score DESC LIMIT ?",
                (f"%{pattern}%", limit),
            )
        )

    # -- 写入 ------------------------------------------------------------
    def record(self, paper: Paper, stage: str, **extra: str) -> None:
        now = time.time()
        self.conn.execute(
            """
            INSERT INTO papers (key, stage, title, doi, arxiv_id, citekey, score,
                                verdict, score_detail, zotero_key, note_path,
                                payload, first_seen, updated)
            VALUES (:key, :stage, :title, :doi, :arxiv_id, :citekey, :score,
                    :verdict, :score_detail, :zotero_key, :note_path,
                    :payload, :now, :now)
            ON CONFLICT(key) DO UPDATE SET
                stage        = excluded.stage,
                citekey      = excluded.citekey,
                score        = excluded.score,
                verdict      = excluded.verdict,
                score_detail = excluded.score_detail,
                zotero_key   = CASE WHEN excluded.zotero_key != ''
                                    THEN excluded.zotero_key ELSE papers.zotero_key END,
                note_path    = CASE WHEN excluded.note_path != ''
                                    THEN excluded.note_path ELSE papers.note_path END,
                payload      = excluded.payload,
                updated      = excluded.updated
            """,
            {
                "key": paper.key,
                "stage": stage,
                "title": paper.title,
                "doi": paper.doi,
                "arxiv_id": paper.arxiv_id,
                "citekey": paper.citekey(),
                "score": paper.score,
                "verdict": paper.verdict,
                "score_detail": json.dumps(paper.score_detail, ensure_ascii=False),
                "zotero_key": extra.get("zotero_key", ""),
                "note_path": extra.get("note_path", ""),
                "payload": json.dumps(paper.to_dict(), ensure_ascii=False),
                "now": now,
            },
        )

    def record_all(self, papers: list[Paper], stage: str) -> None:
        for paper in papers:
            self.record(paper, stage)
        self.conn.commit()

    def set_stage(self, keys: list[str], stage: str) -> int:
        if not keys:
            return 0
        placeholders = ",".join("?" * len(keys))
        cur = self.conn.execute(
            f"UPDATE papers SET stage = ?, updated = ? WHERE key IN ({placeholders})",
            (stage, time.time(), *keys),
        )
        self.conn.commit()
        return cur.rowcount

    def commit(self) -> None:
        self.conn.commit()


@contextmanager
def open_state(path: Path) -> Iterator[State]:
    st = State(path)
    try:
        yield st
    finally:
        st.close()
