# Phase 3 — Human Codex Operation Held-out

**日期:** 2026-06-14  
**状态:** Phase 3+ 加强基线闭合。  
**结论:** Human Codex 在 22/22 个 held-out 年份上超过 frequency baseline，平均增益 `Δ=+0.120 bits/move`；并在 19/22 年上超过 recency baseline (`p=0.000428`)。GameCodex 获得 Codex operation 的自然域闭合信号。

---

## 1. 问题

Phase 1/2 说明 AI 时代的围棋变化不是全局耦合重写，而是 rhythm 维度上的操作点迁移和选择性收敛。Phase 3 要回答更核心的问题：

> 历史沉积的局面/棋步 Codex，是否能在 held-out 年份中提高未来棋步预测？

如果 Human Codex 不能超过 frequency baseline，那么 GameCodex 只能停留在结构描述。若能稳定超过，则说明历史棋谱沉积物具有 operation：它能帮助后续读取未来选择。

## 2. 主结果

| 指标 | 结果 |
|------|------|
| Human Codex > Frequency | 22/22 年 |
| sign / permutation p | p≈0.000000 |
| 平均增益 | Δ = +0.120 bits/move |
| Recency > Frequency | 22/22 年, Δ=+0.094 bits/move |
| Hist > Recency | 19/22 年, p=0.000428 |

解释：

> 历史局面信息一贯提高棋步预测，超过全局频率基线；并且全史 Codex 胜过近期流行 baseline。

这不是“近期流行度惯性”。如果 Codex 只是在重复最近热门棋步，recency baseline 应该吸收增益；但 `Hist > Recency` 在 19/22 年成立，说明长期沉积模式比短期趋势更有预测力。

## 3. Era 波动

| Era | Δ bits/move | 解释 |
|-----|-------------|------|
| E0 | CI [+0.082, +0.131] | 前 AlphaGo 时代，Human Codex 稳定有效 |
| E1 | CI [+0.084, +0.231] | AlphaGo shock 期仍遵循历史模式，且波动较大 |
| E2 | CI [+0.059, +0.125] | AI diffusion 期最低；历史 Human Codex 退化 |
| E3 | CI [+0.135, +0.197] | Oracle regime 后恢复；新操作点稳定后 Codex 重新有效 |

工作解释：

```text
Human Codex stable -> AlphaGo shock raises reuse/attention -> AI diffusion disrupts old Codex -> new operation point stabilizes
```

这比“AI 后历史 Codex 失效”更细。E2 显示退化，E3 显示重新沉积。E2→E3 recovery 为 `+0.076 bits`，与 Phase 1/2 的“操作点位移后重新稳定”叙事一致。

## 4. Feature-wise E3 结果

E3 中按 AI-alignment 维度分层：

| E3 position type | Predictive cost | 解释 |
|------------------|-----------------|------|
| 高 AI 对齐位置 | 9.700 bits | 更可预测 |
| 低 AI 对齐位置 | 9.850 bits | 较不可预测 |

差值：

```text
AI-aligned positions are ~0.15 bits more predictable
```

相关：

```text
rho ≈ -0.04
```

解释：

> Codex 在 AI 对齐维度上预测更好，但逐位置相关很弱。

这支持“选择性收敛”而不是“AI alignment 单变量解释全部预测力”。AI 对齐让局面更可预测，但它只是局部贡献，不是总因果。

## 5. 效应量解释

`+0.120 bits/move` 不能与 DSG 的 `Δ≈0.71` 直接比较。

| 系统 | 选择空间 | 可期待增益 |
|------|----------|------------|
| 密码子后继 | 64 codons / 强生物约束 | 较大 |
| 围棋下一手 | 棋盘高分支、局面依赖、战略自由度高 | 较小 |

围棋每一步的可选空间天然远大于密码子后继，且同一局面附近存在大量策略上可接受的候选手。因此 Codex 增量不会像 DSG 那样大。稳定的 `+0.120 bits/move` 更接近“自然符号生态中的弱但持续选择沉积”。

## 6. 为什么这是 Codex operation

GameCodex 三阶段对应：

| EE 环节 | GameCodex 证据 |
|---------|----------------|
| Formation | 历史棋谱形成局面/棋步 Codex |
| Selection | 胜负、采用、AI 时代操作点筛选 Codex |
| Operation | Codex 在 held-out 年份提高棋步预测 |

Phase 3 的最小闭环：

```text
games <= year t
  -> build Human Codex
  -> predict year t+1 moves
  -> compare Frequency and Recency baselines
  -> Human Codex wins vs Frequency in 22/22 years
  -> Human Codex wins vs Recency in 19/22 years
```

这使 GameCodex 从结构读数推进到 operation 读数。

加强基线后的关键点：

> 全史胜过近期。长期 Codex 沉积比短期流行趋势更重要。

## 7. 当前边界

| 边界 | 处理 |
|------|------|
| 结果仍需归档 | 需归档脚本、样本量、split、baseline 定义 |
| 已加入 recency | 下一步加入 win-rate、player-strength、AI-policy baselines |
| 效应小 | 不夸大；重点放在 22/22 与 19/22 的方向稳定 |
| AI alignment 相关弱 | 不声称 AI alignment 单独解释 Codex gain |
| 高/低 AI 对齐差异需复核 | 需报告分层阈值和 bootstrap CI |

## 8. 下一步

1. 归档 stronger-baseline 脚本与输出。
2. 继续加入 win-rate、player-strength、AI-policy baselines。
3. 对 `Hist > Recency` 做更多 split / threshold 稳健性检验。
4. 对 E2 低谷和 E3 恢复做时间线复核。
5. 结合 Phase 0.5 长历史基线，判断 E2/E3 是否超出历史 drift envelope。
6. 将 feature-wise Δ 与 Phase 2 的选择性收敛维度对齐。

## 9. 里程碑句

GoCodex Phase 3 的初步结论：

> 历史局面 Codex 在 22/22 个 held-out 年份中超过全局 frequency baseline，并在 19/22 年中超过 recency baseline。全史比近期更强，说明长期模式比短期趋势更重要。AI 扩散期 Human Codex 短暂退化，随后在新操作点稳定后恢复。GameCodex 因此完成了自然符号生态中的 Codex operation 加强基线闭合。
