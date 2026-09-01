# 后端工作台结构（Obsidian 侧镜像）

> 后端 `E:/workplace/workbench/`（Hesper / DSH 计划源）的**只读镜像说明**。
> 完整契约见 _系统/后端⇄Obsidian同步约定.md 与 _系统/工作台推送约定.md。

## 后端目录结构

`text
workbench/                      （后端源目录）
  README.md                     # 总入口 + 使用手册
  _data/
    model.md                    # 统一数据模型：Plan ⇄ Task ⇄ Board
    backlog.md                  # 未决任务总表（观看入口）
  year/    YYYY.md              # 年度计划（→ plan_tree scope=year）
  month/   YYYY-MM.md           # 月度计划（→ plan_tree scope=month）
  week/    YYYY-Wnn.md          # 周计划（→ plan_tree scope=week）
  day/     YYYY-MM-DD.md        # 每日登记（→ daily_log）
  taskboard/                    # 与 dsh-task-board 联动（seed/queue/README）
  templates/  task-card.md      # 任务卡规范
  archive/                      # 归档
`

## 与本 vault 的对应关系

后端 day/week/month/year → 本 vault 的 记录/每日研究日志、记录/科研计划（周/月/年）。
后端 backlog 进行中 → 记录/我的研究/未来课题规划/当前任务状态.md。
后端学习收获 → 知识库/04_学习笔记/。

## 同步纪律

- 后端是**源**，Obsidian 是**视图/存档**。
- 推送严格遵循 _系统/工作台推送约定.md 的四类文档契约，可用 check_workbench_docs.py 校验。
- **不覆盖**本 vault 既有科研正文；后端只增量/合并同步。
- 本镜像只记录后端结构，便于在 Obsidian 里也能看到后端工作台长什么样。
