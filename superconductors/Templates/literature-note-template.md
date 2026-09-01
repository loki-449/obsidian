---
title: "{{title}}"
authors: "{{authors}}"
year: "{{date | format('YYYY')}}"
journal: "{{publicationTitle}}"
doi: "{{DOI}}"
arxiv: ""
citekey: "{{citekey}}"
zotero: "{{desktopURI}}"
url: "{{url}}"
source: manual
role: []
system: []
method: []
stage: 未读
relevance: 3
score: 0
added: "{{exportDate | format('YYYY-MM-DD')}}"
tags:
  - 文献
---

# {{title}}

> [!info] 基本信息
> - 作者：{{authors}}
> - 期刊：{{publicationTitle}}
> - 年份：{{date | format('YYYY')}}
> - DOI：{{DOI}}
> - 期刊分区：{{extra}}
> - [在 Zotero 中打开]({{desktopURI}})
> - [打开 PDF]({{firstAttachmentZoteroLink}})

## 摘要

{{abstractNote}}

## 🔬 研究问题

## ⚙️ 主要方法

## 📊 关键结果

## 💡 核心结论

## 🔗 与我研究的关联

## ❓ 问题与待深入理解

## 📝 Zotero标注
{% for annotation in annotations %}
> {{annotation.annotatedText}}
{% if annotation.comment %}> 批注：{{annotation.comment}}{% endif %}
{% endfor %}

---

> [!note]- 正交轴取值参考
> 手填时从这里挑，取值域和 `_litpipe/config/taxonomy.yaml` 保持一致，
> 这样管道建的卡和手建的卡能被同一套 Dataview 查询捞到。
>
> - **role**（可多选）：方法 / 数据 / 理论框架 / 综述 / 竞品 / 工具 / 争议
> - **system**（可多选，可加新值）：镍氧化物 / 铜氧化物 / 铁基超导 / 重费米子 /
>   氢化物 / kagome / 转角石墨烯 / 有机超导 / 模型体系
> - **method**（可多选，可加新值）：DFT、DFT+U、DMFT、GW、QMC、`DMRG/张量网络`、
>   `平均场/解析`、`声子/电声耦合`、结构搜索、ARPES、`STM/STS`、输运、中子散射、
>   高压实验、机器学习
> - **stage**（单选）：未读 / 略读 / 精读 / 已消化
> - **relevance**（1-5）：5 直接关系当前课题，4 同一子方向，3 相邻方向值得知道，
>   2 同领域但用处不大，1 基本无关
