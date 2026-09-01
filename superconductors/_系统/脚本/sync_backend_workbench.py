"""后端工作台 → Obsidian 文件库推送脚本。

按 _系统/后端⇄Obsidian同步约定.md 的映射，把 E:/workplace/workbench/ 的计划文件
增量推送到本 Obsidian vault。安全策略：只创建缺失的目标、合并不覆盖既有科研正文。

映射：
  day/YYYY-MM-DD.md   -> 记录/每日研究日志/YYYY/YYYY-MM-DD.md   (daily_log)
  week/YYYY-Wnn.md    -> 记录/科研计划/周计划/YYYY-Wnn.md        (plan_tree week)
  month/YYYY-MM.md    -> 记录/科研计划/月计划/YYYY-MM.md         (plan_tree month)
  year/YYYY.md        -> 记录/科研计划/年计划/YYYY.md            (plan_tree year)

用法:
  python _系统/脚本/sync_backend_workbench.py            # 默认 --dry-run
  python _系统/脚本/sync_backend_workbench.py --apply     # 真正写盘
  python _系统/脚本/sync_backend_workbench.py --apply --force  # 覆盖既有目标
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

BACKEND_ROOT = Path(r"E:/workplace/workbench").resolve()
VAULT_ROOT = Path(__file__).resolve().parents[2]

# scope -> (后端子目录, Obsidian子目录, period 正则)
PLAN_MAP = [
    ("week",  "科研计划/周计划", re.compile(r"^\d{4}-W\d{2}$")),
    ("month", "科研计划/月计划", re.compile(r"^\d{4}-\d{2}$")),
    ("year",  "科研计划/年计划", re.compile(r"^\d{4}$")),
]


def push_file(src: Path, dst: Path, apply: bool, force: bool, dry_log: list[str], applied: list[str]) -> None:
    if dst.exists() and not force:
        dry_log.append(f"SKIP(已存在,未force) {dst.relative_to(VAULT_ROOT).as_posix()}")
        return
    if apply:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        applied.append(f"WROTE {dst.relative_to(VAULT_ROOT).as_posix()}")
    else:
        dry_log.append(f"WOULD_WRITE {src} -> {dst.relative_to(VAULT_ROOT).as_posix()}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="真正写盘（默认 dry-run）")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的目标文件")
    args = ap.parse_args()

    dry_log: list[str] = []
    applied: list[str] = []

    # 1) 每日日志
    day_src = BACKEND_ROOT / "day"
    if day_src.exists():
        for p in sorted(day_src.glob("*.md")):
            m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})\.md", p.name)
            if not m:
                continue
            date = m.group(1)
            dst = VAULT_ROOT / "记录/每日研究日志" / date[:4] / f"{date}.md"
            push_file(p, dst, args.apply, args.force, dry_log, applied)

    # 2) 周/月/年计划
    for scope, sub, pat in PLAN_MAP:
        src_dir = BACKEND_ROOT / scope
        if not src_dir.exists():
            continue
        for p in sorted(src_dir.glob("*.md")):
            if p.name.startswith("_"):
                continue
            period = p.stem
            if not pat.match(period):
                continue
            dst = VAULT_ROOT / "记录" / sub / f"{period}.md"
            push_file(p, dst, args.apply, args.force, dry_log, applied)

    # 3) 报告
    print("== dry-run / skipped ==")
    for line in dry_log:
        print("  " + line)
    print("== applied ==")
    for line in applied:
        print("  " + line)
    if not dry_log and not applied:
        print("（后端 workbench 无可推送的计划文件）")
    print(f"结果：{len(applied)} 写入，{len(dry_log)} 跳过/待写")
    return 0 if not dry_log or args.apply else 1


if __name__ == "__main__":
    sys.exit(main())
