# COHP / LOBSTER 排查状态

## 已确认问题（3 个）

| # | 问题 | 修改位置 | 状态 |
|---|------|---------|------|
| 1 | Ce 4f 缺失 → spilling 89% | `lib/lobster_basis.py` `DEFAULT_BASIS['Ce']` | 已出设计 |
| 2 | Bunge 不支持 Z>54 → 自动回退 Koga 但轨道不全 | `lib/lobster_basis.py` `write_lobsterin()` | 已出设计 |
| 3 | k 点全对称 warning → vaspkit scheme 1 不够, 须用 3 | `lib/cohp_common.py` `VASPKIT_KPOINTS_INPUT` | 已出设计 |

## 待确认

- Ba3AgH7_10 spilling 31% — 是否 cohpGenerator 范围问题 (1.0-3.0 vs 期望 0.6-1.6)？需检查 lobsterin 文件内容
- 其他含 f 电子体系 (La3AuH7_0, Ce3AuH7_0 等) 是否同样受基组问题影响
