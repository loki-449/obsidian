# basic 材料计算工具包 — 完整使用手册

> 版本说明：本手册覆盖 `basic/` 目录下**全部可执行脚本**、别名、配置项与典型工作流。  
> 设计原则：**整包可复制**到任意 Linux 集群；**单点失败不拖垮批处理**；日志文件记录跳过/失败项。

---

## 目录

1. [30 秒了解](#1-30-秒了解)
2. [第一次部署](#2-第一次部署)
3. [双集群切换](#3-双集群切换)
4. [功能总览图](#4-功能总览图)
5. [全部别名速查](#5-全部别名速查)
6. [根目录工具](#6-根目录工具)
7. [airss/ 结构搜索](#7-airss-结构搜索)
8. [VASP 模板目录](#8-vasp-模板目录)
9. [qe/pl/ VASP 高通量](#9-qepl-vasp-高通量)
10. [qe/ QE 超导与电声](#10-qe-qe-超导与电声)
11. [epw/ EPW 模块](#11-epw-epw-模块)
12. [paint/ 后处理绘图](#12-paint-后处理绘图)
13. [lib/ 公共库](#13-lib-公共库)
14. [资源与赝势](#14-资源与赝势)
15. [config/ 配置说明](#15-config-配置说明)
16. [完整脚本文件清单](#16-完整脚本文件清单)
17. [典型工作流](#17-典型工作流)
18. [错误日志说明](#18-错误日志说明)
19. [容错行为说明](#19-容错行为说明)
20. [外部依赖](#20-外部依赖)
21. [常见问题](#21-常见问题)
22. [paint/ 详细手册（输入输出路径）](#22-paint-详细手册输入输出路径)
23. [辅助脚本详解](#23-辅助脚本详解)
24. [paint 推荐流水线](#24-paint-推荐流水线)

---

## 1. 30 秒了解

```
AIRSS 找结构 → create 建目录 → VASP(opt/scf/phonon/band…) → QE(弛豫/elph/Tc) → paint 出图
```

| 你想做什么 | 用什么 |
|------------|--------|
| 初始化环境 | `bash setup.sh` |
| 查看所有命令 | `basic-help` |
| 建 opt/scf/phonon 目录 | `basic-create` |
| VASP 批量 opt→scf→phonon | `vasp-pl` |
| QE 批量超导全流程 | `qe-pl` |
| 汇总 Tc 结果 | `qe-sc` |
| 批量合并 band+PDOS 图 | `paint-merge` |
| 切换集群 | `basic-switch-cluster cluster2` |

---

## 2. 第一次部署

```bash
cd /path/to/basic
bash setup.sh          # 交互配置 cluster1 + cluster2
```

写入 `~/.bashrc`：

```bash
source /path/to/basic/config/env.sh
source /path/to/basic/aliases.sh
```

验证：

```bash
basic-env
basic-help
```

---

## 3. 双集群切换

`setup.sh` 会生成 `config/env.local.sh`，内含 **cluster1** 和 **cluster2** 两套 profile（VASP 路径、PBS 队列、QE module 等）。

```bash
# 使用集群1（默认）
export BASIC_CLUSTER=cluster1
source /path/to/basic/config/env.sh

# 切换到集群2
basic-switch-cluster cluster2
```

| 变量 | 含义 |
|------|------|
| `BASIC_CLUSTER` | `cluster1` 或 `cluster2` |
| `VASP_STD` | VASP 可执行文件 |
| `VASP_QUEUE` | PBS 队列名 |
| `VASP_NPROC` | 并行核数 |
| `QE_MODULE` | module 名，如 `qe/7.3` |
| `PW_ROOT` | QE bin 目录（可留空自动检测） |
| `ELIASHBERG_BIN` | Eliashberg 程序 |
| `KPOINT_GEN` | lxopt 用 K 点生成工具 |

---

## 4. 功能总览图

```
                    ┌─────────────┐
                    │   AIRSS     │  airss-select / airss-stable
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │ basic-create│  create4.1.1 → opt/scf/phonon/…
                    └──────┬──────┘
                           ▼
     ┌─────────────────────────────────────────────┐
     │              VASP 计算                       │
     │  opt → scf → band/dos/elf/bader/phonon      │
     │  模板: opt/ scf/ band/ …                    │
     │  高通量: vasp-pl / check-log / sort_phon    │
     └────────────────────┬────────────────────────┘
                          ▼
     ┌─────────────────────────────────────────────┐
     │              QE 超导                         │
     │  qe-pl: relax → lambda → elph → Tc           │
     │  单对象: qe-mscf / qe-band / qe-ad / qe-sc   │
     └────────────────────┬────────────────────────┘
                          ▼
     ┌─────────────────────────────────────────────┐
     │              paint 出图                      │
     │  paint-bandjob / paint-merge / paint-pdos   │
     └─────────────────────────────────────────────┘
```

---

## 5. 全部别名速查

### 导航与配置

| 别名 | 实际脚本 | 作用 |
|------|----------|------|
| `basic-cd` | — | 进入 BASIC_ROOT |
| `basic-env` | — | 打印当前环境变量 |
| `basic-help` | `bin/basic-help` | 命令索引 |
| `basic-setup` | `setup.sh` | 重新初始化 |
| `basic-switch-cluster` | — | 切换 cluster1/2 |

### 建目录与赝势

| 别名 | 脚本 | 作用 |
|------|------|------|
| `basic-create` | `create4.1.1` | 建 opt/scf/phonon（A/B/C 三模式） |
| `basic-bandin` | `scf-bandin-4.1` | SCF 后准备 band 目录 |
| `basic-potcar` | `potcarfinding` | 从赝势库找 POTCAR |

### AIRSS

| 别名 | 脚本 | 作用 |
|------|------|------|
| `airss-select` | `airss/opt-select-64.sh` | 筛选 .res / 建 VASP 目录 |
| `airss-stable` | `airss/enstable.sh` | 归档焓差<0.05 的 .res |

### VASP 高通量

| 别名 | 脚本 | 作用 |
|------|------|------|
| `vasp-pl` | `qe/pl/vasp-pl-64.sh` | 批量 scf/band/phonon 等 |
| `vasp-check` | `qe/pl/check-log.sh` | 检查 opt 日志，移到 wrong/ |
| `vasp-sort-phon` | `qe/pl/sort_phon.sh` | phonopy 稳定性分类 |

### QE 超导

| 别名 | 脚本 | 作用 |
|------|------|------|
| `qe-pl` | `qe/pl/qe-pl-64.sh` | QE 高通量主控 |
| `qe-mscf` | `qe/m-scf.sh` | **单对象**：pw.pbs → lambda |
| `qe-mscf-batch` | `qe/pl/pl-mqescf-single-use.sh` | 批量 m-scf + qsub |
| `qe-band` | `qe/BAND.py` | **单对象**：QE 能带链 |
| `qe-ad` | `qe/run_AD_high.sh` | 批量 run_AD 求 Tc |
| `qe-sc` | `qe/detail_Superconduct.sh` | 汇总 S-C.txt |
| `qe-fatband` | `qe/outo_fatband_pdos_high.py` | 批量 fatband+PDOS |
| `qe-cell` | `qe/cell.sh` | 从 relax.out 提取晶胞 |
| `qe-move` | `qe/moving.sh` | 单对象：复制到新压力目录 |
| `qe-move-pl` | `qe/pl/moving-pl.sh` | PL 高通量：复制 relax.in + lambda |

### 画图

| 别名 | 脚本 | 作用 |
|------|------|------|
| `paint-bandjob` | `paint/curr-band-l.py` | 批量提交 VASP band |
| `paint-vaspkit` | `paint/pdos-vaspkit.py` | vaspkit 提取 PDOS |
| `paint-band` | `paint/band_plot.py` | 画能带 |
| `paint-pdos` | `paint/pdos_plot.py` | 画 PDOS |
| `paint-merge` | `paint/merge_all.py` | 批量合并 band+PDOS |
| `paint-pdos-batch` | `paint/pdos-pic.py` | 批量 PDOS 图 |
| `paint-combine` | `paint/combine_plot.py` | 单结构拼接 band.png+pdos.png |
| `paint-clean` | `paint/clean_done_flags.py` | 清除 .done_pic |
| `paint-plot-all` | `paint/plot_all.py` | 批量出 band+pdos+合并三张图 |

### 进入模板目录

| 别名 | 进入 |
|------|------|
| `tpl-opt` | `opt/` |
| `tpl-scf` | `scf/` |
| `tpl-band` | `band/` |
| `tpl-phonon` | `phonon/` |
| `tpl-qe` | `qe/` |

### 函数

| 函数 | 作用 |
|------|------|
| `vasp-qsub [模板名]` | 当前目录提交 VASP（无 pbs 时从模板复制） |

---

## 6. 根目录工具

### `create4.1.1`（别名 `basic-create`）

**前提：** 当前目录有 `POSCAR` 和 `POTCAR`。

| 模式 | 输入 | 生成内容 |
|------|------|----------|
| **A** | 两元素 + H + 化学比 + 压力 | 多组分目录，各含 opt/scf/phonon/scf-bandin-4.1 |
| **B** | 结构名 + 多压力 + 可选 band/bader/elf 压力点 | `{结构}/{压力}/opt,scf,phonon` + `{结构}/lx/` |
| **C** | 结构名 + 单一压力 | `{结构}/opt,scf,phonon`（最常用） |

**压力习惯：** 输入 GPa 数值，脚本自动加 `0` 转为 kbar（如输入 `50` → PSTRESS=500）。

**容错：** 缺 POSCAR/POTCAR 会警告；选项 B 的 band/bader/elf 会检查压力目录是否存在。

---

### `scf-bandin-4.1`（别名 `basic-bandin`）

**在哪里运行：** 某结构的根目录（与 opt/ scf/ 同级）。

**做什么：**
1. 复制 `band/` 模板
2. 从 scf/ 复制 CHGCAR、POTCAR、CONTCAR→POSCAR
3. vaspkit 303 生成 K 路径 → KPOINTS
4. 只改 KPOINTS **第 2 行** 密度为 120

**容错：** 若 band/ 已存在则退出，避免覆盖。

---

### `potcarfinding`（别名 `basic-potcar`）

从 `psudopotential/PAW-GGA-PBE` 按元素找 POTCAR，输出为 `{元素}_POTCAR`。  
多个匹配时交互选择。找不到则警告并继续下一个元素。

---

### `setup.sh`（别名 `basic-setup`）

首次部署：双集群 profile、路径层级、同步 element-information、chmod。

---

## 7. airss/ 结构搜索

### `opt-select-64.sh`（别名 `airss-select`）

| 任务 | 做什么 | 需要 |
|------|--------|------|
| **1** | 焓差<0.05 筛选 .res → POSCAR，打包下载 | `.res`、`ca`、`cabal`、`vaspkit` |
| **2** | 对 select.tmp 结构建 opt 目录 | `select.tmp`、`primitive-temp/`、`potcar/` |
| **3** | 全部 .res 转 POSCAR（不筛选） | `.res`；会**清空** select.tmp |

**容错：** POTCAR 逐元素拼接；create 不复制到 vasp/，直接 `bash $BASIC_CREATE411`；单结构失败 continue。

---

### `enstable.sh`（别名 `airss-stable`）

将焓差<0.05 的 `.res` 复制到 `enthalpy_stable/`。缺文件跳过并警告。

---

## 8. VASP 模板目录

这些目录是**模板**，由 `basic-create` 复制到计算目录，或在目录内 `qsub`。

| 目录 | 算什么 | 关键 INCAR | PBS |
|------|--------|------------|-----|
| `opt/` | 结构优化 | NSW, ISIF=3, PSTRESS | `vasp.pbs` |
| `scf/` | 自洽场 | EDIFF=1e-7, ENCUT=800 | `scf.pbs`, `vasp.pbs` |
| `band/` | 能带 NSCF | ICHARG=11 | `band.pbs`, `vasp.pbs` |
| `dos/` | 态密度 | ISMEAR=-5 | `dos.pbs` |
| `elf/` | 电子局域化 | LELF | `elf.pbs` |
| `bader/` | Bader 电荷 | LAECHG | `bader.pbs` |
| `phonon/` | 有限位移声子 | 6 个 POSCAR-00x | `phon.pbs` |
| `lxopt/` | 压力扫描 0–2000 | PSTRESS 循环 | `run.pbs` |

**PBS 变量：** 使用 `${VASP_STD:-vasp_std}`，由 `env.local.sh` 配置。

**典型顺序：**

```bash
cd 结构名/opt/ && qsub vasp.pbs
# 完成后
cd ../scf/ && cp ../opt/CONTCAR POSCAR && cp ../opt/POTCAR . && qsub scf.pbs
```

---

## 9. qe/pl/ VASP 高通量

### `vasp-pl-64.sh`（别名 `vasp-pl`）

交互菜单（1–8）：

| 选项 | 功能 | 说明 |
|------|------|------|
| 1 | 批量 SCF | opt/CONTCAR → scf/POSCAR，qsub |
| 2 | 批量 band | 调用 scf-bandin-4.1，改 KPOINTS 第 2 行 |
| 3 | 批量 phonon | optin-phonon + qsub |
| 4 | 能带数据处理 | vaspkit 211/113 |
| 5 | 交互查看能带 | xmgrace（可选） |
| 6 | Phonon 数据处理 | phonopy + 分类 → phonopy/lil-unstable |
| 7 | 低精度声子再算 | 在 lil-unstable 里扩胞重算 |
| 8 | 批量提交 opt | qsub opt/vasp.pbs |

**容错：** 每个结构独立处理，失败 `[WARN]` 跳过；`basic_qsub` 失败不中断；修复了原先 `cd ../../` 路径错误。

---

### `check-log.sh`（别名 `vasp-check`）

逐个查看 `*/opt/log0`，可选移到 `wrong/`。

---

### `sort_phon.sh`（别名 `vasp-sort-phon`）

将 `unstable.tmp` / `lil_unstable.tmp` 中的结构移入 `phonopy/lot-unstable/`、`phonopy/lil-unstable/`。  
`vasp-pl` 选项 6 结束时也会自动执行；详见 [第 23.1 节](#231-sort_phonsh别名-vasp-sort-phon)。

---

### `moving-pl.sh`（别名 `qe-move-pl`）

PL 版压力目录复制（`relax.in` + lambda），详见 [第 23.3 节](#233-moving-plsh)。

---

## 10. qe/ QE 超导与电声

### 两个 m-scf 脚本（ deliberately 分开）

| 脚本 | 别名 | 输入文件 | 模板来源 | 用途 |
|------|------|----------|----------|------|
| `qe/m-scf.sh` | `qe-mscf` | `pw.pbs` | `qe/lambda/` | **单研究对象** |
| `qe/pl/m-scf.sh` | （pl 内部） | `relax.in` | `qe/pl/lambda-pl/` | **高通量 pl 流程** |

公共逻辑在 `lib/m_scf_common.sh`：复制 PBS → 填充 prefix/nat/ntyp/晶胞/赝势。

---

### `qe/pl/qe-pl-64.sh`（别名 `qe-pl`）

| 选项 | 功能 |
|------|------|
| 1 | 从 VASP opt/CONTCAR 生成 relax.in + pw.pbs |
| 2 | mqescf：relax.out → extracted_data → pl/m-scf.sh |
| 3 | 批量 qsub pwscf.pbs |
| 4 | 批量 qsub qe-ph.pbs |
| 5 | 批量 qsub pw.pbs（QE 弛豫） |
| 6 | run_elph_1 求第一点 Tc |
| 7 | 清理 tmp 目录 |

---

### `qe/pl/pl-mqescf-single-use.sh`（别名 `qe-mscf-batch`）

批量：复制 **pl/m-scf.sh** → 执行 → qsub pwscf 或 qe-ph。

---

### 单对象脚本（在**单个结构 qe/** 目录下用）

| 脚本 | 别名 | 作用 |
|------|------|------|
| `cell.sh` | `qe-cell` | relax.out → extracted_data.txt |
| `one-mscf.sh` | — | 仅填充已有 lambda（不复制模板） |
| `moving.sh` | `qe-move` | 按压力复制文件夹 |
| `BAND.py` | `qe-band` | QE 能带 NSCF + task_sub 链式提交 |
| `task_sub.py` | — | PBS depend 链 |
| `deta_band.py` | — | 能带细节处理 |

---

### 批量后处理

| 脚本 | 别名 | 输出 |
|------|------|------|
| `run_AD_high.sh` | `qe-ad` | 失败 → `err_run_AD.txt` |
| `detail_Superconduct.sh` | `qe-sc` | `S-C.txt`；路径失败 → `error_cal.txt` |
| `outo_fatband_pdos_high.py` | `qe-fatband` | 批量 fatband+PDOS |

**路径解析（qe-sc）：** 在 `env.local.sh` 设置：

```bash
export BASIC_SC_PRESSURE_UP=2   # lambda 向上第几层是 pressure
export BASIC_SC_SYSTEM_UP=3     # lambda 向上第几层是 system
# 例: Proj/Struct/500/qe/lambda → UP=2 得 500, UP=3 得 Struct
```

---

### `qe/lambda/` — 电声耦合模板

| 文件 | 作用 |
|------|------|
| `pwscf.pbs` | QE SCF |
| `qe-ph.pbs` | ph.x 声子 |
| `pwscf-one.sh` | 一体化 SCF 输入 |
| `run_q2r` / `run_frequency` / `run_dos` | 声子后处理 |
| `elph_dir/run_elph` | lambda.x |
| `elph_dir/run_AD` | AD 法 Tc |
| `elph_dir/run_Eliashberg.sh` | Eliashberg |
| `elph_dir/ML.py` | McMillan Tc |

---

### `qe/band/` — QE 能带（配合 BAND.py）

| 文件 | 作用 |
|------|------|
| `band.py` | 处理 bd.dat |
| `fatband.py` | 投影能带（交互） |
| `outo_fatband_pdos.py` | BAND.dat + PDOS |
| `pw-nscf.pbs` / `band_deal.pbs` / `pdos.pbs` | PBS 模板 |

---

## 11. epw/ EPW 模块

| 文件 | 作用 |
|------|------|
| `epw/pwscf.pbs` | QE scf |
| `epw/Nscf.pbs` | nscf |
| `epw/EPW.pbs` | epw.x |
| 根目录 `epw.pbs` | 串联流程 |

依赖 `phonon/save`（dvscf）。

---

## 12. paint/ 后处理绘图

| 脚本 | 别名 | 输入 | 输出 |
|------|------|------|------|
| `curr-band-l.py` | `paint-bandjob` | 各 `*/scf/log` 成功 | 批量 qsub band |
| `pdos-vaspkit.py` | `paint-vaspkit` | band/ | PDOS 数据 |
| `pdos-deta.py` | — | PDOS_*.dat | pic-PDOS.dat |
| `band_plot.py` | `paint-band` | BAND.dat | 能带 png |
| `pdos_plot.py` | `paint-pdos` | pic-PDOS.dat | PDOS png |
| `merge_band_pdos.py` | — | 单 band/ 目录 | band_pdos_combined.png |
| `merge_all.py` | `paint-merge` | 多结构 | `all_pic/*.png` |
| `pdos-pic.py` | `paint-pdos-batch` | pdos 数据 | all_pic/ |
| `combine_plot.py` | `paint-combine` | band.png + pdos.png | 拼接图 |
| `plot_all.py` | `paint-plot-all` | 批量出 band+pdos+合并三张图到 all_pic/ |
| `clean_done_flags.py` | `paint-clean` | — | 删 .done_pic |
| `utils.py` | — | 绘图工具函数 | — |

**merge_all 容错：** 缺 BAND.dat 或 pic-PDOS.dat 写入 `missing_band_or_pdos.txt`；单结构失败 continue。

详细输入输出路径见 [第 22 节](#22-paint-详细手册输入输出路径)；推荐顺序见 [第 24 节](#24-paint-推荐流水线)。

---

## 13. lib/ 公共库

| 文件 | 作用 |
|------|------|
| `lib/basic.sh` | 加载 env + common |
| `lib/common.sh` | **容错工具**：`basic_warn`、`safe_cd`、`basic_qsub`、`require_cmd`… |
| `lib/basic_paths.py` | Python 路径助手 |
| `lib/extract_cell.sh` | relax.out → extracted_data.txt |
| `lib/m_scf_common.sh` | 两个 m-scf 公共填充 |
| `lib/kpoints_density.sh` | 只改 KPOINTS 第 2 行 |
| `lib/path_meta.sh` | qe-sc 路径层级解析 |
| `lib/phonon_classify.sh` | phonon 分类移动 |

---

## 14. 资源与赝势

| 目录 | 内容 |
|------|------|
| `PBE-6.3-qe/` | QE .UPF 赝势 + element-information |
| `psudopotential/` | VASP 赝势（PAW-GGA-PBE 等） |
| `high_screen/` | 高通量筛选用赝势副本（保留打包） |
| `test/12/` | 完整示例 opt/scf/phonon |

---

## 15. config/ 配置说明

| 文件 | 作用 |
|------|------|
| `config/env.sh` | 主环境（自动检测 BASIC_ROOT） |
| `config/env.local.sh` | **你的配置**（setup 生成） |
| `config/env.local.example.sh` | 配置示例 |
| `config/pbs_vasp.inc` | VASP PBS 公共片段 |

---

## 16. 完整脚本文件清单

> 以下为仓库内全部 `.sh` / `.py` / 入口脚本（不含纯 PBS 模板内的单行 run_*）。

### 根目录
- `create4.1.1` — 建计算目录
- `scf-bandin-4.1` — 准备 band
- `potcarfinding` — 找 POTCAR
- `setup.sh` — 初始化
- `aliases.sh` — 别名
- `epw.pbs` — EPW 一键流程

### airss/
- `opt-select-64.sh` — AIRSS 主流程
- `enstable.sh` — 稳定结构归档

### qe/
- `m-scf.sh` — 单对象 m-scf
- `one-mscf.sh` — 仅填充 lambda
- `cell.sh` — 提取晶胞
- `moving.sh` — 压力复制
- `BAND.py` — 单对象 QE 能带
- `deta_band.py` — 能带细节
- `task_sub.py` — PBS 链
- `run_AD_high.sh` — 批量 AD
- `detail_Superconduct.sh` — 汇总 Tc
- `outo_fatband_pdos_high.py` — 批量 fatband

### qe/pl/
- `qe-pl-64.sh` — QE 高通量主控
- `vasp-pl-64.sh` — VASP 高通量
- `m-scf.sh` — PL 版 m-scf
- `pl-mqescf-single-use.sh` — 批量 m-scf
- `check-log.sh` — 检查 opt
- `sort_phon.sh` — 声子分类
- `moving-pl.sh` — PL 压力移动

### qe/band/
- `band.py`, `fatband.py`, `outo_fatband_pdos.py`, `d-fatband.sh`, `task_sub.py`

### qe/lambda/ & qe/pl/lambda-pl/
- `pwscf.pbs`, `qe-ph.pbs`, `pwscf-one.sh`, `run_q2r`, `run_frequency`, `run_dos`
- `elph_dir/run_elph`, `run_AD`, `run_Eliashberg.sh`, `ML.py`, `eliashberg.pbs`

### paint/
- `curr-band-l.py`, `merge_all.py`, `merge_band_pdos.py`, `band_plot.py`, `pdos_plot.py`
- `pdos-vaspkit.py`, `pdos-vasp.py`, `pdos-deta.py`, `pdos-pic.py`
- `combine_plot.py`, `merge_plot.py`, `plot_all.py`, `clean_done_flags.py`, `utils.py`

### lib/
- `basic.sh`, `common.sh`, `basic_paths.py`, `extract_cell.sh`, `m_scf_common.sh`
- `kpoints_density.sh`, `path_meta.sh`, `phonon_classify.sh`

### bin/
- `basic-help`

---

## 17. 典型工作流

### A. AIRSS → VASP

```bash
cd airss_output/
airss-select    # 1 筛选 → 2 建目录
cd 结构名/opt && qsub vasp.pbs
```

### B. 单结构 VASP 全套

```bash
# POSCAR + POTCAR 就绪
basic-create    # 选 C
cd 结构名/opt && qsub vasp.pbs
cd ../scf && cp ../opt/CONTCAR POSCAR && qsub scf.pbs
basic-bandin && cd band && qsub vasp.pbs
```

### C. 多结构 VASP 高通量

```bash
cd project/
vasp-pl         # 1 scf → 3 phonon → 2 band
vasp-check
paint-bandjob && paint-merge
```

### D. QE 超导

```bash
cd project/     # 各结构已有 opt/CONTCAR
qe-pl           # 1→2→3→4→6
qe-ad && qe-sc  # 看 S-C.txt
```

---

## 18. 错误日志说明

| 文件 | 产生脚本 | 含义 |
|------|----------|------|
| `S-C.txt` | qe-sc | 汇总 Tc 结果 |
| `error_cal.txt` | qe-sc | 路径解析失败 |
| `err_run_AD.txt` | qe-ad | run_AD 失败目录 |
| `err_run_AD.txt.detail` | qe-ad | 详细 stderr |
| `err-scf.txt` | paint-bandjob | SCF 未成功的目录 |
| `missing_band_or_pdos.txt` | paint-merge | 缺数据文件 |
| `.qe_pl_processed.log` | qe-pl 选项1 | 成功生成 relax 的目录 |
| `wrong/` | vasp-check | opt 有问题的结构 |
| `phonopy/lil-unstable/` | vasp-pl 选项6 | 需重算声子的结构 |
| `err-band.txt` | paint-vaspkit | band 计算未成功 |
| `err_pdos_dat.txt` | pdos-deta | 缺 PDOS_*.dat / TDOS.dat |
| `err_pic_pdos_dat.txt` | paint-pdos-batch | 缺 pic-PDOS.dat 或绘图失败 |
| `missing_band.txt` | plot_all.py | 缺 BAND.dat/KLABELS 或 band 绘图失败 |
| `missing_pdos.txt` | plot_all.py | 缺 pic-PDOS.dat 或 pdos 绘图失败 |
| `processed_dirs.txt` | paint-vaspkit | 已跑过 vaspkit 的 band 目录 |
| `.done_pdos` | pdos-deta | 某结构 PDOS 已合并（跳过标记） |
| `.done_pic` | pdos-pic | 某结构 PDOS 图已画（跳过标记） |

---

## 19. 容错行为说明

本工具包批处理脚本的通用原则：

1. **单结构失败不退出整批**：输出 `[WARN]`，继续下一个。
2. **qsub 失败**：`basic_qsub` 只警告，不 `exit`。
3. **缺文件**：跳过并记录到对应 `.txt` 日志。
4. **路径**：所有入口脚本 `source lib/basic.sh`，不依赖硬编码绝对路径。
5. **grep -P 不可用**：m-scf 已改用 `basic_parse_prefix` 等兼容函数。
6. **KPOINTS**：只改第 2 行，避免误改坐标。
7. **目录切换**：高通量脚本用 `topdir` 变量，避免 `cd ../../` 错位。

---

## 20. 外部依赖

| 软件 | 用途 | 必须？ |
|------|------|--------|
| VASP | 优化/SCF/能带/声子 | VASP 流程必须 |
| Quantum ESPRESSO | 超导/elph | QE 流程必须 |
| PBS (qsub) | 提交任务 | 集群必须 |
| vaspkit | K 路径/PDOS | 强烈建议 |
| cabal + ca | AIRSS | AIRSS 必须 |
| bc | 数值比较 | airss 筛选 |
| phonopy | 声子分析 | sort_phon / vasp-pl 6 |
| Python3 + matplotlib | paint | 画图必须 |
| Eliashberg | 精确 Tc | 可选 |

---

## 21. 常见问题

**Q: 命令找不到？**  
`source config/env.sh && source aliases.sh`

**Q: 切换集群后 VASP 路径不对？**  
`basic-switch-cluster cluster1` 或编辑 `env.local.sh`

**Q: qe-sc 的 system/pressure 不对？**  
调整 `BASIC_SC_PRESSURE_UP` / `BASIC_SC_SYSTEM_UP`

**Q: basic-create 失败？**  
确认当前目录有 POSCAR、POTCAR；`basic-env` 检查 BASIC_ROOT

**Q: 如何看全部功能？**  
`basic-help` 或本文档 [第 16 节](#16-完整脚本文件清单)

---

## 22. paint/ 详细手册（输入输出路径）

> 所有 paint 脚本默认在**项目根目录**（含多个结构子文件夹）或**单个 band/** 目录下运行。  
> 下面路径均相对于「结构目录」`StructA/`，除非另说明。

### 22.1 目录与文件约定

```
project/
├── StructA/
│   ├── scf/log              ← paint-bandjob 检查 SCF 是否成功
│   ├── band/
│   │   ├── log              ← paint-vaspkit 检查 band 是否算完
│   │   ├── BAND.dat         ← vaspkit 211 或 QE 后处理
│   │   ├── KLABELS          ← vaspkit 303/113
│   │   ├── PDOS_*.dat       ← vaspkit 111
│   │   ├── TDOS.dat         ← vaspkit 113
│   │   ├── pic-PDOS.dat     ← pdos-deta 合并输出
│   │   ├── band.png         ← band_plot 或 merge_band_pdos
│   │   ├── pdos.png         ← pdos_plot
│   │   └── band_pdos_combined.png  ← merge_band_pdos（单目录）
│   ├── .done_pdos           ← pdos-deta 完成标记
│   └── .done_pic            ← pdos-pic 完成标记
└── all_pic/                 ← 批量输出总目录
    ├── StructA.png          ← paint-merge / pdos-pic
    └── StructA_band+pdos.png ← plot_all.py
```

---

### 22.2 各脚本逐项说明

#### `curr-band-l.py`（别名 `paint-bandjob`）

| 项 | 说明 |
|----|------|
| **在哪运行** | `project/`（含多个 `*/scf/`） |
| **输入** | 各结构 `scf/log` 含 `1 F=`、`E0=` |
| **输出** | 创建 `*/band/`，复制模板，qsub `band/vasp.pbs` |
| **标记** | `band/.submitted`、`.done` |
| **日志** | `err-scf.txt` — SCF 未通过的结构 |
| **用法** | `cd project/ && paint-bandjob` |

---

#### `pdos-vaspkit.py`（别名 `paint-vaspkit`）

| 项 | 说明 |
|----|------|
| **在哪运行** | `project/` |
| **前提** | `band/log` 计算成功 |
| **做什么** | 在每个 `band/` 内依次 vaspkit **113 → 111 → 211** |
| **产出** | `PDOS_*.dat`、`TDOS.dat`、`BAND.dat`、`KLABELS` 等 |
| **日志** | `err-band.txt`；`processed_dirs.txt` 防重复 |
| **下一步** | 运行 `pdos-deta` 生成 `pic-PDOS.dat` |

---

#### `pdos-deta.py`

| 项 | 说明 |
|----|------|
| **在哪运行** | `project/` |
| **输入** | `band/PDOS_*.dat` + `band/TDOS.dat` |
| **输出** | `band/PDOS.dat`、`band/pic-PDOS.dat`（含 tot-PDOS、TDOS、NONE 列） |
| **标记** | 结构根目录 `.done_pdos` |
| **日志** | `err_pdos_dat.txt` |
| **用法** | `python3 paint/pdos-deta.py` |

---

#### `pdos-vasp.py`

与 `pdos-vaspkit.py` 逻辑相同（检查 log + vaspkit 113/111/211），可视为备用副本。

---

#### `band_plot.py`（别名 `paint-band`）

| 项 | 说明 |
|----|------|
| **在哪运行** | `StructA/band/` 或指定路径 |
| **输入** | `BAND.dat` + `KLABELS` |
| **输出** | 默认当前目录 `band.png`（也可命令行指定） |
| **能量范围** | -5 ~ 5 eV |
| **单独用法** | `cd StructA/band && python3 ../../paint/band_plot.py BAND.dat KLABELS band.png` |

---

#### `pdos_plot.py`（别名 `paint-pdos`）

| 项 | 说明 |
|----|------|
| **在哪运行** | `StructA/band/` |
| **输入** | `pic-PDOS.dat` |
| **输出** | `pdos.png`（或指定 `out_png`） |
| **用法** | `cd StructA/band && paint-pdos` |

---

#### `merge_band_pdos.py`

| 项 | 说明 |
|----|------|
| **在哪运行** | **单个** `StructA/band/` |
| **输入** | `BAND.dat`、`KLABELS`、`pic-PDOS.dat` |
| **输出** | `band/band_pdos_combined.png`（一张图含能带+PDOS） |
| **用法** | `cd StructA/band && python3 ../../paint/merge_band_pdos.py` |

---

#### `merge_all.py`（别名 `paint-merge`）

| 项 | 说明 |
|----|------|
| **在哪运行** | `project/` |
| **输入** | 各结构 `band/BAND.dat` + `band/pic-PDOS.dat` |
| **输出** | 调用各目录 `merge_band_pdos.py`，复制到 `all_pic/{结构名}.png` |
| **日志** | `missing_band_or_pdos.txt` |
| **用法** | `cd project/ && paint-merge` |

---

#### `pdos-pic.py`（别名 `paint-pdos-batch`）

| 项 | 说明 |
|----|------|
| **在哪运行** | `project/` |
| **输入** | 各结构 `band/pic-PDOS.dat` |
| **输出** | `all_pic/{结构路径}.png`（横向 PDOS 图） |
| **标记** | `.done_pic` |
| **日志** | `err_pic_pdos_dat.txt` |

---

#### `combine_plot.py`（别名 `paint-combine`）

| 项 | 说明 |
|----|------|
| **在哪运行** | 单结构目录 |
| **输入** | `band/band.png` + `band/pdos.png`（需先分别生成） |
| **输出** | `StructA/StructA_band_pdos.png` |
| **用法** | `python3 paint/combine_plot.py StructA` |

---

#### `plot_all.py`（别名 `paint-plot-all`，批量一站式）

| 项 | 说明 |
|----|------|
| **在哪运行** | `project/` |
| **输入** | 各结构 `band/BAND.dat`、`KLABELS`、`pic-PDOS.dat` |
| **输出** | `all_pic/{名}_band.png`、`{名}_pdos.png`、`{名}_band+pdos.png` |
| **日志** | `missing_band.txt`、`missing_pdos.txt` |
| **与 paint-merge 区别** | plot_all 分三张图；merge_all 只出一张合并 png |

---

#### `clean_done_flags.py`（别名 `paint-clean`）

删除所有 `.done_pic` 标记，便于重跑 `pdos-pic`。

---

#### `utils.py` / `merge_plot.py`

内部模块：`merge_plot.merge_images_horizontally` 供 `plot_all.py` 横向拼接 PNG。

---

## 23. 辅助脚本详解

### 23.1 `sort_phon.sh`（别名 `vasp-sort-phon`）

**作用：** 将 phonon 人工分类结果写入物理目录。

| 步骤 | 说明 |
|------|------|
| 前置 | 通常先运行 `vasp-pl` **选项 6**（deal_phonon），人工判断后写入 `unstable.tmp` / `lil_unstable.tmp` |
| 本脚本 | 把 tmp 中的结构名 `mv` 到 `phonopy/lot-unstable/`、`phonopy/lil-unstable/` |
| 注意 | `vasp-pl` 选项 6 **末尾已自动调用**相同逻辑；若 tmp 是旧流程遗留，可单独跑 `vasp-sort-phon` |

**目录结构：**

```
project/
├── phonopy/
│   ├── lot-unstable/    ← 完全不稳定 (输入 e)
│   └── lil-unstable/    ← 尚可尝试 (输入 n)
├── unstable.tmp         ← 选项6 临时记录（处理后删除）
└── lil_unstable.tmp
```

---

### 23.2 `moving.sh`（别名 `qe-move`）

**用途：** 单对象 QE — 从已有压力点**复制**到新压力目录。

| 输入（交互） | 说明 |
|--------------|------|
| 压力值 | GPa，脚本加 `0` → kbar（如 `50` → `500`） |
| 源目录名 | 含 `pw.pbs` 和 `lambda/` 的文件夹 |

| 输出 | 说明 |
|------|------|
| `{压力}/pw.pbs` | `press =` 已替换 |
| `{压力}/lambda/` | 复制 pwscf.pbs、qe-ph.pbs、pwscf-one.sh |

**示例：**

```bash
cd qe_work/          # 已有 0/ 目录算完
qe-move              # 输入 50 和 0
cd 50/ && qsub pw.pbs
```

---

### 23.3 `moving-pl.sh`（别名 `qe-move-pl`）

与 `moving.sh` 相同思路，但针对 **高通量 pl 目录**（含 `relax.in` + `pw.pbs`）。

| 区别 | moving.sh | moving-pl.sh |
|------|-----------|--------------|
| 别名 | `qe-move` | `qe-move-pl` |
| 压力写在 | `pw.pbs` | `relax.in` |
| 输入文件 | `pw.pbs` | `relax.in` + `pw.pbs` |
| 场景 | 单对象 qe/ | pl 生成的 qe/ 子目录 |

**示例：**

```bash
cd project/StructA/qe/   # 已有 0/ 算完
qe-move-pl             # 输入 50 和 0
cd 50/ && qsub pw.pbs
```

---

### 23.4 `one-mscf.sh`

**用途：** lambda 模板**已在** `./lambda/` 时，仅填充 `pwscf-one.sh` 等（不重新复制 PBS）。

**前提：** 当前目录有 `pw.pbs`、`extracted_data.txt`、`lambda/`。

---

### 23.5 `qe/pl/lambda-pl/` 内小脚本

| 文件 | 何时运行 | 作用 |
|------|----------|------|
| `run_q2r` | 声子后 | `q2r.x < q2r.in` |
| `run_frequency` | q2r 后 | `matdyn.x` 算频率 |
| `run_dos` | 可选 | 声子 DOS |
| `elph_dir/run_elph` | elph 步 | `lambda.x` |
| `elph_dir/run_AD` | 有 lambda.out | AD 法 Tc |
| `elph_dir/run_Eliashberg.sh` | elph 完成 | 生成并 qsub Eliashberg |
| `elph_dir/ML.py` | 手动 | McMillan 公式 |
| `qe_fatband.sh` | 可选 | QE fatband 辅助 |

均在对应 `lambda/` 或 `elph_dir/` 内执行，需先 `module load` QE。

---

### 23.6 `qe/band/` 单对象脚本（配合 `qe-band`）

| 文件 | 作用 |
|------|------|
| `band.py` | 读 scf.out，转换 bd.dat |
| `fatband.py` | **交互**选择轨道，生成投影能带 |
| `outo_fatband_pdos.py` | fatband + sumpdos → BAND.dat、PDOS |
| `d-fatband.sh` | 预处理 transformed_bd.dat.gnu |
| `task_sub.py` | PBS 链式 depend 提交 |
| `pw-nscf.pbs` / `band_deal.pbs` / `pdos.pbs` | PBS 模板 |

**与高通量区别：** 在**单个**研究对象的 `Band/` 目录使用；`qe-fatband` 批量调用 `outo_fatband_pdos_high.py`。

---

### 23.7 `deta_band.py`

QE 能带细节后处理（单文件脚本，配合已有 Band 输出）。

---

## 24. paint 推荐流水线

### 路线 A：VASP band + vaspkit PDOS（最常用）

```bash
cd project/

# 1. SCF 完成后批量提交 band
paint-bandjob

# 2. band 算完后提取 PDOS 数据
paint-vaspkit

# 3. 合并 PDOS 文件
python3 paint/pdos-deta.py

# 4. 批量出合并图
paint-merge
# → 查看 all_pic/*.png
```

### 路线 B：只要 PDOS 横向图

```bash
cd project/
python3 paint/pdos-deta.py    # 若尚未有 pic-PDOS.dat
paint-pdos-batch
# → all_pic/
```

### 路线 C：单结构精细出图

```bash
cd StructA/band/
python3 ../../paint/band_plot.py BAND.dat KLABELS band.png
python3 ../../paint/pdos_plot.py   # 读 pic-PDOS.dat → pdos.png
python3 ../../paint/combine_plot.py ..   # 或 merge_band_pdos.py 一张图
```

### 路线 D：批量三张图（band / pdos / 合并）

```bash
cd project/
paint-plot-all
# → all_pic/{名}_band.png, _pdos.png, _band+pdos.png
```

---

*文档与代码同步维护。若新增脚本，请更新本节与 `bin/basic-help`。*
