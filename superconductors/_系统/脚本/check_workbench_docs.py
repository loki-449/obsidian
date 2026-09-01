"""只读校验工作台推送文档的路径、必填 frontmatter 与关键标题。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]

COMMON_FIELDS = ("doc_type", "template_version", "source", "updated_at", "tags")
TYPE_FIELDS = {
    "daily_log": ("date", "week"),
    "current_task": (),
    "learning_note": ("read", "read_date"),
    "plan_tree": ("scope", "period"),
}
KEY_HEADINGS = {
    "daily_log": ("## 🎯 今日目标",),
    "current_task": ("## 当前进行中",),
    "learning_note": (),
    "plan_tree": ("## 母计划",),
}
SCOPE_DIRS = {"week": "周计划", "month": "月计划", "year": "年计划"}
PERIOD_PATTERNS = {
    "week": re.compile(r"^\d{4}-W\d{2}$"),
    "month": re.compile(r"^\d{4}-\d{2}$"),
    "year": re.compile(r"^\d{4}$"),
}
CURRENT_TASK_PATH = VAULT_ROOT / "记录" / "我的研究" / "未来课题规划" / "当前任务状态.md"
DAILY_LOG_DIR = VAULT_ROOT / "记录" / "每日研究日志"
LEARNING_DIR = VAULT_ROOT / "知识库" / "04_学习笔记"
PLAN_ROOT = VAULT_ROOT / "记录" / "科研计划"
TEMPLATE_PATH = VAULT_ROOT / "Templates" / "daily-note-template.md"
SCIENCE_CHAT_DEAD_LINK = "[[science_chat 今日工作]]"
SCIENCE_CHAT_WORK_DIR = "07_每日工作"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    """解析简单 frontmatter：收集顶层 `key: value` 与 `key:` 下的 `- item` 列表。"""
    meta: dict[str, str] = {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return meta
    current_key: str | None = None
    items: list[str] = []
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if current_key and stripped.startswith("- "):
            items.append(stripped[2:].strip())
            continue
        if line[:1].isspace() or ":" not in line:
            continue
        if current_key and items:
            meta[current_key] = ", ".join(items)
        current_key, _, value = line.partition(":")
        current_key = current_key.strip()
        items = []
        value = value.strip()
        if value:
            meta[current_key] = value
    if current_key and items:
        meta[current_key] = ", ".join(items)
    return meta


def check_fields(path: Path, meta: dict[str, str], doc_type: str) -> list[str]:
    rel = path.relative_to(VAULT_ROOT).as_posix()
    problems: list[str] = []
    for field in COMMON_FIELDS + TYPE_FIELDS[doc_type]:
        if field not in meta or not meta[field]:
            problems.append(f"{rel}: 缺少必填 frontmatter 字段 {field}")
    version = meta.get("template_version", "")
    if version and not version.isdigit():
        problems.append(f"{rel}: template_version 必须是正整数")
    if doc_type == "learning_note" and meta.get("read", "").lower() in ("true", "1", "yes", "已读", "done"):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta.get("read_date", "")):
            problems.append(f"{rel}: read=true 时 read_date 必须是 YYYY-MM-DD")
    return problems


def check_headings(path: Path, text: str, doc_type: str) -> list[str]:
    rel = path.relative_to(VAULT_ROOT).as_posix()
    return [f"{rel}: 缺少 {heading}" for heading in KEY_HEADINGS[doc_type] if heading not in text]


def check_daily_logs() -> list[str]:
    problems: list[str] = []
    if not DAILY_LOG_DIR.exists():
        return problems
    for path in sorted(DAILY_LOG_DIR.rglob("*.md")):
        text = read_text(path)
        meta = parse_frontmatter(text)
        problems += check_fields(path, meta, "daily_log")
        problems += check_headings(path, text, "daily_log")
        if SCIENCE_CHAT_DEAD_LINK in text:
            rel = path.relative_to(VAULT_ROOT).as_posix()
            problems.append(f"{rel}: 存在失效链接 {SCIENCE_CHAT_DEAD_LINK}")
    return problems


def check_template() -> list[str]:
    if not TEMPLATE_PATH.is_file():
        return [f"{TEMPLATE_PATH.relative_to(VAULT_ROOT).as_posix()}: 模板不存在"]
    text = read_text(TEMPLATE_PATH)
    rel = TEMPLATE_PATH.relative_to(VAULT_ROOT).as_posix()
    problems: list[str] = []
    if SCIENCE_CHAT_DEAD_LINK in text:
        problems.append(f"{rel}: 模板存在失效链接 {SCIENCE_CHAT_DEAD_LINK}")
    if SCIENCE_CHAT_WORK_DIR not in text:
        problems.append(f"{rel}: 缺少 science_chat 工作日志路径约定（{SCIENCE_CHAT_WORK_DIR}）")
    return problems


def check_current_task() -> list[str]:
    if not CURRENT_TASK_PATH.is_file():
        return [f"{CURRENT_TASK_PATH.relative_to(VAULT_ROOT).as_posix()}: 文件不存在"]
    text = read_text(CURRENT_TASK_PATH)
    meta = parse_frontmatter(text)
    return check_fields(CURRENT_TASK_PATH, meta, "current_task") + check_headings(
        CURRENT_TASK_PATH, text, "current_task"
    )


def check_learning_notes() -> list[str]:
    problems: list[str] = []
    if not LEARNING_DIR.exists():
        return problems
    for path in sorted(LEARNING_DIR.glob("*.md")):
        text = read_text(path)
        meta = parse_frontmatter(text)
        problems += check_fields(path, meta, "learning_note")
    return problems


def check_plan_trees() -> list[str]:
    problems: list[str] = []
    if not PLAN_ROOT.exists():
        return problems
    for scope, dirname in SCOPE_DIRS.items():
        dirpath = PLAN_ROOT / dirname
        if not dirpath.exists():
            continue
        for path in sorted(dirpath.glob("*.md")):
            text = read_text(path)
            meta = parse_frontmatter(text)
            problems += check_fields(path, meta, "plan_tree")
            problems += check_headings(path, text, "plan_tree")
            rel = path.relative_to(VAULT_ROOT).as_posix()
            if meta.get("scope", "") != scope:
                problems.append(f"{rel}: scope 应为 {scope}")
            if not PERIOD_PATTERNS[scope].match(meta.get("period", "")):
                problems.append(f"{rel}: period 不符合 {scope} 格式")
    return problems


def main() -> int:
    problems: list[str] = []
    problems += check_daily_logs()
    problems += check_current_task()
    problems += check_learning_notes()
    problems += check_plan_trees()
    problems += check_template()
    if problems:
        print("工作台推送文档校验未通过：")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("工作台推送文档校验通过：四类文档的路径、frontmatter 与关键标题均满足约定。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
