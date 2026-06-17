# Phase 0.6 — CWI Archive Composition Audit

**日期:** 2026-06-14  
**状态:** 数据媒介层基线闭合。  
**结论:** 区域风格距离存在长期收敛，但没有明显 AI-era 加速；更重要的信号是 CWI 数据库自身从日本档案转为跨国棋谱流通网络。

---

## 1. 问题

Phase 0.5 已经显示 AI-era drift 没有突破历史封套。Phase 0.6 进一步检查：

> 长历史 envelope 到底是棋风变化，还是棋谱流通与数据库构成变化共同沉积出的外部记忆结构？

这一步不是普通数据清洗。对 GameCodex 来说，数据库本身也是 Codex 外置化的一部分。

## 2. 区域距离

区域距离显示长期收敛：

```text
long-term regional convergence slope = -0.0025 / year
```

但这个趋势从 1970s 就已经开始，并非 AI 后突然出现。

```text
2010s regional distance = 0.0085
2020s regional distance = 0.0082
```

解释：

> AI 后没有明显加速区域风格收敛。

因此，区域距离不支持“AI 造成跨区域风格突然趋同”的强叙事。

## 3. CWI 数据库构成变化

真正有信息量的是 CWI 数据自身的地域构成。

| Decade | JPN | KOR | CHN |
|--------|--------:|-------:|------:|
| 1950s | 58,371 | 0 | 0 |
| 1980s | 336,450 | 35 | 0 |
| 2000s | 320,158 | 37,730 | 140 |
| 2020s | 426,114 | 57,453 | 7,245 |

这不是一个简单的“风格趋同”问题。CWI 的观测对象本身在变化：

```text
Japanese archive
  -> Japan-dominated professional record
  -> transnational go record with visible Korea/China streams
```

中韩棋谱从零到万的过程，是 Codex 流通结构变迁的化石证据。

## 4. 解释

区域距离长期收敛可以来自多种机制：

1. 职业围棋制度和训练方法趋同。
2. 跨国赛事、报刊、棋书、数据库和互联网扩大了共享谱系。
3. CWI 数据库的收录范围从日本中心扩展为跨国流通网络。
4. AI oracle 后期加入这一流通链，但不是收敛的起点。

因此，不能把区域距离收敛直接解释为“棋风趋同”。更稳妥的解释是：

> 棋谱数据库记录的是风格变化和流通结构变化的混合物。

对 EE 来说，这不是缺陷，而是一个更深的读数：外部 Codex 不只改变棋手选择，也改变哪些选择能被保存、传播、检索和再使用。

## 5. 与 Phase 0.5 的关系

Phase 0.5 的历史 envelope 仍然有效，但它应该被表述为：

> CWI 所代表的职业棋谱流通网络中的 historical envelope。

这比“全球围棋整体历史 envelope”更准确。

Phase 0.6 给 Phase 0.5 加了一层媒介限定：

| 层级 | Phase 0.5 | Phase 0.6 |
|------|-----------|-----------|
| 棋步层 | AI-era drift 在历史封套内 | 区域距离长期收敛，无明显 AI 加速 |
| 数据层 | CWI 可给出长历史参照 | CWI 自身从日本档案变成跨国流通网络 |
| EE 含义 | AI 是长期外置化连续阶段 | 数据库构成变化本身也是 Codex 外置化化石 |

## 6. 对后续分析的约束

后续 GameCodex 必须显式区分两类问题：

1. **Move-choice effect:** 棋手在相同观测网络内是否改变下法。
2. **Archive-composition effect:** 哪些地区、棋手、赛事和年代进入了数据库。

若不区分二者，区域差异、年度 drift 和 novelty 都可能把收录结构误读为棋风结构。

最小控制策略：

1. 报告每个 decade 的地域构成。
2. 将主要结果在 Japan-only 或 region-balanced 子集上复核。
3. 把全库结果称为 CWI-network result，而不是 global go result。
4. 在论文叙事中把 CWI 构成变化作为发现，而不是只作为 bias 删除。

## 7. 里程碑句

GameCodex Phase 0.6 的结论：

> 区域风格距离从 1970s 起长期收敛，AI 后没有明显加速；但 CWI 数据库自身从日本档案扩展为跨国棋谱流通网络。中韩棋谱从零到万的过程，是围棋 Codex 外部记忆结构变迁的化石证据。
