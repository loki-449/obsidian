---
title: ΔELF 初步分析结果
date: 2026-07-16
tags: [ΔELF, Bader, 热点分析, A3XH7]
---

# ΔELF 初步分析结果

> 15 个 A₃XH₇ 体系，baseline=La₃AgH₇, 5 个 Pm-3m 高对称热点位置。

## 数据来源

- ΔELFCAR: `test/delta_ELFCAR_TOT/` (15 个 v2 文件, 60³ 网格)
- Bader: `test/317/bader_H.csv`
- Origin CSV: `test/delta_ELFCAR_TOT/for_origin.csv`

## 关键数字

### 趋势一致性

- **Cs 体系** ΔELF 波动最大：H2_mid ~ -0.69, H_isolated ~ +0.34
- **Ce/La 体系** ΔELF 最浅 (|ΔELF| < 0.1)
- **Ba/Sr/Ca/Y 体系** 中间态: H2_mid -0.13 ~ -0.27

### 相关性

- H Bader dq vs H2_mid ΔELF: corr = -0.67
- |H_dq| vs |H2_mid| ΔELF: corr = -0.68

### 异常体系

- **Ca3PdH7** H2_mid 符号反转 (+0.22)
- **Cs3AgH7 vs Cs3AuH7** H1b_to_H6e 符号相反
- **Sr3AgH7** H2_mid 正号 (+0.18)

## 结论判断

**整体趋势一致性良好** — 可以继续推进跨家族验证。

需进一步解释的异常点：
1. Ca3PdH7, Sr3AgH7 的 H2_mid 符号反转 → 检查是否与 Pd/Ag 的 d 轨道填充有关
2. Cs3AgH7 vs Cs3AuH7 的 H1b_to_H6e 符号 → X 位 d 轨道与孤立 H 的相互作用差异
3. 结合 Bader 电荷数据一起讨论
