---
title: "Spin Waves and Electronic Interactions in La2CuO4"
authors:
  - R. Coldea
  - S. M. Hayden
  - G. Aeppli
  - T. G. Perring
  - C. D. Frost
  - T. E. Mason
  - S.-W. Cheong
  - Z. Fisk
year: 2001
journal: Physical Review Letters
doi: 10.1103/PhysRevLett.86.5377
arxiv: ''
citekey: coldea2001spin
zotero: ''
url: https://doi.org/10.1103/PhysRevLett.86.5377
source: manual
role:
  - 数据
  - 方法
system:
  - 铜氧化物
method:
  - 中子散射
stage: 精读
relevance: 5
score: 0
added: '2026-08-31'
tags:
  - 文献
---

# Spin Waves and Electronic Interactions in La2CuO4

> [!info] 基本信息
> - 作者：R. Coldea, S. M. Hayden, G. Aeppli, T. G. Perring, C. D. Frost, T. E. Mason, S.-W. Cheong, Z. Fisk
> - 期刊：*Physical Review Letters* **86**, 5377 (2001)
> - DOI：[10.1103/PhysRevLett.86.5377](https://doi.org/10.1103/PhysRevLett.86.5377)
> - cuprate J 值的标准引用，[[J值实验与理论计算文献汇总|必引]]

## 摘要

The magnetic excitations of the square-lattice spin-1/2 antiferromagnet and high-Tc parent compound La2CuO4 are determined using high-resolution inelastic neutron scattering. Sharp spin waves with absolute intensities in agreement with theory including quantum corrections are found throughout the Brillouin zone.

## 🔬 研究问题

用高分辨率 INS 测量母体 cuprate La₂CuO₄（S=1/2 方晶格反铁磁体）在整个布里渊区内的自旋波色散和绝对强度，检验：(1) 只含最近邻 $J$ 的简单 Heisenberg 模型能否描述观测到的色散；(2) 布里渊区边界（本应因对称性而平坦）为何出现明显色散，其物理起源是什么。

## ⚙️ 主要方法

- ISIS 脉冲中子源 HET 飞行时间谱仪，配合位置灵敏探测器，波矢分辨率比早期工作（如 Hayden et al. 1991）提升约一个数量级。
- 用线性自旋波理论（LSWT）拟合色散关系和绝对散射强度，引入量子重整化因子 $Z_c=1.18$ 修正零点涨落带来的能标重整化（LSWT 的 HP→线性化→傅里叶→Bogoliubov 推导链条见 [[2026年08月31日 研究日志]]）。
- 分别在 295 K（室温）和 10 K（低温）两个温度下重复测量和拟合。

## 📊 关键结果

文章用两种理论假设分别拟合了同一组色散数据，结果并不一致，这正是文章的论证核心。

### 模型一：经验 Heisenberg 模型（仅 $J$、$J'$ 独立，$J''=J_c=0$）

直接拟合数据 + $Z_c=1.18$：

| 温度 | $J$ (meV) | $J'$ (meV) | 备注 |
| :--- | :--- | :--- | :--- |
| 295 K | **111.8 ± 4**（反铁磁） | 拟合为 +11.4（铁磁） | 与超交换理论矛盾——次近邻 $J'$ 理论上应是弱反铁磁 |
| 10 K | **104.1 ± 4**（反铁磁） | 拟合为 −18（强铁磁） | 矛盾进一步加剧 |

### 模型二：单带 Hubbard 模型展开（$t,U$ 约束，自动生成 $J,J',J'',J_c$）

微扰论展开到 $t^4/U^3$ 阶，把各交换常数都写成 Hubbard 参数 $t,U$ 的函数，不再独立拟合：

$$J=\frac{4t^2}{U}-\frac{24t^4}{U^3},\qquad J_c=\frac{80t^4}{U^3},\qquad J'=J''=\frac{4t^4}{U^3}=\frac{J_c}{20}$$

即 $J'$、$J''$ 不再是自由参数，而是由环交换 $J_c$ 唯一决定。用这套约束关系拟合数据先解出 $t,U$，再代回算 $J,J_c$：

| 温度 | $t$ (eV) | $U$ (eV) | $J$ (meV) | $J_c$ (meV) | $J'=J''$ (meV) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 295 K | 0.33 ± 0.02 | 2.9 ± 0.4 | **138.3 ± 4** | **38 ± 8** | 2 ± 0.5（弱反铁磁，符合预期） |
| 10 K | 0.30 ± 0.02 | 2.2 ± 0.4 | **146.3 ± 4** | **61 ± 8** | 3.05 ± 0.5（估算，文中未单独列出） |

两种模型给出的 $J$ 差了约 25%（111.8/104.1 vs 138.3/146.3 meV），差值正好对应被模型一忽略掉的环交换 $J_c$ 的贡献。

## 💡 核心结论

- 文章判定**模型二（Hubbard 展开）给出的 $J\approx138$–$146$ meV 才是物理真实的最近邻反铁磁交换常数**；模型一的低值（104–112 meV）是因为强行把 $J'$、$J_c$ 混在一起用一个独立的 $J'$ 去吸收，导致 $J'$ 被拟合成不合理的铁磁值，是系统误差的信号，不是真实结果。
- 环交换 $J_c\approx38$–$61$ meV（$J_c/J\approx0.27$–0.42），量级与 Cu-O-Cu 超交换路径上的多体跃迁过程（$t^4/U^3$ 阶）一致，且量级上与高 Tc 材料的配对能标可比，暗示环/多体交换机制可能与掺杂后的超导配对相关。
- $t,U$ 随温度从 295 K 降到 10 K 发生变化（$U$ 从 2.9 降到 2.2 eV），$J$、$J_c$ 都增大，说明布里渊区边界色散随降温而增强——这本身也是纯最近邻模型无法解释、需要引入环交换才能自洽描述的现象。
- 绝对散射强度经 $Z_c=1.18$ 量子修正后与 LSWT 预言一致，说明尽管 S=1/2 方晶格 AFM 量子涨落很强（亚晶格磁矩只剩经典值的 ~60%），LSWT（+1/S 修正）依然能在整个布里渊区内定量描述自旋波。

## 🔗 与我研究的关联

- 这是 `Tc-J关系论证调研计划.md` 第一阶段基线表（Table 1 / Fig. 5b 相关引用 77–107 号）里 cuprate J 值的标准来源，也是 [[J值实验与理论计算文献汇总]] 里"必引"的那一条。
- **关键提醒**：同一篇论文、同一组原始数据，按"经验 Heisenberg 模型"和"Hubbard 展开模型"两种假设拟合，能给出相差 ~25% 的 $J$ 值（104–112 vs 138–146 meV）。在做跨材料/跨体系的 $J$—$T_c$ 关系统计检验（调研计划里的问题 5：可复现性问题）时，必须先确认每篇被引文献报的 $J$ 是在哪种模型假设下拟合出来的，不能把不同假设下的数字直接放进同一张表比较。
- $J_c$（环交换）本身量级可观（~38–61 meV），如果调研计划后续要检验 Tc/J 约束里的"J"该用哪个交换能标，环交换是否应该单独计入或以某种有效组合计入，是需要跟踪的一个方法论问题。

## ❓ 问题与待深入理解

- 环交换 $J_c$ 的微观图像（Cu₄O₄ 四方格上的多体跃迁路径）具体怎么从 $t^4/U^3$ 阶微扰展开推导出来？
- 295 K → 10 K 降温后 $U$ 减小、$J$ 和 $J_c$ 增大的物理机制是什么？是热展缩改变了 Cu-O 键长/键角，还是别的效应？
- 这套"用 Hubbard 参数约束多交换常数"的拟合方法后来（YBCO、掺杂 cuprate 等）有没有被继续使用或修正？

---

> [!note]- 抓取信息
> 手动建卡，来源为与 Claude 的文献阅读讨论 + 用户补充的详细拟合数据。核对了 DOI（10.1103/PhysRevLett.86.5377，*PRL* 86 卷第 23 期，2001 年 6 月 4 日刊出）。
