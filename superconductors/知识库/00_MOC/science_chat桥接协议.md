---
created: 2026-07-10
updated: 2026-08-14
tags: [MOC, 元信息]
---

# science_chat ↔ Obsidian ↔ 工作台 桥接协议

> 约定 science_chat、Obsidian 与工作台三方的角色分工和互相引用方式。工作台推送文档的模板与字段契约见 [[工作台推送约定]]。

## 角色分工

| 内容类型 | 存放位置 | 路径 |
|----------|----------|------|
| 工作进展、部署、规划 | **science_chat** | `E:\claude_work\science_chat\07_每日工作\` |
| 学习笔记、新知识点 | **Obsidian** | `记录/每日研究日志/` |
| 文献精读笔记 | **两边各一份** | Obsidian 侧用模板生成完整笔记，science_chat 侧用简化版笔记 |
| 综述草稿 | **science_chat** | `E:\claude_work\science_chat\02_综述与评论\` |
| 论文草稿 | **science_chat** | `E:\claude_work\science_chat\03_论文草稿\` |
| 推导与伪代码 | **science_chat** | `E:\claude_work\science_chat\04_推导与计算思路\` |
| 可执行脚本 | **calculation** | `E:\claude_work\Ai_for_science_calculation\calculation\` | [[../02_理论计算方法/DFT/calculation脚本库|calculation 脚本索引]] |
| 每日日志、任务状态、学习笔记、周/月/年计划 | **Obsidian（工作台写入）** | 路径映射见 [[工作台推送约定]] |

## 知识学习流程

1. Claude 对话中学习新内容
2. 对话结束后，Claude 将知识点写入 Obsidian：`记录/每日研究日志/[日期].md`
3. 同时更新对应的 MOC 索引（如 `00_MOC/超导总地图.md`）
4. science_chat 侧只在当日工作日志中留一条索引链接，不重复记录
5. 工作台按 [[工作台推送约定]] 写入每日日志、当前任务状态、学习笔记与计划树，不直接写 science_chat 目录

## 三方互相引用

- Obsidian → science_chat：使用绝对路径 Markdown 链接，路径统一用正斜杠。文件示例：`[今日工作日志](E:/claude_work/science_chat/07_每日工作/2026-08-14_周五.md)`；目录示例：`[打开目录](E:/claude_work/science_chat/07_每日工作/)`。
- science_chat → Obsidian：使用 Obsidian URI：`obsidian://open?vault=superconductors&file=...`。
- 工作台 → Obsidian：经 `system/workbench/obsidian_adapter.py` 读写四类文档；模板中的 `<% tp.date.now(...) %>` 占位符由适配器替换为实际日期。

## 工作台推送文档

四类文档的路径、frontmatter、关键标题与版本规则统一由 `_系统/工作台推送约定.md` 管理，校验脚本为 `_系统/脚本/check_workbench_docs.py`。

## Obsidian Vault 现有结构

```text
superconductors/
├── 知识库/           # 知识点：MOC、基础理论、计算方法、文献笔记、学习笔记
│   ├── 00_MOC/
│   ├── 00_配置备忘/
│   ├── 01_基础知识/
│   ├── 02_理论计算方法/
│   ├── 03_文献笔记/
│   ├── 04_学习笔记/
│   └── 05_工具与资源/
├── 记录/             # 用户记录：每日日志、科研计划、课题状态、Agent 学习
│   ├── 每日研究日志/
│   ├── 科研计划/
│   ├── 我的研究/
│   └── Agent学习/
├── 收件箱/Clippings/
├── _待删除/
├── _系统/脚本/
├── _litpipe/
└── Templates/
```
