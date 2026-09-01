#!/usr/bin/env python
"""文献管道命令行入口。

典型一周：
    python run.py fetch          抓最近 7 天，打分，高分的排队，中间档进收件箱
    （在 Obsidian 里打开「文献收件箱」勾选）
    python run.py accept         把勾中的转入待同步
    python run.py sync           打标签 -> 推 Zotero -> 生成卡片

其他：
    python run.py seeds          用导师论文反推候选关键词
    python run.py status         看各阶段有多少篇
    python run.py find <关键词>  回查某篇被怎么处理了
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from litpipe import inbox, notes, score, seeds, state, tagger, zotero
from litpipe.config import Config
from litpipe.http import Client
from litpipe.model import Paper, dedupe, write_jsonl
from litpipe.resolvers import resolve as resolve_pdf
from litpipe.sources import REGISTRY


# ============================================================ fetch
def cmd_fetch(cfg: Config, args: argparse.Namespace) -> int:
    client = Client(cfg)
    enabled = cfg.section("fetch").get("sources") or list(REGISTRY)

    harvested: list[Paper] = []
    for name in enabled:
        fn = REGISTRY.get(name)
        if fn is None:
            print(f"  [fetch] 未知源 {name}，跳过")
            continue
        harvested.extend(fn(cfg, client, lookback_days=args.days))

    harvested = dedupe(harvested)
    print(f"去重后 {len(harvested)} 条")

    with state.open_state(cfg.work_dir / "state.sqlite") as st:
        known = st.known()
        fresh = [p for p in harvested if p.key not in known]
        print(f"其中新增 {len(fresh)} 条（{len(harvested) - len(fresh)} 条以前见过）")

        if args.limit:
            fresh = fresh[: args.limit]
            print(f"按 --limit 只处理前 {len(fresh)} 条")

        buckets = score.score_all(fresh, cfg)
        accepted = buckets[score.ACCEPT]
        review = buckets[score.REVIEW]
        rejected = buckets[score.REJECT]
        print(
            f"打分结果：直接入库 {len(accepted)}，待复核 {len(review)}，"
            f"丢弃 {len(rejected)}"
        )

        if cfg.section("resolve").get("chain"):
            for paper in accepted + review:
                resolve_pdf(paper, cfg, client)

        st.record_all(accepted, state.QUEUED)
        st.record_all(review, state.SEEN)
        st.record_all(rejected, state.REJECTED)

        write_jsonl(cfg.work_dir / "rejected.jsonl", rejected)
        pending = _refresh_inbox(cfg, st)

    print(f"收件箱现有 {pending} 篇待裁决 -> {inbox.path_for(cfg.moc_dir)}")
    print("勾选后跑 `python run.py accept`，再跑 `python run.py sync`。")
    return 0


def _refresh_inbox(cfg: Config, st: state.State) -> int:
    path = inbox.path_for(cfg.moc_dir)
    checked, _ = inbox.read_marks(path)
    return inbox.render(path, st.load(state.SEEN), checked)


# ============================================================ accept
def cmd_accept(cfg: Config, args: argparse.Namespace) -> int:
    path = inbox.path_for(cfg.moc_dir)
    if not path.exists():
        print(f"收件箱还不存在：{path}。先跑 `python run.py fetch`。")
        return 1

    checked, unchecked = inbox.read_marks(path)
    if not checked and not (args.drop_unchecked and unchecked):
        print("没有勾选任何条目，什么都没做。")
        return 0

    with state.open_state(cfg.work_dir / "state.sqlite") as st:
        moved = st.set_stage(sorted(checked), state.QUEUED)
        print(f"{moved} 篇转入待同步队列")

        if args.drop_unchecked and unchecked:
            dropped = st.set_stage(sorted(unchecked), state.REJECTED)
            print(f"{dropped} 篇未勾选的已否掉，下次不再出现")

        pending = _refresh_inbox(cfg, st)

    print(f"收件箱剩 {pending} 篇。接着跑 `python run.py sync`。")
    return 0


# ============================================================ sync
def cmd_sync(cfg: Config, args: argparse.Namespace) -> int:
    client = Client(cfg)

    with state.open_state(cfg.work_dir / "state.sqlite") as st:
        queued = st.load(state.QUEUED)
        if args.limit:
            queued = queued[: args.limit]
        if not queued:
            print("待同步队列是空的。")
            return 0
        print(f"待同步 {len(queued)} 篇")

        _tag(queued, cfg, args)

        if args.dry_run:
            _preview(queued)
            print("\n--dry-run：没有推 Zotero，也没有生成卡片。")
            return 0

        pushed = _push_to_zotero(queued, cfg, client)
        written = _write_cards(queued, cfg, st, pushed)

    print(f"完成：生成卡片 {written} 张 -> {cfg.notes_dir}")
    return 0


def _tag(papers: list[Paper], cfg: Config, args: argparse.Namespace) -> None:
    if args.no_tag:
        print("--no-tag：跳过 LLM 打标签")
        return
    try:
        count = tagger.tag_papers(papers, cfg)
    except tagger.TaggerUnavailable as exc:
        print(f"[tagger] 不可用，跳过打标签：{exc}")
        return
    print(f"[tagger] {count}/{len(papers)} 篇打上标签")


def _push_to_zotero(papers: list[Paper], cfg: Config, client: Client) -> dict[str, str]:
    """推元数据进 Zotero，回读拿 itemKey。返回 paper.key -> zotero itemKey。"""
    if not zotero.connector_alive(cfg, client):
        path = cfg.work_dir / "pending.bib"
        zotero.write_bibtex(papers, path)
        print(f"[zotero] 连接器没响应（Zotero 没开？）。已导出 {path}，手动拖进去。")
        print("[zotero] 卡片里的 Zotero 链接会留空，之后重跑 sync 可以补上。")
        return {}

    want = cfg.section("zotero").get("target_collection") or ""
    current = zotero.selected_collection(cfg, client)
    if want and current and current != want:
        print(f"[zotero] 注意：Zotero 里当前选中的是「{current}」，不是「{want}」。")
        print("[zotero] 连接器只能存进选中的分类，要改就去 Zotero 侧栏点一下再重跑。")

    ok, failed = zotero.push(papers, cfg, client)
    print(f"[zotero] 入库 {ok}/{len(papers)}" + (f"，失败 {len(failed)}" if failed else ""))

    library = zotero.read_library(cfg)
    matched = zotero.match_items(library, papers)
    print(f"[zotero] 回读认领到 {len(matched)} 篇的 itemKey")
    return {key: item.key for key, item in matched.items()}


def _write_cards(
    papers: list[Paper], cfg: Config, st: state.State, pushed: dict[str, str]
) -> int:
    written = 0
    for paper in papers:
        zkey = pushed.get(paper.key, "")
        path = notes.write_card(paper, cfg.notes_dir, zkey)
        if path is None:
            print(f"  [notes] 已有卡片，跳过：{paper.citekey()}")
            st.record(paper, state.SYNCED, zotero_key=zkey)
            continue
        written += 1
        st.record(
            paper,
            state.SYNCED,
            zotero_key=zkey,
            note_path=str(path.relative_to(cfg.vault)),
        )
    st.commit()
    return written


def _preview(papers: list[Paper]) -> None:
    print("\n---- 标注预览 ----")
    for paper in papers:
        tags = paper.tags or {}
        print(f"\n[{paper.score}] {paper.title[:90]}")
        print(f"  relevance={tags.get('relevance')}  role={tags.get('role')}")
        print(f"  system={tags.get('system')}  method={tags.get('method')}")


# ============================================================ seeds
def cmd_seeds(cfg: Config, args: argparse.Namespace) -> int:
    client = Client(cfg)
    papers = seeds.collect(cfg, client)
    if not papers:
        print("没拿到种子论文。检查 field_profile.yaml 的 seeds 配置。")
        return 1
    print(f"种子论文 {len(papers)} 篇")

    terms = seeds.suggest_terms(papers, cfg, top=args.top)
    out = cfg.work_dir / "seed_terms.md"
    seeds.write_report(out, papers, terms)
    print(f"候选术语 {len(terms)} 个 -> {out}")
    print("过一遍，认可的手动合并进 field_profile.yaml。这里不自动改配置。")
    return 0


# ============================================================ status / find
def cmd_status(cfg: Config, args: argparse.Namespace) -> int:
    with state.open_state(cfg.work_dir / "state.sqlite") as st:
        counts = st.counts()
    labels = {
        state.SEEN: "待裁决（在收件箱里）",
        state.QUEUED: "待同步",
        state.SYNCED: "已入库",
        state.REJECTED: "已否掉",
    }
    total = sum(counts.values())
    print(f"库里共 {total} 篇：")
    for stage, label in labels.items():
        print(f"  {label:<20} {counts.get(stage, 0)}")
    print(f"\n卡片目录：{cfg.notes_dir}")
    print(f"收件箱：  {inbox.path_for(cfg.moc_dir)}")
    return 0


def cmd_find(cfg: Config, args: argparse.Namespace) -> int:
    with state.open_state(cfg.work_dir / "state.sqlite") as st:
        rows = st.find(args.pattern)
    if not rows:
        print(f"没找到标题含「{args.pattern}」的记录。")
        return 1
    for row in rows:
        print(f"\n[{row['stage']}] {row['title'][:90]}")
        print(f"  分数 {row['score']}  判定 {row['verdict']}  citekey {row['citekey']}")
        if row["note_path"]:
            print(f"  卡片 {row['note_path']}")
        if row["score_detail"]:
            print(f"  命中 {row['score_detail'][:200]}")
    return 0


# ============================================================ main
def main() -> int:
    parser = argparse.ArgumentParser(
        prog="run.py", description="文献抓取 / 打分 / 入库管道"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("fetch", help="抓取并打分")
    p.add_argument("--days", type=int, default=None, help="回看天数，默认读配置")
    p.add_argument("--limit", type=int, default=0, help="只处理前 N 条新文献")
    p.set_defaults(fn=cmd_fetch)

    p = sub.add_parser("accept", help="把收件箱里勾选的转入待同步")
    p.add_argument(
        "--drop-unchecked", action="store_true", help="同时把没勾的永久否掉"
    )
    p.set_defaults(fn=cmd_accept)

    p = sub.add_parser("sync", help="打标签 + 推 Zotero + 生成卡片")
    p.add_argument("--limit", type=int, default=0, help="只处理前 N 篇")
    p.add_argument("--no-tag", action="store_true", help="跳过 LLM 打标签")
    p.add_argument(
        "--dry-run", action="store_true", help="只打标签并预览，不写 Zotero 和卡片"
    )
    p.set_defaults(fn=cmd_sync)

    p = sub.add_parser("seeds", help="用导师论文反推候选关键词")
    p.add_argument("--top", type=int, default=40, help="输出多少个候选术语")
    p.set_defaults(fn=cmd_seeds)

    p = sub.add_parser("status", help="各阶段计数")
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser("find", help="按标题回查处理记录")
    p.add_argument("pattern")
    p.set_defaults(fn=cmd_find)

    args = parser.parse_args()
    try:
        cfg = Config.load()
    except FileNotFoundError as exc:
        print(exc)
        return 1
    return args.fn(cfg, args)


if __name__ == "__main__":
    sys.exit(main())
