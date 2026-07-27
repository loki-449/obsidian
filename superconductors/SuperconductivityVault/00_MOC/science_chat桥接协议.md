---
created: 2026-07-10
tags: [MOC, 元信息]
---

# science_chat ↔ Obsidian 桥接协议

## 角色分工

| 内容类型 | 存放位置 | 路径 |
|----------|----------|------|
| 工作进展、部署、规划 | **science_chat** | `E:\claude_work\science_chat\07_每日工作\` |
| 学习笔记、新知识点 | **Obsidian** | `SuperconductivityVault/06_每日研究日志/` |
| 文献精读笔记 | **两边各一份** | Obsidian 侧用模板生成完整笔记，science_chat 侧用简化版笔记 |
| 综述草稿 | **science_chat** | `science_chat/02_综述与评论/` |
| 论文草稿 | **science_chat** | `science_chat/03_论文草稿/` |
| 推导与伪代码 | **science_chat** | `science_chat/04_推导与计算思路/` |
| 可执行脚本 | **calculation** | `E:\claude_work\Ai_for_science_calculation\calculation\` | [[../02_理论计算方法/DFT/calculation脚本库|calculation 脚本索引]] |

## 知识学习流程

1. Claude 对话中学习新内容
2. 对话结束后，Claude 将知识点写入 Obsidian：`06_每日研究日志/[日期].md`
3. 同时更新对应的 MOC 索引（如 `00_MOC/强关联MOC.md`）
4. science_chat 侧只在当日工作日志中留一条索引链接，不重复记录

## 两边互相引用

- Obsidian → science_chat：使用完整路径 wikilink `[science_chat/02_综述/xxx](E:\claude_work\...)`（Obsidian 支持绝对路径）
- science_chat → Obsidian：使用 Obsidian URI `obsidian://open?vault=hydride_superconduct&file=...`

## Obsidian Vault 现有结构

```
hydride_superconduct/
├── SuperconductivityVault/
│   ├── 00_MOC/           # 知识地图索引
│   ├── 01_基础知识/       # BCS、Eliashberg、氢化物等
│   ├── 02_理论计算方法/   # DFT、声子、EPC、结构预测
│   ├── 03_文献笔记/       # 氢化物超导文献
│   ├── 04_我的研究/       # 硕士课题、未来规划
│   ├── 05_工具与资源/
│   └── 06_每日研究日志/   # ← 新知识点写入这里
├── 强关联/               # Kondo、重整化群、磁学基础
├── Templates/            # 文献、日志、研究笔记模板
├── Clippings/
├── 计算工具-qe/
└── 脚本/
```
