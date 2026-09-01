---
tags:
  - superconductivity
  - magnetic-exchange
  - J-value
  - Tc
  - literature-survey
  - experimental-measurement
  - theoretical-calculation
date: 2026-08-03
aliases:
  - J值实验与理论计算文献汇总
  - J-Tc参考文献
---

# 磁交换耦合 J 值：实验测量与理论计算文献汇总

> 按体系分类，每条标注测量手段或计算方法、可信度、在 J-Tc 调研中的用途。

---

## 一、铜氧化物 — J 值黄金标准（INS + RIXS + Raman 三重互洽）

### 1.1 La₂CuO₄

**实验测量**

| 文献                       | 期刊                             | 方法              | J 值             | 备注                      | 笔记                   |
| :----------------------- | :----------------------------- | :-------------- | :-------------- | :---------------------- | -------------------- |
| Coldea et al. (2001)     | *Phys. Rev. Lett.* 86, 5377    | INS 自旋波色散       | J ≈ 120–138 meV | **cuprate J 值的标准引用，必引** | [[2026年08月31日 研究日志]] |
| Hayden et al. (1991)     | *Phys. Rev. Lett.* 67, 3622    | INS             | J ≈ 130 meV     | 更早的 INS 基准              |                      |
| Braicovich et al. (2009) | *Phys. Rev. Lett.* 102, 167401 | Cu L₃-edge RIXS | J ≈ 120–140 meV | RIXS 与 INS 互洽，薄膜友好的替代方案 |                      |
| Le Tacon et al. (2011)   | *Nature Physics* 7, 725        | RIXS 顺磁激发       | 掺杂 cuprate 磁涨落  | 证明磁涨落存活到超导态             |                      |

**理论计算（DFT+DMFT / 模型计算）**

| 文献                               | 期刊                                   | 方法          | 用途             |
| :------------------------------- | :----------------------------------- | :---------- | :------------- |
| Katsnelson & Lichtenstein (2004) | *J. Phys.: Condens. Matter* 16, R755 | DFT+DMFT 综述 | cuprate J 计算框架 |
| Werner et al. (2009)             | *Phys. Rev. B* 79, 220503            | DFT+DMFT    | 与实验 J 值互洽      |
| Ogata & Fukuyama (2008)          | *Rep. Prog. Phys.* 71, 036501        | t-J 模型综述    | J 驱动配对的理论基础    |

### 1.2 YBa₂Cu₃O₆₊ₓ (YBCO)

**实验测量**

| 文献 | 期刊 | 方法 | J 值 | 备注 |
|:---|:---|:---|:---|:---|
| Hayden et al. (1996) | *Phys. Rev. Lett.* 76, 1344 | INS 自旋波 | J ≈ 120–150 meV | 双分子层 cuprate |
| Reznik et al. (1996) | *Phys. Rev. B* 53, R14741 | INS | — | — |
| Sugai et al. (1990) | *Phys. Rev. B* 42, 1045 | Raman 双磁子 | J ≈ 120 meV | — |

### 1.3 Bi₂Sr₂CaCu₂O₈₊ₓ (Bi2212)

**实验测量**

| 文献 | 期刊 | 方法 | 备注 |
|:---|:---|:---|:---|
| Fong et al. (1999) | *Phys. Rev. Lett.* 82, 1939 | INS | J 值与 La₂CuO₄ 相近 |
| Dean et al. (2013) | *Nature Materials* 12, 1019 | RIXS | 顺磁激发，超导态下仍存在 |

### 1.4 cuprate 关键综述

| 文献 | 期刊 | 用途 |
|:---|:---|:---|
| **Scalapino (2012)** | ***Rev. Mod. Phys.* 84, 1383** | **自旋涨落配对理论奠基综述，必读** |
| Keimer et al. (2015) | *Nature* 518, 179 | cuprate 超导全面综述 |

---

## 二、铁基超导体 — J₁–J₂ 阻挫体系（INS + RIXS）

### 2.1 BaFe₂As₂ (122 母体)

**实验测量**

| 文献 | 期刊 | 方法 | J 值 | 备注 |
|:---|:---|:---|:---|:---|
| Harriger et al. (2011) | *Phys. Rev. B* 84, 054544 | INS 全布里渊区自旋波 | J₁ ~ 30–60 meV, J₂ ~ 15–25 meV | **Ba122 J 值标准引用** |
| Ewings et al. (2011) | *Phys. Rev. B* 83, 214519 | INS | 类似 | SrFe₂As₂ 对比 |
| Diallo et al. (2009) | *Phys. Rev. Lett.* 102, 187206 | INS | — | 高能自旋激发 |

**理论计算**

| 文献 | 期刊 | 方法 | 用途 |
|:---|:---|:---|:---|
| Yin, Pickett & Ku (2011) | *Phys. Rev. B* 84, 014529 | DFT 拟合 INS | 与实验 J₁, J₂ 互洽 |
| Mazin & Johannes (2009) | *Nature Physics* 5, 141 | DFT | J₁–J₂ 阻挫模型提出 |

### 2.2 FeSe (11 体系)

**实验测量**

| 文献 | 期刊 | 方法 | J 值 | 备注 |
|:---|:---|:---|:---|:---|
| Wang et al. (2016) | *Nature Materials* 15, 159 | INS | J₁ ~ 30–40 meV, J₂ ~ 20–30 meV | **向列相以上和以下均测量，FeSe 标准引用** |

**理论计算**

| 文献 | 期刊 | 方法 | 用途 |
|:---|:---|:---|:---|
| Kreisel et al. (2017) | *Phys. Rev. B* 95, 174504 | 自旋涨落 Eliashberg | FeSe 及其他铁基配对理论 |
| Luo et al. (2010) | *Phys. Rev. B* 82, 104508 | DFT | 铁基超导交换耦合系统比较 |

### 2.3 铁基关键综述

| 文献 | 期刊 | 用途 |
|:---|:---|:---|
| **Dai (2015)** | ***Rev. Mod. Phys.* 87, 855** | **铁基 INS 磁激发综述，最重要的铁基 J 值实验文献** |
| Stewart (2011) | *Rev. Mod. Phys.* 83, 1589 | 铁基超导全面综述 |

---

## 三、镍基超导体 — J 值前沿（INS 仅 327，其余全依赖计算）

### 3.1 La₃Ni₂O₇₋δ (327) — 唯一有直接 INS 测量的镍基体系

**实验测量**

| 文献 | 期刊 | 方法 | J 值 | 备注 |
|:---|:---|:---|:---|:---|
| **Xie et al. (2024)** | ***Science Bulletin* 69, 3221** | **INS（粉末）** | **J⊥ ~ 60–100 meV** | **全球首例 La₃Ni₂O₇₋δ INS 测量，镍基唯一直接 J 实验值，必引** |

**理论计算**

| 文献 | 期刊 | 方法 | 用途 | 优先级 |
|:---|:---|:---|:---|:---:|
| **Qu et al. (2024)** | ***Phys. Rev. Lett.* 132, 036502** | **bilayer t-J-J⊥ 模型** | **层间磁交换+配对理论框架，核心理论文献** | ★★★★★ |
| Bötzel & Lechermann (2024) | *Phys. Rev. X* 14, 041023 | DFT+DMFT | 多层磁激发谱，与 Xie INS 互洽 | ★★★★★ |
| Yang et al. (2024) | *Phys. Rev. B* 109, L241106 | DFT+DMFT | 327 电子结构 | ★★★★ |
| Luo et al. (2024) | *Phys. Rev. B* 110, 045145 | RPA | 磁激发谱计算 | ★★★ |
| Lu et al. (2024) | *Chin. Phys. Lett.* 41, 057403 | t-J Gutzwiller | 磁和超导性质 | ★★★ |
| Fan et al. (2024) | *Phys. Rev. B* 110, 024514 | 双层 Hubbard/双轨道模型 | 层间配对机制 | ★★★ |

### 3.2 NdNiO₂ / PrNiO₂ (112) — J 完全依赖理论计算

**实验测量**（RIXS，信号弱、有争议）

| 文献 | 期刊 | 方法 | 备注 |
|:---|:---|:---|:---|
| Lu et al. (2021) | *Science* 373, 213 | RIXS | NdNiO₂ 薄膜磁激发，唯一接近 112 磁激发测量的实验，争议未消 |

**理论计算**

| 文献 | 期刊 | 方法 | J 值 | 备注 |
|:---|:---|:---|:---|:---|
| **Chen et al. (2022)** | ***Phys. Rev. B* 106, 045105** | **DFT+DMFT** | **J ~ 30–60 meV** | **112 的 J 值来源，调研中必定引用** |
| Kitatani et al. (2020) | *Phys. Rev. B* 102, 060504(R) | DFT+DMFT | — | 母体磁性和 J |
| Karp et al. (2020) | *Phys. Rev. B* 101, 081106(R) | DFT | — | 无限层镍氧化物磁交换 |
| Si et al. (2021) | *Phys. Rev. Lett.* 126, 196402 | DFT+DMFT | — | 多带描述，d_z² 与 5d 杂化 |

### 3.3 La₄Ni₃O₁₀ (4310) — J 完全未知

| 文献 | 期刊 | 内容 | 备注 |
|:---|:---|:---|:---|
| **Zhu et al. (2024)** | ***Nature* 631, 531** | **超导发现** | 高压单晶 Tc ~ 20–30 K，无磁激发数据 |
| Li, Guan et al. (2025) | *Phys. Rev. X* 15, 021005 | 高压下单晶结构测定 | — |
| Peng et al. (2025) | arXiv:2502.14410 | 各向同性超导 | 上临界场测量 |

> ⚠️ **研究空白**：La₄Ni₃O₁₀ 没有任何磁激发测量（INS 或 RIXS），也没有专门计算 J 的理论工作。如果你博导组能填补这个空白，将是该体系的首次。

### 3.4 镍基关键综述

| 文献 | 期刊 | 用途 |
|:---|:---|:---|
| Nature Reviews Physics (2025) | *Nat. Rev. Phys.* | infinite-layer + RP 镍氧化物综述 |
| [NSR, 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12512173/) | *Natl. Sci. Rev.* | 中国科学家镍基超导系统综述 |

---

## 四、t-J 模型与 Tc/J 上界 — 直接决定你调研的理论基础

### 4.1 有限温 DMRG / 张量网络

| 文献 | 期刊 | 方法 | 核心结论 | 优先级 |
|:---|:---|:---|:---|:---:|
| **Qu et al. (2025)** | ***PNAS* 122, e2420963122** | **有限温 DMRG** | **正方格子 t-J 模型 d 波超导全局相图，Tc/J ≈ 0.04–0.06** | ★★★★★ |
| Jiang & Devereaux (2019) | *Science* 365, 1424 | DMRG | Tc/J 上界的存在 | ★★★★★ |

### 4.2 约束路径蒙特卡洛 (CPMC) + 最大熵

| 文献 | 期刊 | 方法 | 核心结论 | 优先级 |
|:---|:---|:---|:---|:---:|
| **Qin et al. (2025)** | ***npj Quantum Materials* 10, 13** | **CPMC + 最大熵** | **Tc/J ≤ 0.04–0.07 的内在约束，严格数值论证** | ★★★★★ |

### 4.3 Eliashberg 框架

| 文献 | 期刊 | 核心内容 |
|:---|:---|:---|
| **Scalapino (2012)** | ***Rev. Mod. Phys.* 84, 1383** | 自旋涨落 Eliashberg，推 Tc ≈ 0.1 J |
| Mai et al. (2021) | *Phys. Rev. X* 11, 011026 | DCA+Eliashberg，系统比较各种理论的 Tc 预测精度 |

---

## 五、重费米子 — RKKY/T_K 替代 J 的等效标度

| 文献 | 期刊 | 内容 | 备注 |
|:---|:---|:---|:---|
| Stock et al. (2012) | *Phys. Rev. Lett.* 109, 167207 | CeCoIn₅ 超导态自旋共振 INS | J 等效值 ~ 2–5 meV |
| Mathur et al. (1998) | *Nature* 394, 39 | CeRhIn₅ / CeCoIn₅ 磁序与超导 | Doniach 相图 |
| Coleman (2007) | *Handbook of Magnetism* | Doniach 相图 + RKKY-Kondo 竞争 | 标准理论参考 |
| Aynajian et al. (2012) | *Nature* 486, 201 | CeCoIn₅ 中 QCP 附近的自旋涨落 STM | — |

---

## 六、其他有 J 值的小体系（可选纳入）

| 文献 | 期刊 | 材料 | 方法 | J 值 |
|:---|:---|:---|:---|:---|
| Braden et al. (2002) | *Phys. Rev. B* 65, 214510 | Sr₂RuO₄ | INS | J ≈ 40 meV |
| Powell & McKenzie (2011) | *Rep. Prog. Phys.* 74, 056501 | κ-(BEDT-TTF)₂X | NMR / 综述 | J ~ 20–40 meV |

---

## 七、跨体系标度律相关综述

| 文献 | 期刊 | 核心内容 |
|:---|:---|:---|
| **Uemura et al. (1989)** | ***Phys. Rev. Lett.* 62, 2317** | **Tc 与超流密度的 Uemura 标度——第一个跨体系标度律** |
| Uemura et al. (1991) | *Phys. Rev. Lett.* 66, 2665 | 扩展版 Uemura 标度 |
| Lee, Nagaosa & Wen (2006) | *Rev. Mod. Phys.* 78, 17 | 铜氧化物理论综述 |
| Hirschfeld et al. (2011) | *Rep. Prog. Phys.* 74, 124508 | 铁基能隙结构和配对对称性 |

---

## 八、计算方法对比 — 为你的调研选择合适算法

### A. DFT+DMFT（最推荐）

- **能做**：晶体结构 → 轨道分辨 χ(q, ω) → 海森堡 J
- **优点**：与材料直接对应、与 INS/Raman 实验可对比、成熟度高
- **缺点**：计算成本中等，需要 DMFT 自洽经验
- **适合材料**：镍基 327/4310/112、铜氧化物、铁基
- **代码**：Wien2k+DMFT(w2dynamics)、VASP+DMFT(TRIQS/solid_dmft)
- **文献**：Chen et al. (2022) 已对 NdNiO₂ 走完全流程
- **空白**：La₄Ni₃O₁₀ 尚未有 DFT+DMFT J 计算 → **首创机会**

### B. t-J/Hubbard 模型 + DMRG/CPMC

- **能做**：从 t, U/J 出发 → 算全量子力学 Tc/J 最大允许值
- **优点**：数值严格、不受平均场近似的限制、可直接验证 Tc/J 上界
- **缺点**：不直接对应具体材料参数、需要模型化
- **代码**：ITensor(DMRG)、ALF(CPMC)
- **文献**：Qu et al. (2025, PNAS)、Qin et al. (2025, npj QM)

### C. Eliashberg 方程

- **能做**：给定 χ(q, ω)（来自 A 或实验）→ 自洽解 Δ 和 Tc
- **优点**：直接计算 Tc、可对比实验
- **缺点**：多轨道 Eliashberg 复杂度高、对联价能隙对称性假设敏感
- **文献**：Scalapino (2012, RMP)

### D. 纯 DFT（不推荐）

- **缺点**：低估关联效应，J 值显著偏离实验。不适合 Mott 体系。

---

## 九、三条核心引用链 — 论文逻辑骨架

### 线 1：实验 J 值链

```
La₂CuO₄: Coldea PRL 2001
  → BaFe₂As₂: Harriger PRB 2011
  → FeSe: Wang Nature Materials 2016
  → La₃Ni₂O₇: Xie Science Bulletin 2024（镍基唯一 INS）
  → NdNiO₂: Chen PRB 2022（计算值，非实验）
```

### 线 2：Tc/J 理论约束链

```
Scalapino RMP 2012（Eliashberg 框架）
  → Jiang Science 2019（DMRG Tc/J 上界）
  → Qu PNAS 2025（有限温 DMRG 全局相图）
  → Qin npj QM 2025（Tc/J ≤ 0.04–0.07）
```

### 线 3：镍基特化理论链

```
Qu PRL 2024（bilayer t-J-J⊥ 模型）
  → Bötzel PRX 2024（DFT+DMFT 磁激发）
  → Yang PRB 2024（DFT+DMFT 电子结构）
  → 你的工作：新 J 数据 × 理论约束 → 填充 J-Tc 相图空白点
```

---

## 十、按可信度分层的材料清单

| 层级 | 材料 | J 值来源 | 可信度 | 调研中的用途 |
|:---|:---|:---|:---:|:---|
| **L1** | La₂CuO₄ | INS+RIXS+Raman | ★★★★★ | 铜氧化物锚点 |
| **L1** | YBCO | INS+Raman | ★★★★★ | 铜氧化物验证 |
| **L1** | Bi2212 | INS+RIXS | ★★★★★ | 铜氧化物验证 |
| **L1** | BaFe₂As₂ | INS | ★★★★ | 铁基锚点 |
| **L1** | FeSe | INS | ★★★★ | 铁基锚点 |
| **L1** | La₃Ni₂O₇₋δ | INS（粉末） | ★★★★ | 镍基唯一实验 J |
| **L1** | Sr₂RuO₄ | INS | ★★★★ | 奇异对比点 |
| **L1** | CeCoIn₅ | INS | ★★★★ | 重费米子锚点 |
| **L2** | Nd₀.₈Sr₀.₂NiO₂ | DFT+DMFT 反推 | ★★ | 112 参考值 |
| **L2** | La₄Ni₃O₁₀ | 无 | ☆ | 空白，标注 only |
| **L2** | FeSe/SrTiO₃ 单层 | DFT 反推 | ★★ | 参考 |
| **L3** | Hg1223 | 外推 | ★ | Cu Tc 最高但无 J 测量 |

---

*创建时间：2026-08-03*
*关联笔记：[[J值与Tc关系跨体系调研]] | [[镍基超导四大体系调研]] | [[La3Ni2O7-层间层内电子对比分析]]*
