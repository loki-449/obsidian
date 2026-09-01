> 后端来源：`E:/workplace/workbench/_data/model.md`（只读镜像，后端为准）。

# 统一数据模型规范（Plan ⇄ Task ⇄ Board）

> 这是工作台的「契约层」：所有计划文件、任务卡、看板 seed 都遵循这里定义的字段，
> agent 与脚本才能可靠地读写和联动。
> 关联：`templates/task-card.md`（单卡模板）、`taskboard/seed.tasks.json`（看板结构样例）。

## 1. 三个概念的关系

```text
Plan (工作台 md)           Task (任务卡)            Board (看板记录)
──────────────           ───────────           ───────────────
year/2026.md           任务是最小执行单元       dsh.taskBoard.v1
  └─ month/2026-08.md   一张卡（task-card）     = TaskRecord 数组
       └─ week/…        ↕ 双向引用              {id,title,description,
            └─ day/…     task-id <-> board id    prompt,status,createdAt,
                                                  updatedAt,executions[],
                                                  schedule?}
```

- **Plan** 出生在工作台；**Board** 出生在看板；**Task 卡**是两者的共同语言。
- 一条任务只会出现在**一个层级**文件（就近登记：能在哪天做进 `day/`，本周做进 `week/`，
  本月做进 `month/`，长期目标进 `year/`），并可在 `_data/backlog.md` 汇总。

## 2. Plan 文件 frontmatter（所有层级通用）

每个 `year/month/week/day` md 顶部统一：

```yaml
---
period: "2026-W33"        # 周期标识：2026 | 2026-08 | 2026-W33 | 2026-08-17
type: week                # year | month | week | day
status: open              # open | closed | archived
parent: "2026-08"         # 直接父级周期，root 时省略/填 null
owned_by: ""              # 责任人，可空
tags: [""]                # 可选标签
created_at: "2026-08-17T09:00:00+08:00"
updated_at: "2026-08-17T18:00:00+08:00"
---
```

## 3. 任务卡规范（Task）

见 `templates/task-card.md` 的完整模板。核心字段（在计划文件正文里以卡片块写）：

```text
- [ ] T-<id> 【板<看板id>】任务标题
      desc: 一句话描述
      how:  验收/完成标准（几条可勾）
      est:  预估（如 2h / 0.5d）
      dep:  依赖任务 id（可空）
      to:   board=<boardId,缺省=未灌看板>
      ref:  上级计划链接（如 ../month/2026-08.md）
```

- 状态符号：`[ ]` 待办 / `[~]` 进行中 / `[x]` 完成 / `[!]` 卡住。
- `T-<id>` 是本仓库内任务唯一 id（建议 `T-2026-0817-01` 风格：周期+序号）。
- `看板id` 在任务灌入看板后回填，用于工作台→看板回链。

## 4. Board 记录结构（dsh.taskBoard.v1）

localStorage 键 `dsh.taskBoard.v1` 存一个 **JSON 数组**，每元素是 `TaskRecord`：

```ts
type TaskStatus = 'backlog' | 'todo' | 'running' | 'done' | 'failed'

interface ExecutionRecord {
  id: string            // uuid
  sessionId?: string    // dsh 会话 id（执行后回填）
  startedAt: number     // ms epoch
  endedAt?: number      // ms epoch
  result?: 'succeeded' | 'failed' | 'cancelled'
  error?: string
}

interface ScheduleRule {
  enabled: boolean
  cron: string          // 5 段：分 时 日 月 周
  nextRunAt?: number    // ms epoch
  lastTriggeredAt?: number
}

interface TaskRecord {
  id: string            // 看板内唯一（建议 uuid）
  title: string
  description: string
  prompt: string        // 给 DSH agent 的执行 Prompt
  status: TaskStatus
  createdAt: number     // ms epoch
  updatedAt: number     // ms epoch
  executions: ExecutionRecord[]
  schedule?: ScheduleRule   // 可选定时规则
}
```

5 列顺序：`待规划(backlog) 待办(todo) 进行中(running) 已完成(done) 已失败(failed)`。

解析规则（来自插件源码 `core/store.ts` / `core/tasks.ts`）：
- 缺 `status` 或非法 → 归 `todo`；字段结构非法 → 整行丢弃。
- `schedule` 的 cron 非法 → 该 schedule 被丢弃（任务保留）。
- `executions` 必须为数组。

## 5. 双向一致性约定

- **正向（工作台→看板）**：把新任务卡写进 `taskboard/task-queue.md`，再灌入看板，
  拿回生成的看板 id 回填到卡上 `【板<id>】`。
- **反向（看板→工作台）**：每周/月从看板拉 `dsh.taskBoard.v1`，
  把 `status` 回写到 `_data/backlog.md` 与对应层级文件的卡片状态上。
- 冲突时以**看板执行状态为准**（它是被 agent 驱动的真相源），工作台负责复盘与计划修订。