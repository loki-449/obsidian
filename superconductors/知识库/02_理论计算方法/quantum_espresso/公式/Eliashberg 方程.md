Eliashberg 方程是强耦合超导理论的基石。不同于 BCS 理论中的常数相互作用近似，Eliashberg 理论通过格林函数方法（Green's Function Formalism）考虑了电子-声子相互作用的动力学过程（即相互作用具有频率依赖性）。

### 1. Eliashberg 方程的核心物理量

在 Matsubara 频率（虚频）域 $\omega_n = (2n+1)\pi T$ 下，系统的物理状态由两个自能（Self-energy）函数描述：

- **$\chi(i\omega_n)$**：能量重整化函数（涉及电子有效质量的修正）。
    
- **$\phi(i\omega_n)$**：超导配对函数（即能隙函数的分子部分）。
    

由此定义归一化能隙函数为：$\Delta(i\omega_n) = \frac{\phi(i\omega_n)}{Z(i\omega_n)}$，其中 $Z(i\omega_n) = 1 - \frac{\chi(i\omega_n)}{i\omega_n}$ 是准粒子波函数重整化因子。

### 2. Eliashberg 方程组

对于各向同性超导体，方程组如下：

#### A. 能量重整化方程

$$[1 - Z(i\omega_n)]\omega_n = \pi T \sum_{m} \lambda(i\omega_n - i\omega_m) \frac{\omega_m}{\sqrt{\omega_m^2 + \Delta^2(i\omega_m)}}$$

#### B. 能隙方程

$$Z(i\omega_n)\Delta(i\omega_n) = \pi T \sum_{m} \left[ \lambda(i\omega_n - i\omega_m) - \mu^* \right] \frac{\Delta(i\omega_m)}{\sqrt{\omega_m^2 + \Delta^2(i\omega_m)}}$$

- **$\lambda(\Omega)$**：电子-声子谱函数 $\alpha^2F(\Omega)$ 的相互作用核，定义为：
    
    $$\lambda(i\omega_n - i\omega_m) = 2 \int_{0}^{\infty} d\Omega \frac{\Omega \alpha^2F(\Omega)}{\Omega^2 + (\omega_n - \omega_m)^2}$$
    
- **$\mu^*$**：库仑赝势（Coulomb pseudopotential），用于修正电子间的直接库仑排斥。
    

### 3. 方程的物理内涵

1. **动力学修整：** 与 BCS 理论中的常数能隙不同，这里的 $\Delta(i\omega_n)$ 是频率的函数。这意味着超导配对的强度随能量变化，反映了声子作为媒介的物理时间延迟。
    
2. **准粒子阻尼：** $Z(i\omega_n)$ 描述了电子在传播过程中因被声子散射而形成的“虚云”，这增加了电子的有效质量 $m^* = m(1+\lambda)$。
    
3. **自洽求解：** 这是一组非线性积分方程组。通常从一个初始能隙 $\Delta$ 开始，通过数值迭代求解直到函数不再变化，从而得到临界温度 $T_c$ 和能隙 $\Delta(\omega)$。
    

### 4. McMillan 公式 (近似解)

为了在不进行复杂数值计算的情况下估算 $T_c$，人们常使用 McMillan 提出的公式（基于对 Eliashberg 方程的近似拟合）：

$$T_c = \frac{\Theta_D}{1.45} \exp\left[ - \frac{1.04(1+\lambda)}{\lambda - \mu^*(1+0.62\lambda)} \right]$$

其中：

- $\lambda = 2 \int \frac{\alpha^2F(\Omega)}{\Omega} d\Omega$ 是电子-声子耦合常数。
    
- $\Theta_D$ 是德拜温度。
    

### 总结

Eliashberg 方程不仅仅是求 $T_c$ 的工具，它是**将强关联（电子-声子强耦合）显式纳入超导微观机制的唯一途径**。