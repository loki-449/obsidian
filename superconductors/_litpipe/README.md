# litpipe — 文献抓取 / 打分 / 入库管道

把 arXiv + OpenAlex 的新文献按领域画像筛一遍，高分的打上正交标签后推进
Zotero（只推元数据），同时在 Obsidian 里生成扁平卡片。

```
fetch → 打分 → [高分进队列 | 中间档进收件箱 | 低分丢弃]
accept → 把收件箱勾选项转入队列
sync  → LLM 打标签 → 推 Zotero → 写 Obsidian 卡片
```

PDF 不走这条管道。全文用 Zotero 的 Find Available PDF（配好机构代理即可）。

## 一次性配置

1. 依赖（本机已有的话可跳过）：

   ```
   pip install -r requirements.txt
   ```

2. 配置：

   ```
   copy config\settings.example.yaml config\settings.yaml
   ```

   按需改 `paths`、`network.contact_email`、代理。`settings.yaml` 已在 `.gitignore`。

3. DeepSeek API key（打标签用）：

   ```powershell
   [Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY", "sk-...", "User")
   ```

   当前 PowerShell 会话要立刻生效的话再执行一次 `$env:DEEPSEEK_API_KEY="sk-..."`。

4. Zotero：打开客户端，侧栏点到目标分类（默认提醒名是 `0_管道入库`）。
   连接器只能存进**当前选中**的分类，请求里指定不了。

## 每周工作流

在 `_litpipe` 目录下：

```powershell
python run.py fetch                  # 抓最近 7 天，打分，更新收件箱
# 打开 Obsidian → 00_MOC/文献收件箱.md，勾想要的
python run.py accept                 # 勾中的进待同步；可加 --drop-unchecked
python run.py sync                   # 打标签 + 推 Zotero + 生成卡片
```

小样本试跑：

```powershell
python run.py fetch --days 3 --limit 20
python run.py sync --dry-run         # 只打标签预览，不写库
```

其他：

```powershell
python run.py seeds                  # 用导师论文反推候选关键词 → out/seed_terms.md
python run.py status                 # 各阶段计数
python run.py find "Kondo"           # 按标题回查处理记录
```

## 配置文件

| 文件 | 作用 |
| --- | --- |
| `config/field_profile.yaml` | 领域关键词、arXiv 分类、导师种子、打分阈值 |
| `config/taxonomy.yaml` | 正交标签轴（role / system / method / stage / relevance） |
| `config/settings.yaml` | 路径、网络、Zotero、LLM 供应商 |

种子术语建议写在 `out/seed_terms.md`，**不会自动改配置**——认可的词条自己合进 `field_profile.yaml`。

## Obsidian 产物

- `知识库/03_文献笔记/{citekey}.md` — 一篇一卡
- `知识库/00_MOC/文献收件箱.md` — 待裁决队列
- `知识库/00_MOC/文献总览.md` — Dataview 面板

卡片 frontmatter 的正交轴和手动模板（`Templates/literature-note-template.md`）对齐，
同一套 Dataview 查询两边都能捞到。

## 职责边界

| | Obsidian | Zotero |
| --- | --- | --- |
| 笔记、标签、交叉查询 | 管 | — |
| PDF 阅读、标注、附件 | — | 管 |
| 元数据入库 | 卡片里留 `zotero://` 链接 | 连接器写入 |

## 目录结构

```
_litpipe/
  run.py                 CLI 入口
  config/                配置
  litpipe/               管道代码
    sources/             arXiv / OpenAlex
    resolvers/           PDF 解析链（默认关闭）
  out/                   中间产物（gitignore）
```
