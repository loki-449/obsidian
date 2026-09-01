---
tags: [计算方法, 分子动力学, AIMD, VASP]
created: 2026-07-13
---

# AIMD 计算与数据分析

> Ab Initio Molecular Dynamics（第一性原理分子动力学）：在 DFT 框架下对原子核做经典动力学演化，电子结构每一步自洽求解。

---

## 一、基本概念

### MSD（均方位移，Mean Square Displacement）

$$\text{MSD}_i(t) = \langle |\mathbf{r}_i(t) - \mathbf{r}_i(0)|^2 \rangle$$

$\mathbf{r}_i(t)$ 是原子 i 在时刻 t 的位置，$\mathbf{r}_i(0)$ 是参考初始位置。⟨·⟩ 表示对所有等效原子取平均。

- **固体（仅振动）**：MSD 随时间增大到一个平台值后不再增长——原子被"困"在晶格位置上
- **液体/扩散**：MSD 随时间线性增长，$\text{MSD}(t) \propto t$

扩散系数从 MSD 斜率得到：

$$D = \frac{1}{6} \lim_{t \to \infty} \frac{d}{dt} \text{MSD}(t)$$

### RMSD（均方根位移，Root Mean Square Displacement）

$$\text{RMSD} = \sqrt{\text{MSD}}$$

量纲是长度（Å），可以直接对照晶格常数、键长来感受原子跑了多远。

### MSD vs RMSD

| | MSD | RMSD |
|---|---|---|
| 量纲 | Å² | Å |
| 用途 | 扩散系数 D 正比于斜率 | 直观判断原子位移大小 |
| 物理本质 | 同一件事——原子偏离初始位置的幅度 | |

---

## 二、AIMD 可提取的分析量

### 2.1 结构稳定性

**总能量-时间曲线**

- 能量在小范围振荡不漂移 → 热力学平衡
- 持续单调下降 → 还在弛豫
- 突然跳变 → 结构相变或键断裂

**温度-时间曲线**

NVT 系综下温度应在设定值附近小幅波动。波动过大说明控温出了问题或体系不稳定。

### 2.2 氢扩散与迁移

**速度自相关函数（VACF）**

$$\text{VACF}(t) = \langle \mathbf{v}(t) \cdot \mathbf{v}(0) \rangle$$

傅里叶变换后得到**振动态密度（VDOS）**，可与声子谱的 PHDOS 对比：

- VDOS 峰位与 PHDOS 一致 → 简谐近似成立
- 偏离 → 非谐效应明显

**扩散系数 D 的两种算法**

| 方法 | 公式 | 说明 |
|------|------|------|
| MSD 斜率 | $D = \frac{1}{6} \frac{d}{dt}\text{MSD}$ | Einstein 关系 |
| VACF 积分 | $D = \frac{1}{3} \int_0^{\infty} \text{VACF}(t) dt$ | Green-Kubo 关系 |

两种方法结果一致 → 统计采样充分。

### 2.3 结构序参量

**径向分布函数 RDF（对关联函数 $g(r)$）**

$$g_{\alpha\beta}(r) = \frac{V}{4\pi r^2 N_\alpha N_\beta} \left\langle \sum_{i\in\alpha}\sum_{j\neq i\in\beta} \delta(r - |\mathbf{r}_i - \mathbf{r}_j|) \right\rangle$$

- 峰位置 → 特征键长
- 峰宽度 → 结构无序程度
- 峰随时间变宽/消失 → 键在断裂重组

**配位数**

从 RDF 第一个峰的积分得到：
$$N_c = 4\pi\rho \int_0^{r_{\text{min}}} r^2 g(r) dr$$

- H₂ 分子单元 → 配位数约 1
- 笼状 H₂₄ → 配位数约 4-5

### 2.4 相变识别

**B-factor（原子位移参数）**

高温下某些原子的 B-factor 突然大幅增加 → 熔化或预熔化信号。

**Lindemann 判据**

$$\frac{\sqrt{\langle u^2 \rangle}}{d_{\text{nn}}} \gtrsim 0.1$$

其中 $d_{\text{nn}}$ 是最近邻距离。比值超过约 10-15% → 晶体熔化。

**原子轨迹投影**

把选定原子的 xyz 坐标随时间变化画出来，肉眼判断是定点振动还是跨晶格扩散。比 MSD 直观但不够定量。

### 2.5 电子性质（需开启电子结构输出）

- **能隙随时间演化**：金属↔绝缘体转变的判据
- **Bader 电荷波动**：原子化学环境是否改变（扩散/成键/断键）

---

## 三、在氢化物研究中的标准使用流程

结构稳定性需同时满足三个判据：

1. **AIMD 能量不漂移**（热力学稳定）
2. **声子谱无虚频**（动力学稳定）
3. **H 原子的 MSD 不扩散**（氢不逃逸）

三者同时满足 → 该结构在该温压条件下稳定存在。

---

## 相关笔记

- [[PHONON计算流程]]
- [[DFT基础]]
- [[高压氢化物概述]]
