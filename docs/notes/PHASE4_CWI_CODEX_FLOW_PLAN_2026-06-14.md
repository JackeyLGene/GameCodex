# Phase 4 — CWI Codex Flow & Archive Network

**日期:** 2026-06-14  
**状态:** 工作计划。由 Phase 0.5 / 0.6 推导出的下一实证阶段。  
**目标:** 从“AI 是否造成断裂”转向“棋谱 Codex 如何在外部记忆网络中流通、保存、重组和被再次读取”。

---

## 1. 战略定位

Phase 0.5 显示：

```text
AI-era drift (2010s -> 2020s): |drift| = 0.0130
pre-2016 historical envelope:  0.0146 ± 0.0098
Z-score:                       -0.16
```

AI-era shift 位于历史封套内，不是围棋 Codex 的断裂开端。

Phase 0.6 进一步显示：

```text
regional distance slope: -0.0025 / year
2010s -> 2020s:          0.0085 -> 0.0082
```

区域距离从 1970s 起长期收敛，AI 后没有明显加速。真正关键的是 CWI 数据库自身的构成变化：

| Decade | JPN | KOR | CHN |
|--------|--------:|-------:|------:|
| 1950s | 58,371 | 0 | 0 |
| 1980s | 336,450 | 35 | 0 |
| 2000s | 320,158 | 37,730 | 140 |
| 2020s | 426,114 | 57,453 | 7,245 |

因此，Phase 4 不再把 CWI 当作透明窗口，而是把 CWI 本身作为外部 Codex 流通网络的沉积物。

一句话：

> Phase 4 研究的不是“棋风有没有变”，而是“哪些棋谱进入了可被读取的 Codex，以及这些进入如何改变未来可预测性”。

## 2. 核心问题

Phase 4 回答五个问题：

1. Phase 0.5 / Phase 1 / Phase 3 的结果在 `Japan-only`、`region-balanced` 和 `CWI full network` 三种读法中是否一致？
2. `1910s -> 1920s` 最大漂移是棋步结构变化，还是收录结构变化？
3. 中韩棋谱进入 CWI 后，带来的是新 pattern，还是放大已有 pattern 的计数？
4. 局部 pattern 的 adoption、survival 和 cross-region lag 是否构成可测的 Codex operation？
5. KataGo alignment 的选择性吸收是否在 region-controlled 子集中仍然存在？

## 3. 数据层

Phase 4 需要把棋谱分成三层读数：

| 层级 | 读数 | 目的 |
|------|------|------|
| Archive composition | `region/year/player/event/source` | 判断数据库构成是否在变 |
| Move-choice structure | `chroma/rhythm/prefix/hash` | 判断棋步结构是否在变 |
| Codex flow | `first_seen/adoption/survival/cross_region_lag` | 判断 pattern 如何传播和沉积 |

这三层不能混在一起。全库结果统一称为 `CWI-network result`，不称为 `global go result`。

## 4. 工作包

### Phase 4A — Archive Composition Matrix

目标：建立 `decade × region × player × event × source` 的数据构成矩阵。

输出：

| 输出 | 内容 |
|------|------|
| `archive_composition_by_decade.csv` | 每十年地域、赛事、棋手构成 |
| `region_share_timeline.csv` | JPN/KOR/CHN 占比时间线 |
| `coverage_breaks.md` | 记录明显收录断点 |

核心读数：

- region share
- unique players
- event count
- games per player
- source coverage
- region entropy

### Phase 4B — Region-Controlled Replication

目标：复核现有结论是否依赖 CWI 构成变化。

三个版本：

| 版本 | 定义 | 解释 |
|------|------|------|
| Full CWI | 使用全库 | CWI-network result |
| Japan-only | 只用日本棋谱 | 长期连续档案控制 |
| Region-balanced | 每 decade 按地区下采样或加权 | 地域构成控制 |

复核对象：

1. Phase 0.5 decade drift envelope。
2. Phase 1 chroma-rhythm coupling and rhythm shift。
3. Phase 3 Human Codex > frequency / recency。
4. Phase 2 `adj_opp/adj_own/dens_delta` KataGo selective alignment。

解释规则：

| 结果 | 解释 |
|------|------|
| Full + controlled 都成立 | 棋步层 Codex 结构稳健 |
| Full 成立、controlled 消失 | 主要是 archive-composition effect |
| controlled 成立、Full 更强 | 流通网络放大了真实棋步信号 |
| 全部消失 | 退回数据描述，不声称 operation |

### Phase 4C — 1910s -> 1920s Decomposition

目标：拆解长历史中最大漂移。

候选原因：

1. 日本职业制度和赛事记录变化。
2. 报刊/棋书传播扩大。
3. 布局和定式整理造成真实棋步变化。
4. CWI 收录结构或样本量断点。

最小检验：

| 检验 | 判别 |
|------|------|
| composition drift vs move drift | 构成变化能否解释最大漂移 |
| same-region/same-event subset | 是否仍有 1910s->1920s drift |
| player overlap control | 是否由棋手群体更替驱动 |
| opening/rhythm split | 漂移来自开局路径还是空间节奏 |

结论目标不是写历史解释，而是给 `AI is not the largest event` 一个可审计锚点。

### Phase 4D — Pattern Adoption & Survival

目标：从“年度 drift”进入“Codex 流通”。

pattern 可以先用无语义编码：

| Pattern | 定义 |
|---------|------|
| opening prefix | 前 N 手序列或规范化 hash |
| local patch | 落子周围局部棋形 hash |
| rhythm state | `chroma × rhythm` 离散状态 |
| transition | `state_t -> move_{t+1}` |

核心读数：

| 读数 | 定义 |
|------|------|
| first_seen | pattern 首次出现年份 |
| adoption_lag | 首次出现到跨玩家/跨地区复用的时间 |
| survival_half_life | pattern 使用率衰减到一半的时间 |
| cross_region_lag | 从一个地区到另一个地区的传播延迟 |
| reuse_rate | 后续年份重复采用率 |
| Codex Δ | 历史 pattern 是否提高未来采用预测 |

这一步最接近 GameCodex 的主命题：

> Codex 不是静态谱库，而是能改变未来读取概率的外部记忆结构。

### Phase 4E — Player / Region Propagation Network

目标：把棋谱看成传播网络，而不是独立样本。

节点：

- region
- player
- event
- pattern

边：

- player reuses pattern
- region imports pattern
- event amplifies pattern
- AI-era pattern receives policy support

读数：

| 读数 | 解释 |
|------|------|
| source centrality | 哪些地区/棋手更像 pattern 源头 |
| sink centrality | 哪些地区/棋手更像 pattern 吸收者 |
| cascade size | pattern 传播规模 |
| cascade speed | pattern 扩散速度 |
| post-AI acceleration | AI 后传播是否变快 |

如果成立，Phase 4 可以把“中韩棋谱进入 CWI”从数据偏倚提升为流通网络重组。

### Phase 4F — KataGo Historical Replay

目标：给 Phase 2 的选择性吸收加历史坐标。

抽样策略：

| 样本 | 目的 |
|------|------|
| 1910s / 1920s | 最大历史漂移对照 |
| 1970s / 1980s | 最稳定期对照 |
| 2010s / 2020s | AI-era 对照 |
| Japan-only / balanced | 地域控制 |

问题：

1. 老棋手是否已经偶然接近现代 AI policy？
2. AI alignment 的上升是否只发生在 `adj_opp/adj_own/dens_delta`？
3. `dist_last/is_corner_open` 的独立性是否在控制地区后仍存在？
4. AI 后收敛是否是棋步选择变化，而不是数据库构成变化？

## 5. 最小实现顺序

1. 建立 `archive_composition_by_decade.csv`。
2. 做 `Japan-only` 与 `region-balanced` 的 Phase 0.5 drift 复核。
3. 拆解 `1910s -> 1920s` 最大漂移。
4. 用 opening prefix / rhythm state 定义第一版 pattern。
5. 跑 adoption lag / survival half-life。
6. 把 Phase 3 held-out Codex 改成 pattern adoption 预测。
7. 小样本 KataGo historical replay。

## 6. 停止规则

| 停止条件 | 处理 |
|----------|------|
| Full CWI 信号无法在任何控制子集复现 | 不声称棋步层发现，改写为 archive-flow finding |
| 1910s->1920s 完全由样本构成解释 | 不写历史棋风断点，只写收录网络变化 |
| pattern adoption 无 held-out 增益 | 不声称 Codex operation，只报告流通描述 |
| KataGo replay 无选择性吸收 | 保留 Phase 2 为初步结果，不进入强 AI 叙事 |
| 地域/赛事 metadata 不足 | 降级为 decade-level CWI-network 分析 |

## 7. 预期图表

| 图 | 内容 |
|----|------|
| Fig 1 | CWI region composition timeline |
| Fig 2 | Full vs Japan-only vs region-balanced drift envelope |
| Fig 3 | 1910s->1920s decomposition |
| Fig 4 | pattern adoption lag and survival half-life |
| Fig 5 | region/player pattern propagation network |
| Fig 6 | KataGo historical replay by feature axis |

## 8. 成功标准

Phase 4 成功不要求证明 AI 是断裂。成功标准是：

1. 明确区分 move-choice effect 与 archive-composition effect。
2. 判断现有 GameCodex 信号是否依赖 CWI 地域构成。
3. 将中韩棋谱进入 CWI 的过程量化为 Codex 流通网络变化。
4. 给 pattern adoption / survival 建立 held-out operation 检验。
5. 给 Phase 5 论文骨架提供稳健边界。

## 9. 里程碑句

Phase 4 的目标句：

> CWI 不是围棋历史的透明窗口，而是围棋 Codex 外部记忆网络的沉积物。Phase 4 将区分棋步选择变化与档案构成变化，并检验 pattern 如何在地区、棋手和年代之间被保存、传播、淘汰和再次读取。
