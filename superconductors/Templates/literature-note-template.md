---
title: "{{title}}"
authors: "{{authors}}"
year: "{{date | format('YYYY')}}"
journal: "{{publicationTitle}}"
citekey: "{{citekey}}"
zotero: "{{desktopURI}}"
tags:
  - 文献
status: 未读
---

# {{title}}

## 基本信息
- 作者：{{authors}}
- 期刊：{{publicationTitle}}
- 年份：{{date | format('YYYY')}}
- DOI：{{DOI}}
- 期刊分区：{{extra}}
- [📎 在Zotero中打开]({{desktopURI}})
- [📄 打开PDF]({{firstAttachmentZoteroLink}})

## 🔬 研究问题
{{abstractNote}}

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