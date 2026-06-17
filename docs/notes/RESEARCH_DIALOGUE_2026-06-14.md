# Research Dialogue — GameCodex Direction

**日期:** 2026-06-14  
**性质:** 对话沉淀。记录 GameCodex 从方法论转向到围棋 SHP / KataGo 选择性收敛的关键判断。  
**用途:** 保留研究动机、概念转折和当前叙事边界，避免后续只剩指标而丢失问题意识。

---

## 1. 从生物线封口到新实验域

生物线以负结果收束后，一个核心判断被固定下来：

> EE 的方法是符号学基底的。符号层越纯，方法越锋利；现实耦合越厚，越需要稳定缓冲环节。

生物线不是“直觉错误”，而是发表支撑不足。疾病/失败模式直觉保留为 hypothesis reserve；但当前读数不能直接承担疾病机制或湿实验因果的论文重量。

这迫使下一阶段从“再找一个大领域”转为“寻找 Codex operation 的自然实验域”。

## 2. 为什么转向棋类

几个候选被筛掉或降级：

| 候选 | 主要问题 |
|------|----------|
| 私人代码 | 公开性和可复核性不足 |
| 市场 | 已在经济学线同步推进 |
| 法律/协议 | 符号性强，但结果变量难以定量 |
| 数字生命/哥德尔流 | 已与经济学/仿真线重合 |
| 语言学 | 已有很多发现，但语义污染和发表问题仍重 |

棋类满足 GameCodex 所需的条件：公共、符号化、规则封闭、有代际继承、有选择压力、有稳定执行缓冲层。

围棋尤其有话题度，因为顶尖棋手对 AI 时代有明确体感：“比赛变成了背 AI 谱子”。这个体感可以被操作化，而不是停留在评论层。

## 3. 核心问题的重写

最初问题：

> AI 是否改变了围棋？

被重写为：

> 围棋开局/定式如何把 AI 外部 Codex 吸收到既有的人类代际 Codex 中？

进一步收紧为：

> AI Codex 是否在特定 rhythm 维度上提供 held-out 增益，而不是全局替代人类棋风？

这一路径让 GameCodex 不再只是“AI 影响围棋”的重复研究，而是 EE 的 Codex operation 缺口实验。

## 4. SHP 编码对话

关键编码判断来自 SHP：

```text
每手棋 = (chroma, rhythm)
```

| 轴 | 含义 | 围棋化解释 |
|----|------|------------|
| Chroma | 棋局生命周期位置 | 第几手、阶段、棋盘占用率、开局/中盘/收官 |
| Rhythm | 与在场棋子的空间关系 | 最近子距离、邻接对手、邻接己方、局部密度、是否开新角 |

这解决了普通 opening-prefix 编码的盲点：同一个坐标在不同局面中不是同一个事件。空角小目与挂角后的回应小目，在 SHP 中有不同 rhythm。

该编码保留了 EE 的差异化：不只读“下了什么”，还读“这手棋在棋局生命期的位置”和“它如何接续已有空间对话”。

## 5. Phase 1 的转折

Phase 1 初步结果：

```text
cross-harm d = -0.029
```

全局 chroma-rhythm 耦合稳定。若只看 cross-harm，似乎 AI 后没有结构变化。

但单轴读数显示强位移：

| 轴 | 结果 |
|----|------|
| `dens_delta` | d=+3.30 |
| `is_corner_open` | d=-2.54 |
| `adj_opp` | d=-1.45 |
| `adj_own` | d=+0.97 |
| `dist_near_opp` | d=+0.96 |

解释被改写为：

> AI 没有改变围棋 chroma-rhythm 的耦合结构；它改变了棋手在该耦合结构中的操作点。

这一步是 GameCodex 的第一个真正发现。它比 entropy/novelty 更细，因为它解释了为什么全局耦合不动但棋风体感改变。

## 6. Phase 2 的转折

Phase 2 KataGo alignment 初步结果：

```text
overall rhythm gap d(E0 vs E3) = -0.008
```

聚合层面仍然不变。但逐特征拆开：

| feature | E0 gap | E3 gap | 方向 |
|---------|--------|--------|------|
| `adj_opp` | -0.220 | -0.016 | 向 KataGo 收敛 |
| `adj_own` | -0.209 | +0.007 | 向 KataGo 收敛 |
| `dens_delta` | +0.216 | -0.043 | 向 KataGo 收敛 |
| `dist_last` | -0.240 | -0.444 | 更远 |
| `is_corner_open` | +0.061 | -0.337 | 更远 |

结论：

> AI 后人类在贴身对抗和密度压力维度上向 KataGo policy 收敛，但在步伐节奏和角部策略上保持独立。

这不是全面对齐，而是选择性收敛。SHP 的价值正是在这里：单一 aggregate gap 会把相反维度抵消掉；正交分解能读出被吸收的部分和保留独立的部分。

## 7. 长历史视角

下一步需要更长时间的统计视角。短时断点容易把 AI 说成凭空革命，但更好的表述是：

> AI 是围棋外部记忆史的第三次加速，而不是凭空出现的断裂。

暂定长历史时代：

| Era | 年份 | 机制 |
|-----|------|------|
| Classical Codex | 1600-1850 | 师承、棋书、流派 |
| Modern Institutional | 1850-1945 | 报刊、职业制度、头衔战 |
| Database Prehistory | 1945-1995 | 战后职业化、国际交流 |
| Internet Codex | 1995-2015 | 棋谱库、在线学习 |
| AI Shock / Diffusion | 2016-2021 | AlphaGo、Leela、KataGo |
| Oracle Regime | 2022+ | AI 谱常态化 |

Phase 0.5 已回答：

```text
AI-era drift (2010s -> 2020s): |drift| = 0.0130
Pre-2016 mean drift:           0.0146 ± 0.0098
Z-score:                       -0.16
```

AI-era shift 位于历史封套内。最大历史漂移是 `1910s -> 1920s` (`|drift|=0.034`)，约为 AI-era 的 2.6x；最高新颖度也在 1910s，而非 AI 时代。

这不是 null，而是历史定位：AI 不是围棋 Codex 演化的断裂开端，而是长期外置化过程中的一个连续阶段。

长历史基线已经进一步补上数据媒介层：

```text
regional distance slope: -0.0025 / year
2010s -> 2020s:          0.0085 -> 0.0082
```

区域距离从 1970s 起长期收敛，AI 后没有明显加速。但 CWI 数据自身发生了更重要的构成变化：

| Decade | JPN | KOR | CHN |
|--------|--------:|-------:|------:|
| 1950s | 58,371 | 0 | 0 |
| 1980s | 336,450 | 35 | 0 |
| 2000s | 320,158 | 37,730 | 140 |
| 2020s | 426,114 | 57,453 | 7,245 |

这不是“风格趋同”本身，而是 CWI 从日本档案变成跨国棋谱流通网络。中韩棋谱从零到万的过程，是 Codex 流通结构变迁的化石证据。

这已经形成 Phase 4 的工作面：

> CWI 不是围棋历史的透明窗口，而是围棋 Codex 外部记忆网络的沉积物。下一阶段要区分棋步选择变化与档案构成变化，并检验 pattern 如何在地区、棋手和年代之间被保存、传播、淘汰和再次读取。

Phase 4 文档：`docs/PHASE4_CWI_CODEX_FLOW_PLAN_2026-06-14.md`。

Phase 4A-E 后，叙事已经进一步收束：

```text
Historical baseline -> AI 在封套内，不是断裂
Archive decomposition -> CWI 是沉积物，不是透明窗
Region control -> 信号在棋步里，不在档案构成里
Mechanism split -> 1910s Oteai 制度革命 != 2020s Oracle 速度革命
Pattern flow -> adoption lag 6.3 年 -> 1.5 年，4.2x 加速
Regional rhythm -> 2016-17 shock 收敛，2018-21 分化吸收，2022-25 oracle 稳定
```

一句话：

> AI 没有重写围棋的棋步结构——它重写了围棋 Codex 被发现、传播和锁定的速度。

区域层补充一句：

> AI 也没有简单抹平区域风格；它先制造共同震荡，再放大区域性吸收，最后让 Oracle Codex 稳定收敛。

综合文档：`results/PHASE05_PHASE4_CONVERGENCE_2026-06-14.md`。
区域 rhythm 文档：`results/PHASE4E_REGIONAL_RHYTHM_ORACLE_CONVERGENCE_2026-06-14.md`。

长历史基线接下来还要回答：

1. Cross-harm 是否几百年稳定？
2. Rhythm 操作点是否长期漂移？
3. 互联网是否先改变扩散速度？
4. AI 是否超出历史漂移 envelope？
5. Phase 2 的选择性收敛是否只发生在 AI 时代？
6. Japan-only / region-balanced 子集是否复现全库结论？

## 8. 与既有研究的关系

已有研究已经覆盖“AI 影响围棋”：

| 研究方向 | 已有结论 |
|----------|----------|
| Human-AI decision gap | 人类在 AI 工具扩散后更接近 AI |
| AI training and professional performance | 职业棋手更常下出 AI 推荐手 |
| Long-history opening evolution | 围棋开局策略可作为文化演化研究对象 |

GameCodex 的差异点：

1. 不只看整体相似度或胜率质量。
2. 使用 `chroma × rhythm` 的 SHP 正交分解。
3. 解释 aggregate gap 不变的原因：维度抵消。
4. 把 AI 影响重写为 Codex operation：外部 Codex 是否在特定 rhythm 维度上改变未来选择预测。

## 9. Phase 3：Operation 初步闭合

Phase 3+ 给出了加强基线后的 Codex operation 信号：

```text
Human Codex > Frequency: 22/22 years, Δ=+0.120 bits/move, p≈0
Recency > Frequency:     22/22 years, Δ=+0.094 bits/move, p≈0
Hist > Recency:          19/22 years, p=0.000428
```

这个结果不大，但重要在稳定，并且已经排除了最简单的“近期流行度”解释。围棋每步选择空间远大于密码子后继，策略自由度也高，因此不能期待 DSG 式 `Δ≈0.71` 的强增益。GameCodex 的自然量级更像弱而持续的选择沉积。

Era 波动提供了叙事线：

| Era | Δ bits/move | 解释 |
|-----|-------------|------|
| E0 | CI [+0.082,+0.131] | Human Codex 稳定有效 |
| E1 | CI [+0.084,+0.231] | AlphaGo shock 期仍遵循历史模式 |
| E2 | CI [+0.059,+0.125] | AI diffusion 期历史 Codex 退化 |
| E3 | CI [+0.135,+0.197] | 新操作点稳定后 Codex 恢复 |

E3 feature-wise 读数显示高 AI 对齐位置更可预测约 `+0.15 bits`，但相关弱 (`ρ≈-0.04`)。这说明 AI alignment 是局部贡献，不是总解释。

这一步把 GameCodex 从结构读数推进到 operation 读数：历史棋谱沉积物不仅可描述，而且能帮助 held-out 年份预测。

最关键的新增判断：

> 全史比近期强。长期 Codex 沉积比短期流行趋势更重要。

## 10. 当前工作句

最稳的当前表述：

> 既有研究证明 AI 改变了职业围棋；GameCodex 进一步说明这种改变不是整体模仿，而是发生在可分解空间节奏维度上的选择性 Codex 吸收。AI 后人类在局部对抗/密度压力维度向 KataGo 收敛，同时在步伐节奏和角部策略上保留独立。

Phase 0.5 之后必须再补一层历史限定：

> AI 的特殊性不在总体漂移幅度，而在局部 rhythm 维度的选择性吸收。总体上，AI-era drift 位于历史封套内，是围棋 Codex 外置化长史中的连续阶段。

Phase 3 之后可补一句：

> 历史局面 Codex 在 22/22 个 held-out 年份上超过全局频率基线，并在 19/22 年上超过近期趋势基线，说明围棋开局/中盘选择中存在弱但稳定的 operation 层；AI 扩散先扰动旧 Codex，随后在新操作点上重新沉积。

## 11. 下一步

1. 归档 Long-History Baseline 脚本与数据源，特别复核 1910s->1920s 最大漂移。
2. 归档 Phase 1/2 的样本量、数据源、访问数、抽样策略。
3. Phase 3 用 feature-wise Δ bits 做 Codex operation，而不是 aggregate gap。
4. 检验 AI Codex 的 held-out 增益是否集中在 `adj_opp`、`adj_own`、`dens_delta`。
5. 若选择性吸收、长历史连续性和 Codex operation 在加强基线下同时稳健，再进入论文骨架。
