---
tags: [MOC, 计算工具, 脚本]
created: 2026-07-14
updated: 2026-07-14
---

# 计算脚本库（calculation）

> 从 QE relax.in → VASP POSCAR/POTCAR/INCAR/PBS → 批量提交 → 后处理的全流程脚本集。

## 目录结构

```
calculation/
├── CLAUDE.md                    ← 顶层 agent 路由
├── CLAUDE_TEMPLATE.md           ← 子模块 CLAUDE.md 编写规范
├── vasp/
│   ├── CLAUDE.md                ← VASP 模块总入口（opt + scf_ELF + 未来 bader）
│   ├── opt/                     ← ① 结构优化部署
│   │   ├── vasp_common.py       ← 核心库
│   │   ├── setup_elf_workflow.py
│   │   ├── make_poscar.py
│   │   ├── make_potcar.py
│   │   ├── run_elf_batch.py
│   │   └── submit_opt_elf.py
│   └── scf_ELF/                 ← ② SCF + ELF 计算部署
│       ├── scf_common.py         ← 导入 vasp_common
│       ├── scf_contcar_to_poscar_ELF.py
│       └── run_scf_batch.py
└── AIMD/
    ├── CLAUDE.md                ← AIMD 模块路由
    └── MSD&RMSD/                ← MSD / RMSD 后处理
        ├── msd_common.py
        ├── extract_msd_flex.py
        ├── plot_msd_flex.py
        ├── xdatcar_msd_flex.py
        └── plot_line_template.py  ← 通用绘图模板
```

## 核心功能

### VASP 结构优化（vasp/opt/）

| 脚本 | 功能 | 触发词 |
|------|------|--------|
| `setup_elf_workflow.py` | 批量建立 opt_ELF 目录 + ELF.pbs | "建立 opt 目录"、"setup opt" |
| `make_poscar.py` | 从 QE relax.in 生成 POSCAR | "生成 POSCAR"、"make poscar" |
| `make_potcar.py` | 赝势库择优拼接 POTCAR | "拼接 POTCAR"、"make potcar" |
| `run_elf_batch.py` | 一键部署 opt_ELF（①②③） | "一键部署 opt"、"run elf batch" |
| `submit_opt_elf.py` | 批量 qsub 提交 opt PBS 任务 | "提交 opt 任务"、"submit opt" |

**输出**: `vasp/opt/<材料>/<压强>/opt_ELF/{ELF.pbs, POSCAR, POTCAR}`

### VASP SCF + ELF（vasp/scf_ELF/）

| 脚本 | 功能 | 触发词 |
|------|------|--------|
| `scf_contcar_to_poscar_ELF.py` | opt/CONTCAR → scf_ELF/POSCAR | "CONTCAR 转 POSCAR"、"contcar to poscar" |
| `run_scf_batch.py` | 一键部署 scf_ELF（PBS+POSCAR+POTCAR） | "部署 scf"、"run scf batch" |

**输出**: `vasp/scf_ELF/<材料>/<压强>/scf_ELF/{ELF.pbs, POSCAR, POTCAR}`

### AIMD MSD/RMSD（AIMD/MSD&RMSD/）

| 脚本 | 功能 | 触发词 |
|------|------|--------|
| `extract_msd_flex.py` | XDATCAR → MSD/RMSD 数据表 | "提取 MSD"、"extract msd" |
| `plot_msd_flex.py` | MSD/RMSD 双子图 | "画 MSD 图"、"plot msd" |
| `xdatcar_msd_flex.py` | 一键计算+出图 | "MSD 一键分析" |
| `plot_line_template.py` | 通用折线图模板 | "画折线图"、"line template" |

## 全局约定

- Python 3.8+，仅标准库，无第三方依赖（AIMD 绘图除外，需 numpy + matplotlib）
- 代码注释和 docstring 使用中文
- 赝势库默认路径：`/home/test1/hhy/basic/psudopotential/PAW-GGA-PBE`
- POTCAR 择优：ZVAL 最大优先，日期最新次之
- KSPACING = 0.03，ENCUT = 800 eV，EDIFF = 1e-6
- PBS 模板默认：nodes=1:ppn=64，mpirun -np 16，队列 song
- prefer 分步脚本 > 一键脚本
- 目录建立先于文件部署，部分失败不删已有文件

## 相关链接

- [[../science_chat桥接协议|科学桥接协议]]
- [[DFT基础]]
- [[VASP使用指南]]
