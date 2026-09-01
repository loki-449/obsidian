# 后端 ⇄ Obsidian 同步约定

> 桥接 **后端工作台 E:/workplace/workbench/（DSH / Hesper 计划源）** 与
> 本 Obsidian vault（记录/ 科研日志、知识库/、_系统/）的对应契约。
> 本文件受 _系统/工作台推送约定.md 的总契约约束，并扩展「后端工作台」这条推送来源。

## 1. 为什么需要同步

后端工作台是 Hesper / DSH 的**登记与部署源**（每日计划、周/月/年计划、任务看板联动），
但真正的**观看、留存、历史归档**发生在 Obsidian。因此凡后端产生的计划/日志信息，
必须按既有四类文档契约「及时」在 Obsidian 有对应对象，避免信息只落在 DSH 侧无法长期回看。

## 2. 路径映射（后端 workbench → 本 vault）

| 后端源 | doc_type | 本 vault 目标 | 说明 |
| --- | --- | --- | --- |
| workbench/day/YYYY-MM-DD.md | daily_log | 记录/每日研究日志/YYYY/YYYY-MM-DD.md | 每日日志，frontmatter 加 date/week |
| workbench/week/YYYY-Wnn.md | plan_tree | 记录/科研计划/周计划/YYYY-Wnn.md | scope=week |
| workbench/month/YYYY-MM.md | plan_tree | 记录/科研计划/月计划/YYYY-MM.md | scope=month |
| workbench/year/YYYY.md | plan_tree | 记录/科研计划/年计划/YYYY.md | scope=year |
| workbench/_data/backlog.md 未决任务 | current_task | 记录/我的研究/未来课题规划/当前任务状态.md | 只同步「当前进行中」到 ## 当前进行中 |
| workbench/day/*.md 学习收获 | learning_note | 知识库/04_学习笔记/*.md | 由后端 agent 整理后推送 |
| workbench/taskboard/（看板联动） | 桥文档 | _系统/workbench/taskboard/ | 镜像，非科研正文 |

> 方向：**后端是源，Obsidian 是视图/存档**。Obsidian 侧已存在的科研正文（如既有母计划、
> 文献笔记）**不被后端骨架覆盖**；后端只同步它真实产生的计划/日志/任务条目。

## 3. 同步时序（何时推送）

| 时机 | 动作 |
| --- | --- |
| 每日登记后 | 后端 day/今天.md → 推送为 daily_log（合并进当天目标/进展） |
| 周计划定稿 | 后端 week/本周.md → 推送/合并为 plan_tree(week)，只更新 ## 母计划 树 |
| 当前任务变化 | 后端 backlog 里的「进行中」→ 更新 current_task 的 ## 当前进行中 首条 |
| 周/月/年复盘 | 后端复盘 → 追加到对应 plan_tree 的 ## 复盘 |
| 学习笔记产出 | 后端整理 → 落 learning_note |

## 4. frontmatter 扩展（后端同步的文档）

后端推送的文档除既有公共字段（doc_type/template_version/source/updated_at/tags）外，追加：

| 字段 | 说明 |
| --- | --- |
| origin | backend-workbench（后端来源声明） |
| backend_path | 后端对应文件路径，如 workbench/week/2026-W33.md |
| synced_at | 同步时刻 YYYY-MM-DD（可选，待推送代码支持后启用） |

> 保持 template_version 与既有公共契约一致（当前 = 1）；不破坏既有校验脚本。

## 5. 与既有推送约定/校验的关系

- 本桥档**沿用并依赖** _系统/工作台推送约定.md 的四类文档结构与 check_workbench_docs.py。
- 后端推送的文档同样通过该校验（路径、必填 frontmatter、关键标题）。
- 若校验失败，以 check_workbench_docs.py 输出清单为准，在后端修正后再推送。
- **禁止行为**：不删除/改写 Obsidian 既有科研正文；不把后端空模板/示例覆盖既有日志；
  不用 source: backend-workbench 之外的冷门字段绕过校验。

## 6. 本 vault 中已镜像的后端资产

见 _系统/workbench/README.md（后端工作台结构的 Obsidian 侧镜像与说明），
以及本目录下 workbench/ 中以 backend- 前缀标注的镜像文档。

## 7. 需要时人工触发的同步

- DSH / Hesper agent 会话结束时：把本次会话产生的计划/日志按表 2 落盘。
- 每周日晚：对齐本周 plan_tree 与 current_task。
- 每次后端模板或数据模型变更：同步更新 _系统/workbench/README.md 镜像。
