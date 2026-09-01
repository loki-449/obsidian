---
title: A₃XH₇ 氢化物超导体 ELF-λ 关联规律研究
tags: [课题规划, 氢化物超导, 主动学习, ELF, 高通量, A3XH7]
created: 2026-07-14
status: planning
---

# A₃XH₇ 氢化物超导体 ELF-λ 关联规律研究

> 基于高通量筛选 + 主动学习 + 跨家族验证，探究氢框架电荷离域程度与电声耦合强度的普适关联。

---

## 一、研究体系

**核心体系**：A₃XH₇ 三元氢化物（空间群 Pm-3m, No. 221）

- A 位：碱金属/碱土金属/稀土元素（Cs, Rb, K, Ba, La, Ac 等），大半径电子供体
- X 位：过渡金属或主族金属（In, Ga, Tl, Rh, Ir, Os 等），与 H 构建框架
- H：两种化学不等价 Wyckoff 位置 — 准 H₂ 分子单元中的 H + 体心孤立 H 原子

**关键结构特征**：
- 准 H₂ 分子单元 + In/X 元素形成氢合金框架
- 体心孤立 H 原子以离子键方式作用，调节 Fermi 面嵌套
- 高对称性 Pm-3m → ELF 谷底位置由对称性固定

**跨家族验证体系**：

| 家族 | 空间群 | H 配位特征 | 代表体系 | 数据状态 |
|------|--------|-----------|---------|---------|
| AXH₈ | Fm-3m | H₈ 笼 + 笼间弱共价连接 | AcRhH₈, CeOsH₈ 等 8 个 | λ 已收敛 ✓ |
| AXH₃ | Pm-3m | H-IIIA 层状框架 + 碱金属掺杂 | KGaH₃, CsInH₃, RbTlH₃ | 文献 λ 可用 |
| 笼形氢化物 | Fm-3m/Im-3m | H₂₄/H₂₉/H₃₂ 连续共价笼 | CaH₆, YH₆, LaH₁₀ | 文献 λ 可用 |

### 当前已完成数据

| 分析项目 | 状态 | 路径/工具 |
|---------|------|----------|
| ELFCAR (16 体系) | ✓ | `test/ELFCAR_TOT/` |
| ΔELFCAR (网格统一 60³, baseline=La₃AgH₇) | ✓ | `test/delta_ELFCAR_TOT/` (v2 文件) |
| ΔELF 热点提取 (5 热点 × 15 体系) | ✓ | `test/delta_ELFCAR_TOT/hotspot_summary.csv` |
| Origin 作图总表 (含键长+Bader) | ✓ | `test/delta_ELFCAR_TOT/for_origin_final.csv` |
| Bader H 拆分 (H-H vs H1b) | ✓ | `test/317/bader_H_split.csv` |
| Bader A/X 位点 | ✓ | `test/317/bader_large_radius.csv`, `bader_small_radius.csv` |
| 最近邻键长分析 | ✓ | `vasp/scripts/elf_analysis/bond_length.py` |
| ELF-Bader-键长关联分析 | ✓ | `vasp/scripts/elf_analysis/correlate_elf_bader.py` |
| 网格插值工具 | ✓ | `elf_analysis/elf_grid_interp.py` |
| 热点提取工具 | ✓ | `elf_analysis/elf_hotspot_extract.py` |
| COHP/ICOHP | ⚠️ | LOBSTER 待排查：基组(spilling ~30-89%) + k点修复中 |
| LOBSTER 诊断 | ⚠️ | 设计: `diag_lobster.py` (需先完成 §3 三处修正后全体系排查) |
| Bader 电荷 | ✓ | VASP Bader 全体系已跑，H 拆分完成 |
| L2 高精度 EPC | ✗ | 待选点 |
| Fermi 面嵌套 ξ(q) | ✗ | P2 |

### 关键发现 (ΔELF + Bader + 键长, 2026-07-17)

**趋势一致性**：
- **Cs 体系** ΔELF 波动最大：H2_mid ~ -0.69, H_isolated ~ +0.34
- **Ce/La 体系** ΔELF 最浅（|ΔELF| < 0.1）
- **Ba/Sr/Ca/Y 体系** 中间态

**电子分布规则 — 两条路径模型**：

A 位注入的电子经两条竞争路径到达氢框架：

1. **共价通道 A → X → H₂**：电子经 X 位中转注入准 H₂ 反键轨道 → H-H 键削弱 → 电荷离域
   - X 是"守门人"：X 为给体（Zn/Cu）→ 路径开通；X 为受体（Au/Pt）→ 截流
   - 关键证据：Cs₃AgH₇ → Cs₃AuH₇ 只换 X，ΔELF_X-H₂ 骤降 1.0，但 ΔELF_H-H 和 ΔELF_H₁b 几乎不变
2. **离子通道 A → H₁b**：A 位电子直接转移给体心孤立 H → H₁b 趋近 H⁻
   - 这条路径始终开放，不受 X 位调控

**A_e_dens 是统一的电子描述符**：
- A_e_dens = 3×A_dq / V_cell —— A 位注入的电子浓度（"电子化学压"）
- A_e_dens 封装了"注入多少电子"和"稀释到什么体积"两个独立维度
- A_e_dens vs ΔELF_H-H: r = +0.78 (p = 0.0007) —— 比单独用 A_dq (r=0.68) 或 a_lat (r=-0.81) 更干净

**预测**：
- A_e_dens 最大 → H₂ 最离域 → ΔELF_H-H ≈ 0 → 预测 λ 最大（Y₃CuH₇, Ca₃PdH₇）
- A_e_dens 最小 → H₂ 最共价 → ΔELF_H-H ≪ 0 → 预测 λ 最小（Cs₃AuH₇, Cs₃AgH₅）

---

## 二、核心物理问题与研究假设

### 2.1 核心假设

> **氢子晶格中 ELF 谷底值（ELF_min）——电荷离域化程度的直接量度——与电声耦合强度 λ 存在跨结构家族的稳健正相关关系。**

物理直觉链：
1. ELF 谷底处 Pauli 超额动能 D(r) 最小 → 同自旋电子对最不受 Pauli 排斥约束
2. 电荷离域程度高 → 电子云对原子位移扰动更敏感 → 更大的 ∂V_SCF/∂u
3. 更大的 ∂V_SCF/∂u → 更大的电声耦合矩阵元 |g|² → 更大的 λ

**但这不是严格推导，是唯象关联**。需要通过数据验证其适用范围和失效边界。

### 2.2 关键物理量定义

**(a) ELF（电子局域函数）**

$$\chi(\mathbf{r}) = \frac{D(\mathbf{r})}{D^0(\mathbf{r})}, \quad \text{ELF}(\mathbf{r}) = \frac{1}{1 + \chi^2(\mathbf{r})}$$

$$D(\mathbf{r}) = \tau(\mathbf{r}) - \frac{1}{8}\frac{|\nabla n(\mathbf{r})|^2}{n(\mathbf{r})}$$

$$D^0(\mathbf{r}) = \frac{3}{10}(3\pi^2)^{2/3} n(\mathbf{r})^{5/3}$$

$$\tau(\mathbf{r}) = \frac{1}{2}\sum_i f_i |\nabla\psi_i(\mathbf{r})|^2$$

- D(r)：实际体系的 Pauli 超额动能密度
- D⁰(r)：同密度均匀电子气的动能密度（参考态）
- χ = D/D⁰：Pauli 动能相对于均匀气的超额倍数
- ELF ∈ [0,1]：1 = 完全局域（共价键/芯电子），0.5 = 均匀电子气，<0.5 = 比均匀气更离域

ELF 已自带密度归一化——**跨体系直接可比，无需额外归一化**。

**(b) 电声耦合常数 λ**

$$\lambda = 2\int_0^\infty \frac{\alpha^2F(\omega)}{\omega}d\omega$$

$$\alpha^2F(\omega) = \frac{1}{N(E_F)}\sum_{\mathbf{k},\mathbf{q},\nu,m,n} |g_{\mathbf{k},\mathbf{q}\nu}^{mn}|^2 \delta(\omega - \omega_{\mathbf{q}\nu})\delta(\epsilon_{\mathbf{k}}^m)\delta(\epsilon_{\mathbf{k+q}}^n)$$

**(c) 电声耦合矩阵元**

$$g_{\mathbf{k},\mathbf{q}\nu}^{mn} = \left(\frac{\hbar}{2M\omega_{\mathbf{q}\nu}}\right)^{1/2} \langle\psi_{m,\mathbf{k}+\mathbf{q}}|\partial_{\mathbf{q}\nu}V_{SCF}|\psi_{n,\mathbf{k}}\rangle$$

- 依赖费米面附近的电子态 |ψ⟩ 对声子位移 ∂V_SCF/∂u 的响应
- 这是 ELF 与 λ 关联的**物理桥梁**——ELF 谷底处电荷离域 → 对 ∂V/∂u 敏感 → g 大

**(d) 超导转变温度（Eliashberg 方程）**

$$Z(i\omega_n) = 1 + \frac{\pi T}{\omega_n}\sum_m \lambda(i\omega_n - i\omega_m)\frac{\omega_m}{\sqrt{\omega_m^2 + \Delta^2(i\omega_m)}}$$

$$Z(i\omega_n)\Delta(i\omega_n) = \pi T\sum_m [\lambda(i\omega_n - i\omega_m) - \mu^*]\frac{\Delta(i\omega_m)}{\sqrt{\omega_m^2 + \Delta^2(i\omega_m)}}$$

**(e) McMillan 公式（近似解）**

$$T_c = \frac{\omega_{log}}{1.2}\exp\left[-\frac{1.04(1+\lambda)}{\lambda - \mu^*(1+0.62\lambda)}\right]$$

**(f) Fermi 面嵌套函数**

$$\xi(\mathbf{q}) = \sum_{\mathbf{k},m,n} \delta(\epsilon_{\mathbf{k}}^m)\delta(\epsilon_{\mathbf{k+q}}^n)$$

- 嵌套峰 → 特定 q 处大量电子态可以散射 → 声子软化 → λ 增强
- 这是 ELF 单描述符的**主要"漏报区"**——声子软化机制 ELF 无法捕获

---

## 三、研究方法

### 3.1 计算工作流

```
结构生成 → 低精度 QE (SCF + DFPT + EPC, 4×4×4 q)
    ↓
600 结构 → 声子稳定性筛选 → 60 动力学稳定
    ↓
全 60 体系：SCF (8×8×8 k) → ELFCAR → ELF 谷底提取
    ↓
L1 数据：60 个 (ELF_min, λ_low) 点 → GP 回归
    ↓
主动学习选 L2：6-8 个 → 高精度 QE (12×12×12 k, 6×6×6 q)
    ↓
L1→L2 标定 + 跨家族验证 (AXH₈ / AXH₃ / 笼形)
    ↓
失效边界探测 → 物理诊断 → 规律适用性结论
```

### 3.2 计算参数

| 层级      | k 网格     | q 网格  | 截断能    | μ*         |
| ------- | -------- | ----- | ------ | ---------- |
| L1（已完成） | ~8×8×8   | 4×4×4 | ~90 Ry | 0.10, 0.13 |
| L2（已完成） | 12×12×12 | 6×6×6 | 90 Ry  | 0.10, 0.15 |

### 3.3 ELF 特征提取方案

1. 从 VASP ELFCAR 读取三维 ELF 格点数据
2. H-mask：以每个 H 原子 Wigner-Seitz 半径（~1.2 Å）内格点取并集
3. 提取 ELF 分布的统计量：
   - ELF_min（绝对最小值）或 ELF_P1（最低 1% 均值，更稳健）
   - μ_ELF（氢子晶格 ELF 均值）——整体共价强度
   - σ_ELF（氢子晶格 ELF 标准差）——化学环境多样性
4. **不做 z-score 归一化**——ELF 本身已密度归一化，跨体系直接可比

### 3.4 主动学习框架

**身份定位**：校准器 + 边界探测器（非优化器，非分类器）

**目标**：
1. 用 GP 回归形式化 ELF_min → λ 的关联
2. 以最少 L2 计算完成 L1→L2 精度标定
3. 通过标准化残差分析探测规律的失效边界

**冷启动选点**（手动，覆盖 ELF 和化学多样性）：
- ELF_min 最大/最小的各 1 个
- L1 λ 最大/最小的各 1 个
- L1 回归残差最大的 2 个（检验离群点）
- A 位化学差异最大的 2 个（Cs→Ba→La 跨度）

**选点策略**（后续循环）：
- 最大化预测方差 σ²（GP 不确定性最大的区域）
- 停止条件：R² 变化 < 0.05 连续两轮，或已跑 ≥ 15 个 L2

**失效边界探测**：
- 训练 317-only GP → 喂入 AXH₈/AXH₃/笼形数据
- 标记"GP 低 σ 但预测偏差大"的体系 → 规律失效候选
- 逐一物理诊断：α²F 软化占比 / ξ(q) 嵌套峰 / X-d 轨道 DOS

---

## 四、研究目的与预期产出

### 4.1 核心发现

**ELF 谷底值是否可以作为氢化物超导体电声耦合强度的跨结构家族前置筛选描述符。**

### 4.2 预期产出

1. **主结果**：317 家族 60 个体系的 ELF_min-λ 关联曲线（L1 + L2 标定后）
2. **跨家族验证**：AXH₈ (8)、AXH₃ (3-4)、笼形 (3-4) 是否落在同一趋势线上
3. **失效模式分类**：

| 失效模式 | 物理原因 | 诊断方法 | 补救描述符 |
|---------|---------|---------|-----------|
| 声子软化 | Fermi 面嵌套驱动 | ξ(q) 峰值 | ξ(q_max) |
| d/f 轨道贡献 | X 的 d/f 带在 E_F 有显著 DOS | PDOS 分析 | N(Ef)_X/N(Ef)_H |
| 全对称 H | 无化学不等价 H → 无 ELF 谷 | Wyckoff 分析 | 描述符不适用 |

4. **方法贡献**：主动学习框架在有限计算预算下验证物性关联的范式

### 4.3 与已有工作形成闭环

- [[Du 等 - High-temperature Superconductivity in Perovskite H|钙钛矿 AXH₃]]：III A-H 框架 + 碱金属掺杂，ELF 谷底在 H-IIIA 层
- [[High-temperature superconductivity of thermodynamically stable fluorite-type hydrides at ambient pre|萤石 AXH₈]]：已建立 ELF_min-λ 线性关系 ELF = 0.073λ + 0.138（Adv. Sci. 2025）
- [[PhysRevB.111.224502|Cs-In-H (PRB 2025)]]：孤立 H 原子的 Fermi 面嵌套调控 → ELF 单描述符的"漏报"机制
- [[Huang 等 - 2024 - Superconductivity of thulium substituted clathrate|Tm 笼形氢化物]]：4f 电子 DOS vs H-s DOS → 只有 H 贡献参与超导

---

## 五、已有资源清单

### 5.1 已完成计算

| 内容 | 数量 | 精度 | 状态 |
|------|------|------|------|
| A₃XH₇ 结构搜索 (AIRSS + CASTEP) | 600 | - | ✓ |
| QE 结构优化 + SCF | 600 | 8×8×8 k, ~90 Ry | ✓ |
| DFPT 声子计算 | 600 | 4×4×4 q | ✓ |
| 低精度 EPC (α²F, λ_low, ω_log, Tc_McM) | 600 | 4×4×4 q, μ*=0.10 | ✓ |
| **QE band + PDOS（轨道投影）** | **600** | **8×8×8 k** | ✓ |
| AIMD 分子动力学 | 部分 | NVT, 不同温度点 | ✓ (MSD 可画) |
| VASP ELF (ELFCAR) | **0** | — | **待跑** |
| VASP COHP/ICOHP (LOBSTER) | **0** | — | **待跑** |
| VASP Bader 电荷 | **0** | — | **待跑** |
| 高精度 EPC (L2) | **0** | — | **待跑** |
| 动力学稳定结构 | **60 个** | — | ✓ |

### 5.2 已有文献/验证数据

| 家族 | 体系数 | λ 来源 | 状态 |
|------|--------|--------|------|
| AXH₈ 萤石 | 8 | 自己计算（已收敛） | ✓ 可用 |
| AXH₃ 钙钛矿 | ~5 | 文献 + 合作者计算 | 需确认 |
| 笼形氢化物 | ~4 | 文献值 | 需整理 |

### 5.3 工具链

- VASP：SCF + ELF 提取
- QE：声子 + EPC (ph.x + q2r.x + matdyn.x + lambda.x)
- Python：GP 回归 (scikit-learn)、ELF 格点分析、数据可视化
- 已有脚本库：`calculation/vasp/`、`calculation/AIMD/MSD&RMSD/`

---

## 六维分析框架：常规超导体系的系统分析角度

> 以下六维框架覆盖"力学稳定性→电子结构→结构信息→声子→超导性质→嵌套/软化"的完整分析链。每维度标注了已有数据状态（✓ 已有 / ⚡ 可提取 / ✗ 待补充）及可深挖的角度。

---

### 维度 1：力学稳定性（AIMD 分子动力学）

**标准问题**：该结构在该温压条件下能否稳定存在？

**已有**：AIMD 跑过，可画 MSD-t 和 MSD-T 曲线 ✓

**深挖角度**：

#### 1.1 H 扩散系数的 Arrhenius 拟合
$$D = \frac{1}{6}\lim_{t\to\infty}\frac{d}{dt}\text{MSD}(t)$$
$$D(T) = D_0 e^{-E_a/k_BT}$$

从 MSD 斜率提取各温度的 D，做 ln(D) vs 1/T → 活化能 E_a。**预测**：E_a 与 ELF 谷底值可能负相关——谷越深（ELF 越低）→ H 越离域 → 扩散能垒越低 → 越接近超离子态。

#### 1.2 Lindemann 判据定量化
$$\frac{\sqrt{\langle u^2\rangle}}{d_{nn}} \gtrsim 0.1 \Rightarrow \text{熔化}$$

标记各体系 Lindemann 比接近 0.1 的温度。不同 A 位元素对此温度的影响——检验"A 位提供化学预压缩"的最直接证据。

#### 1.3 VACF → VDOS vs PHDOS（非谐性度量）
- VDOS（来自 AIMD 速度自相关函数的傅里叶变换）vs PHDOS（来自 DFPT 简谐声子）
- 峰位偏移 → 非谐声子重整化强度
- **预测**：声子软化强的体系（λ_soft/λ_total 大），VDOS 与 PHDOS 偏离也大——可作为离群点诊断的独立指标

**需补充**：VACF 分析脚本、Arrhenius 拟合脚本

---

### 维度 2：电子结构信息

**标准问题**：费米面附近的电子态由谁贡献？化学键的本质是什么？

**已有**：

| 分析量 | 软件 | 状态 |
|--------|------|------|
| Band + PDOS（轨道投影） | QE | ✓ 600 体系 |
| COHP / ICOHP | LOBSTER | ✗ 待跑 |
| Bader 电荷 | VASP | ✗ 待跑 |
| ELF | VASP | ✗ 待跑 |

**深挖角度**：

#### 2.1 Bader 电荷的系统性趋势
- A 位 Bader 电荷 vs A 位电负性/离子半径 → 检验"碱金属为固定电子供体"在 317 中是否成立
- X 位 Bader 电荷 vs X 位电负性 → X-H 键的离子性/共价性调控
- H 的 Bader 电荷分类：准 H₂ 分子中的 H vs 体心孤立 H → 电荷差异是否随 A/X 变化

#### 2.2 COHP 积分与 ELF 谷底的共定位
- 在 ELF 谷底空间位置处，对应键的 -ICOHP 值
- ELF 低且 -ICOHP 小 → 弱键 = 电荷离域 → 自洽
- ELF 低但 -ICOHP 大 → 强键但电荷离域？→ 需要解释

#### 2.3 PDOS 中 H-s 贡献占比
$$f_{H\text{-}s} = \frac{N(E_F)_{H\text{-}s}}{N(E_F)_{total}}$$

- 你在 Tm 氢化物工作中已确认：只有 H-s 对超导有实质贡献
- f_H-s 作为 ELF_min 的**共生描述符**——两者从不同角度量度"H 电子参与超导的程度"
- ELF_min 测空间离域度，f_H-s 测能量窗口内的电子可用量

#### 2.4 Band 结构特征提取（与 Cs₃InH₇ PRB 对齐）
- **费米面方形网格**（由 In/X + 准 H₂ 的电子态构建）→ 是否 60 个体系都出现？
- **Γ 点低 Fermi 速度电子袋**→ 是否因孤立 H 的引入被压制？（Cs₃InH₆ vs Cs₃InH₇ 的核心差异）
- **平带/范霍夫奇点在费米面附近的存在**→ 与 FLat band → 高 DOS → 大 λ 的对应关系
- 提取量化指标：费米面附近 ±0.5 eV 内能带的平均色散宽度 ΔE_band → 越平 → 电子群速度越低 → 电声耦合窗口越大

#### 2.5 能带分解 ELF（选 2 个体系验证）
- 全占据 vs 费米面 ±1 eV 能带分解的 ELF 对比
- 检验"ELF 谷底由费米面附近电子主导（而非深能级）"——排除漏洞 A 的实际影响

---

### 维度 3：结构信息

**标准问题**：键长、键角、配位数如何随化学组分变化？

**已有**：POSCAR 结构数据（键长可提取）✓

**深挖角度**：

#### 3.1 H-H 键长分布的双峰分析
- 准 H₂ 分子单元内 H-H 键长（d1）vs 孤立 H 到最近邻准 H₂ 分子的距离（d2）
- 比值 r = d1/d2 → r 接近 1 → 两类 H 趋于等价 → ELF 分布窄 → 谷浅
- **可检验预测**：r 与 ELF_min 相关；r 与 σ_ELF 相关

#### 3.2 ELF 谷底空间坐标的跨体系恒定性
- Pm-3m 中 ELF 谷底出现在哪个高对称方向（[100]? [110]? [111]?）的哪个分数坐标？
- 60 个体系对比 → 恒定 → 群论约束成立 → 谷底由空间群 + Wyckoff 位置决定，与元素种类无关
- 若有漂移 → 元素化学影响谷底位置 → 需要解释

#### 3.3 弱共价连接网络的几何特征
- X-H 键长、H-H 连接距离与 ELF 谷底值的关联
- 晶格常数 a 的系统性趋势 vs A 位离子半径

**需补充**：批量键长提取脚本

---

### 维度 4：声子信息

**标准问题**：声子色散无虚频 → 动力学稳定；PHDOS + λ(q,ν) 投影 → 哪些模式主导耦合？

**已有**：L1 声子谱 + PHDOS + EPC 投影 ✓

**深挖角度**：

#### 4.1 λ(q,ν) 分解 → 主导耦合模式空间定位
L2 精度下选 2-3 个代表性体系，提取 λ 最大的声子支和 q 点。结合实空间 ELF 谷底位置——如果耦合最强的声子模式恰好是 ELF 谷底处 H 原子的位移模式 → 实空间-动量空间共定位的直接证据。

#### 4.2 声子软化贡献占比
$$\lambda_{soft} = 2\int_{\omega \in \text{softening region}} \frac{\alpha^2F(\omega)}{\omega}d\omega$$

定义软化区为 λ 累计增长最快的频率区间。λ_soft/λ_total > 0.5 → 声子软化主导 → ELF 单描述符可能低估 λ。

#### 4.3 ω_log 系统趋势
- ω_log ∼ sqrt(m⁻¹) → 主要受 H 质量控制，但结构刚性（键强度）也有贡献
- 317 家族内 ω_log 的方差 → 如果方差大 → 控制 ω_log 的因素需要独立分析
- ω_log 与晶格常数 a、与 A 位质量的散点图

#### 4.4 PHDOS 中 H 贡献占比
- H 在低频区（<200 cm⁻¹）的贡献 → A 位质量影响
- H 在中频区（600-1000 cm⁻¹）的贡献 → 准 H₂ 分子单元的剪切/旋转模式 → 软化区
- H 在高频区（>1000 cm⁻¹）的贡献 → H-H 伸缩 → 与 ELF 谷深的关系？

---

### 维度 5：超导性质

**标准问题**：Tc、ω_log、N(Ef) 的系统性趋势？ELF 预测 λ 后 λ→Tc 的转化效率？

**已有**：L1 λ_low, ω_log, Tc_McM, N(Ef)_total ✓

**深挖角度**：

#### 5.1 Tc 的 μ* 敏感性分析
$$\frac{\partial T_c}{\partial \mu^*} \text{ 在 } \lambda \approx 0.8-1.2 \text{ 区间最大}$$

（Allen-Dynes 公式分母 λ-μ*(1+0.62λ) → 0 时发散）
标记"μ* 敏感"体系 → 其 Tc 预测不确定性天然更大。

#### 5.2 N(Ef)_total vs N(Ef)_H-s vs λ 三角关系
- 含 f 电子体系（如 Ce, La 作 A 位）：N(Ef)_total 大但 N(Ef)_H-s 不一定大
- ELF 是全占据积分，不区分轨道成分 → 可能误判含 f 体系
- **这是你描述符的物理边界之一**——在论文中需要讨论

#### 5.3 Tc-λ 的跨家族对比
AXH₈(λ=1.5) 和 317(λ=1.5) → Tc 是否接近？
→ 如果不接近 → ω_log 差异 → 解释 ω_log 为什么随结构家族变化

#### 5.4 λ→Tc 的转化效率
定义 η = Tc / ω_log → 仅与 λ, μ* 有关（来自 Allen-Dynes 公式）

ELF 预测 λ → λ 通过 η 转化为 Tc。如果 η 在家族间差异大 → ELF→Tc 的直接预测会打折扣 → 需要多层模型。

---

### 维度 6：其他信息（嵌套、声子软化、超导机制补充诊断）

**标准问题**：Fermi 面拓扑是否驱动了特定 q 的声子软化？

**已有**：L1 数据中 PHDOS 软化区间接可见，但嵌套函数 ξ(q) 未算 ✗

**深挖角度**：

#### 6.1 Fermi 面嵌套函数 ξ(q)
$$\xi(\mathbf{q}) = \sum_{\mathbf{k},m,n} \delta(\epsilon_{\mathbf{k}}^m)\delta(\epsilon_{\mathbf{k+q}}^n)$$

选 3-4 个代表性体系（λ 最高/最低 + 残差最大的离群点）计算 ξ(q)。检验：
- "孤立 H 增强 R 点嵌套"是否在 317 家族中普适？（Cs₃InH₇ PRB 的核心发现）
- ξ(q_soft) 峰值与 λ_soft 的定量关系

#### 6.2 声子线宽 γ_qν
$$\gamma_{\mathbf{q}\nu} = 2\pi\omega_{\mathbf{q}\nu}\sum_{\mathbf{k},m,n}|g_{\mathbf{k},\mathbf{q}\nu}^{mn}|^2\delta(\epsilon_{\mathbf{k}}^m)\delta(\epsilon_{\mathbf{k+q}}^n)$$

γ ∝ |g|² × 嵌套强度。γ 的 q 空间分布（动量空间）与 ELF 谷底位置（实空间）的对偶关系——连接两个空间的桥梁。

#### 6.3 声子软化驱动 λ 的占比
λ_soft/λ_total > 0.5 的体系 → ELF 不捕获软化 → 系统偏差
→ 这些体系恰好是 GP 残差最大的 → 它们需要额外描述符（如 ξ(q_max) 或 γ_max）

#### 6.4 与 Cs₃InH₇ 的对齐验证
对你已发表的 Cs₃InH₇ 体系：QE band + PDOS 数据已有 → 提取 f_H-s, ΔE_band（费米面能带色散宽度）、ξ(q) 特征 → 作为"已知对照点"标定所有新分析方法的合理性和基准值。

---

### 六维分析框架总结：数据状态矩阵

| 维度      | 分析量                                       | 状态              | 优先级    |
| ------- | ----------------------------------------- | --------------- | ------ |
| 1. AIMD | MSD-T, D(T)→E_a, Lindemann, VDOS vs PHDOS | ⚡ 可提取           | P1     |
| 2. 电子结构 | Band+PDOS (QE)                            | ✓               | —      |
| 2. 电子结构 | ELF (VASP ELFCAR)                         | ✗               | **P0** |
| 2. 电子结构 | COHP/ICOHP (LOBSTER)                      | ✗               | P2     |
| 2. 电子结构 | Bader 电荷 (VASP)                           | ✗               | P2     |
| 2. 电子结构 | f_H-s = N(Ef)_H / N(Ef)_total             | ⚡ 可从 QE PDOS 提取 | P1     |
| 2. 电子结构 | ΔE_band（费米面能带平坦度）                         | ⚡ 可从 QE band 提取 | P1     |
| 2. 电子结构 | 能带分解 ELF（2 体系验证）                          | ✗               | P2     |
| 3. 结构   | H-H 键长双峰分布, 谷底空间坐标                        | ⚡ 可提取           | P1     |
| 4. 声子   | λ(q,ν) 分解, λ_soft/λ_total, ω_log 趋势       | ⚡ 可提取           | P1     |
| 5. 超导   | μ* 敏感性, Tc-λ 跨家族对比, η = Tc/ω_log          | ⚡ 可提取           | P1     |
| 6. 嵌套   | ξ(q), γ_qν, 软化占比, Cs₃InH₇ 对标              | ✗ 需算嵌套          | P1     |

> ✓ = 已跑完 | ⚡ = 数据已有可提取 | ✗ = 需补充计算
> P0 = 阻塞项（不跑后续分析无法进行）| P1 = 本周 | P2 = 可排队

### 6.1 立即执行（优先级最高）

- [ ] **全 60 个 317 体系的 VASP SCF + ELFCAR**
  - 参数：800 eV, 8×8×8 k, PBE, PAW
  - 输出：ELFCAR, DOSCAR, PROCAR
  - 预估：单体系 ~1-2 核时，总计 ~100 核时

- [ ] **ELF 谷底特征批量提取脚本**
  - 输入：ELFCAR + POSCAR（获取 H 原子坐标）
  - 输出：ELF_P1, ELF_P5, μ_ELF, σ_ELF, H Wyckoff 类型数
  - Python + pymatgen 或手写有限差分读取

- [ ] **GP 回归初探**
  - 60 个 (ELF_min, λ_low) 散点图
  - 线性回归 + GP 回归 (RBF kernel)
  - 留一交叉验证 R² + 标准化残差分析

### 6.2 L2 精度标定（选 6-8 个）

- [ ] **选点方案确定**（基于 L1 回归结果）
- [ ] **高精度 EPC 计算**
  - QE: 12×12×12 k, 6×6×6 q, μ*=0.10, 0.15
  - 输出：α²F(ω), λ, ω_log, Tc (McM + Eliashberg)

### 6.3 补充计算（增强论证）

- [ ] **frozen-phonon ΔELF 对比**（2 个体系）
  - 选 λ 最高和最低的 317 体系
  - 沿关键声子模式位移 ±0.05 Å
  - 对比静态 ELF 谷底 vs 位移后 ELF 变化

- [ ] **Fermi 面嵌套函数**（对 L1 残差最大的 2-3 个体系）
  - 确认离群机制是否为声子软化

### 6.4 跨家族验证

- [ ] **AXH₃ 3-4 个体系的 ELF 提取**
- [ ] **笼形氢化物 ELF 分布分析**（检验"H 全对称 → ELF 谷不存在"预测）
- [ ] **统一参数下 AXH₃ + 笼形 EPC 重算？**（若文献 λ 计算参数不一致）

### 6.5 论文撰写相关

- [ ] 主动学习框架的形式化描述（Methods 章节）
- [ ] 失效模式分类表 + 物理诊断流程图
- [ ] 化学空间覆盖矩阵（A × X 元素组合的已探索 vs 未探索区域）

---

## 六、待完成计算与数据分析清单（按 P0→P1→P2 优先级）

### P0 — 阻塞项

- [ ] **全 60 个 VASP SCF + ELFCAR**（ELF 数据源）
  - 800 eV, 8×8×8 k, PBE, PAW, LELF=.TRUE.
  - 单体系 ~2-4 核时，总计 ~150-250 核时

- [ ] **ELF 谷底特征批量提取脚本**
  - ELFCAR + POSCAR → ELF_P1, ELF_P5, μ_ELF, σ_ELF

### P1 — 本周：从已有 L1 数据中直接提取

- [ ] **GP 回归初探**：60 点 ELF_min vs λ_low，交叉验证 R²，标准化残差
- [ ] **f_H-s 提取**（QE PDOS）：N(Ef)_H-s / N(Ef)_total
- [ ] **ΔE_band 提取**（QE band）：费米面附近能带平坦度
- [ ] **Band 特征对标**（与 Cs₃InH₇ PRB）：方形 Fermi 面网格 / Γ 点电子袋 / 范霍夫奇点
- [ ] **AIMD 分析**：MSD→D(T)→E_a, Lindemann 比, VDOS vs PHDOS（选 2 体系）
- [ ] **结构提取**：H-H 双峰键长 (d1/d2), 谷底坐标恒定性, a vs r_A
- [ ] **声子提取**（选 5-8 体系）：λ(q,ν) 分解, λ_soft/λ_total, ω_log 趋势
- [ ] **L2 选点方案**：GP 残差 + σ + 化学多样性 → 6-8 个候选
- [ ] **Cs₃InH₇ 对标**：提取 f_H-s, ΔE_band, ξ(q) 基准值

### P2 — 补充计算

- [ ] **L2 高精度 EPC**（选定的 6-8 个）：12×12×12 k, 6×6×6 q, μ*=0.10/0.15, Eliashberg 自洽
- [ ] **COHP/ICOHP**（选 5-8 个，LOBSTER）：ELF 谷底处 -ICOHP 提取
- [ ] **Bader 电荷**（全 60 个可批量）：A 位电荷转移系统性趋势
- [ ] **frozen-phonon ΔELF**（选 2 个体系）：静态谷底 vs 位移后 ELF 共定位验证
- [ ] **Fermi 面嵌套 ξ(q)**（残差最大 2-3 个 + λ 最高 2 个）：离群机制确认
- [ ] **能带分解 ELF**（选 2 个）：全占据 vs E_F±1eV → 关闭漏洞 A

### 跨家族验证（P1）

- [ ] AXH₃ 3-4 个 + 笼形 3-4 个 ELF 提取
- [ ] 笼形：检验"H 全对称 → ELF 谷不存在"
- [ ] 文献 λ 参数一致性检查，不一致则重算

### 论文撰写（P1 启动，贯穿全程）

- [ ] Methods: GP 主动学习框架形式化描述
- [ ] Results: 六维框架图、ELF-λ 主散点图、残差诊断图、跨家族验证对比图
- [ ] Discussion: 失效模式分类表 + 物理诊断流程图 + 化学空间覆盖矩阵

---

## 七、理论公式汇总

### 核心定义
- ELF 定义：[[Eliashberg 方程]]（已有笔记）
- λ 定义：`λ = 2∫ α²F(ω)/ω dω`

### 超导理论
- Eliashberg 方程（强耦合，Matsubara 域）
- McMillan 公式（弱-中耦合近似）
- Allen-Dynes 修正公式（含 f1, f2 修正因子）

### Fermi 面分析
- 嵌套函数 ξ(q)
- 费米速度 v_F(k) = ∇_k ε(k)
- 态密度 N(E_F) = ∑_k δ(ε_k - E_F)

### 已有笔记链接
- [[Eliashberg方程]]
- [[麦克米兰方程]]
- [[McMillan与Hill极限]]
- [[声子机制]]
- [[BCS理论]]
- [[高压氢化物概述]]
- [[化学预压缩机制]]
- [[EPW计算]]

---

## 八、论文预期结构（六维框架组织版）

1. **Introduction**
   - 氢化物超导高通量筛选现状
   - 现有筛选指标（N(Ef)、λ、Tc）的不足 → 需要一个仅需 SCF 成本的前置描述符
   - ELF 作为电荷离域程度自然量度的动机
   - 本文目标：在 A₃XH₇ + AXH₈ + AXH₃ + 笼形四家族中系统检验 ELF 谷底-λ 关联

2. **Methods**
   - 2.1 计算参数：L1 (4×4×4 q, ~90 Ry) → L2 (6×6×6 q, 90 Ry) → 跨家族
   - 2.2 ELF 特征提取方案（H-mask + P1/P5 分位数）
   - 2.3 GP 主动学习框架：身份定义（校准器+边界探测器）、选点策略、停止条件

3. **Results — 按六维框架组织**

   - **3.1 结构稳定性与力学性质（维度 1+3）**
     - AIMD: MSD-T, H 扩散 Arrhenius, Lindemann 判据, VDOS vs PHDOS
     - 结构: H-H 双峰键长、ELF 谷底空间坐标恒定性（群论约束验证）

   - **3.2 电子结构系统分析（维度 2）**
     - Band+PDOS: Fermi 面主要由 In/X + 准 H₂ 贡献（与 Cs₃InH₇ PRB 对齐）
     - ELF 三维分布: 谷底识别 + 跨体系比较
     - COHP/ICOHP: 谷底处弱共价键的定量确认
     - Bader: A 位电荷转移系统性趋势
     - f_H-s = N(Ef)_H-s/N(Ef)_total 提取与趋势

   - **3.3 ELF-λ 关联规律（维度 4+5，核心结果）**
     - L1 60 体系 ELF_min vs λ_low 散点图 + GP 回归
     - 多描述符比较：ELF_P1 vs f_H-s vs ΔE_band → 哪个与 λ 相关最显著
     - L1→L2 标定：选 6-8 个，GP 主动学习选点
     - 残留不确定性来源分析

   - **3.4 跨家族验证（维度 4+5）**
     - AXH₈ (8): ELF = 0.073λ + 0.138 在 317 数据上是否复现？
     - AXH₃ (3-4): 是否落在同一趋势线？
     - 笼形氢化物 (3-4): ELF 分布窄 → 描述符天然失效的化学解释

   - **3.5 失效边界与物理诊断（维度 6）**
     - GP 标准化残差 → 异常点标记
     - 诊断菜单：ξ(q) 嵌套、λ_soft/λ_total、f_H-s 异常、d/f 轨道污染
     - 失效模式分类表
     - frozen-phonon ΔELF 验证：静态谷底 = 动态电声耦合活跃区

4. **Discussion**
   - ELF 谷底描述符的化学适用范围："H 存在至少两种化学不等价 Wyckoff 位置"
   - 主动学习框架在物性关联验证中的方法论意义
   - 与已有工作（AXH₈ 线性、Cs₃InH₇ 嵌套、Tm 4f-EC 解耦）的闭环
   - 高通量筛选的实用建议：SCF+ELF 前置筛选 → EPC 验证选点策略

5. **Conclusion**
   - ELF_min ↔ λ 跨家族关联成立，适用范围明确
   - 主动学习有效校准 L1→L2，为有限预算下高通量筛选提供新范式
   - 未来方向：三元以上体系、含 d/f 成键体系、向 Tc 预测的延伸

---

## 九、后续工作的对话范式

> 以下为与本对话联动的工作协议，供后续 session 参考：

### 计算请求范式

当需要部署新计算时，提供以下信息：
1. 体系名（如 Cs3InH7）、空间群
2. 计算类型（SCF / ELF / EPC-L1 / EPC-L2 / frozen-phonon）
3. 优先级（P0-立即 / P1-本周 / P2-可排队）
4. 参数覆盖（若偏离标准参数需注明）

### 分析请求范式

当需要分析已有数据时，提供以下信息：
1. 数据集范围（全 60 个 / 指定子集 / 某个家族）
2. 分析目标（关联分析 / 残差诊断 / 跨家族对比）
3. 输出格式（散点图 / 统计表 / 回归报告）

### 标准计算模板

**SCF (VASP)**:
```
ENCUT = 800, KSPACING = 0.03, PBE, PAW
LELF = .TRUE.
```

**EPC-L1 (QE, 已完成)**:
```
ph.x: ldisp=.true., nq1=4, nq2=4, nq3=4
electron_phonon='interpolated'
```

**EPC-L2 (QE, 待跑)**:
```
ph.x: ldisp=.true., nq1=6, nq2=6, nq3=6
electron_phonon='interpolated'
el_ph_nsigma=10, el_ph_sigma=0.005
lambda.x: μ*=0.10, 0.15
```

---

## 相关笔记

- [[氢化物超导MOC]]
- [[理论计算MOC]]
- [[../00_MOC/超导总地图|超导总地图]]
- 已有工作 PDF：`E:\claude_work\science_chat\08_我的相关工作\`
