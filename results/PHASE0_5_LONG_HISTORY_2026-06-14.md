# Phase 0.5 — Long-History Baseline

**日期:** 2026-06-14  
**状态:** 长历史基线闭合。  
**结论:** AI-era rhythm drift 位于 pre-2016 历史漂移封套内。AI 不是围棋 Codex 的断裂开端，而是世纪尺度外置化演化的连续阶段。

---

## 1. 问题

Phase 1-3 已经证明 AI-era 的短时链条：

```text
Phase 1: chroma-rhythm 耦合稳定，操作点位移
Phase 2: 局部对抗/密度压力维度向 KataGo 选择性收敛
Phase 3: Human Codex operation > frequency / recency
```

Phase 0.5 要回答历史定位问题：

> AI-era shift 是否超出几百年围棋 Codex 漂移的 historical envelope？

## 2. 主结果

| 指标 | 结果 |
|------|------|
| AI-era drift (2010s -> 2020s) | \|drift\| = 0.0130 |
| Pre-2016 mean drift | 0.0146 ± 0.0098 |
| Z-score | -0.16 |

结论：

> AI-era shift is within the historical envelope.

AI 时代的总体 rhythm drift 没有突破历史封套。单个特征也未显著突破封套；`is_corner_open` 最接近，但仍不显著 (`Z=+1.42`)。

## 3. 这不是 null

该结果不是“AI 没影响”，而是给出了正确历史定位：

> AI 不是断裂，而是长期 Codex 外置化过程中的一个阶段。

Phase 1/2 读到的选择性收敛仍然成立；Phase 3 读到的 Codex operation 仍然成立。Phase 0.5 只是说明：这些变化没有超出围棋长期历史漂移范围。

## 4. 历史参照点

长历史基线显示，围棋历史上存在比 AI-era 更大的漂移。

| 读数 | 时代 | 结果 |
|------|------|------|
| 最大漂移 | 1910s -> 1920s | \|drift\| = 0.034 |
| 相对 AI-era | 1910s -> 1920s | 约为 AI-era 的 2.6x |
| 最稳定 | 1970s -> 1980s | \|drift\| = 0.004 |
| 最高新颖度 | 1910s | novelty = 0.999 |
| 最常规 | 1950s | novelty = 0.742 |

这说明 AI-era 不是围棋策略空间中最大的新颖度事件，也不是最大 rhythm 操作点漂移。

## 4.5 数据媒介层限定

Phase 0.6 的 CWI archive composition audit 显示，长历史 envelope 不能被当作透明的“全球围棋”读数。区域距离确实长期收敛 (`slope=-0.0025/year`)，但 AI 后没有明显加速 (`2020s=0.0082` vs `2010s=0.0085`)。

更关键的是，CWI 数据库自身从日本档案扩展为跨国棋谱流通网络：

| Decade | JPN | KOR | CHN |
|--------|--------:|-------:|------:|
| 1950s | 58,371 | 0 | 0 |
| 1980s | 336,450 | 35 | 0 |
| 2000s | 320,158 | 37,730 | 140 |
| 2020s | 426,114 | 57,453 | 7,245 |

因此，Phase 0.5 的准确表述是：AI-era drift 位于 **CWI 所代表的职业棋谱流通网络** 的历史漂移封套内。数据库构成变化不是需要被抹掉的噪声，而是 Codex 外部记忆结构变迁的直接证据。

## 5. Codex Operation 的长历史属性

Codex Δ 跨所有十年为正：

```text
mean Δ = +0.027
```

解释：

> Codex operation 不是 AI 时代特有现象，而是围棋历史中的普遍属性。

长期历史模式一直帮助预测未来棋步；AI 只是改变了部分操作点和局部维度的吸收方式。

## 6. 与 Phase 1-3 的关系

Phase 0.5 改写的是叙事强度，不撤回短期结果：

| Phase | 结果 | Phase 0.5 后的解释 |
|-------|------|---------------------|
| Phase 1 | cross-harm 稳定，rhythm 操作点位移 | 位移真实，但历史上并非异常幅度 |
| Phase 2 | `adj_opp/adj_own/dens_delta` 向 KataGo 收敛 | AI 影响是选择性吸收，不是全局断裂 |
| Phase 3 | Human Codex > frequency/recency | Codex operation 是长期普遍属性，AI-era 只是其中一段 |

因此，GameCodex 的最佳叙事从：

> AI 造成围棋 regime shift

收束为：

> AI 被吸收到围棋长期 Codex 演化中，并在特定 rhythm 维度上重排操作点。

## 7. 对论文叙事的影响

Phase 0.5 让结论更诚实，也更强：

1. 不再依赖“AI 革命断裂”式叙事。
2. 将 AlphaGo/KataGo 放回外置化历史：棋书、报刊、职业制度、数据库、互联网、AI oracle。
3. 把 GameCodex 的贡献定位为：用 SHP/Codex operation 读出围棋文化如何在外部记忆介质中连续沉积。
4. AI 不是开端，而是一个可测的现代阶段。

## 8. 下一步

1. 把长历史 drift envelope 与 Phase 1/2 的 feature-wise shift 合图。
2. 检查 1910s->1920s 的历史原因：现代职业制度、报刊传播、布局/定式整理、样本构成变化。
3. 对 decade-level Codex Δ 做 bootstrap CI。
4. 明确数据源地域偏倚，避免把 CWI-network result 称为“全球围棋”。
5. 在论文中把 AI 叙事降级为“continuity with selective absorption”。

## 9. 里程碑句

GoCodex Phase 0.5 的结论：

> AI-era drift 位于 pre-2016 历史封套内。AI 不是围棋 Codex 演化的断裂开端，而是长期外置化过程中的一个连续阶段；它的特殊性不在总体漂移幅度，而在局部 rhythm 维度上对 KataGo policy 的选择性吸收。
