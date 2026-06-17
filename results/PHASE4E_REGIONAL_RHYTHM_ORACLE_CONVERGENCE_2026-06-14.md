# Phase 4E — Regional Rhythm & Oracle Convergence

**日期:** 2026-06-14  
**状态:** 区域 rhythm 结果闭合。  
**结论:** AI 不是简单抹平区域风格。它先造成共同收敛冲击，再放大各区域对 AI 的不同吸收方式，最后在 Oracle Codex 稳定后再次收敛。

---

## 1. 问题

Phase 4A-D 已经说明：

```text
historical envelope -> AI 在封套内，不是断裂
archive control -> 信号在棋步里，不在档案构成里
pattern adoption -> AI 改变 Codex 传播速度
```

Phase 4E 进一步追问：

> AI 对区域棋风的影响，是抹平差异，还是改变不同区域吸收 Codex 的路径？

## 2. 区域 Rhythm 签名

1990-2015 的区域 rhythm 签名显示，日本、韩国、中国有清晰可分的操作点。

| Region | N | adj_opp | is_corner_open | dist_last | 解释 |
|--------|------:|--------:|---------------:|----------:|------|
| JPN | 949K | 0.1421 | 0.1326 | 0.1794 | 厚实 / 地域型 |
| KOR | 95K | 0.1454 | 0.1422 | 0.1825 | 战斗 / 灵活型 |
| CHN | 18K | 0.1484 | 0.1464 | 0.1834 | 战斗 + 高机动型 |

解释：

1. 日本最不贴对手，最少开新角，步伐最连贯。
2. 韩国比日本更贴对手，也更灵活。
3. 中国在韩国基础上更极端，呈现更高的战斗和机动倾向。

这说明区域差异不是噪声，而是可以在 SHP rhythm 空间中读出的 Codex 操作点。

## 3. AI 三阶段区域距离

区域间距离呈现三阶段结构：

| Era | Regional distance | 解释 |
|-----|------------------:|------|
| 1990s | 0.0186 | 最分散：三个独立传统 |
| 2016-17 | 0.0070 | 最收敛：AlphaGo 冲击下共同震荡 |
| 2018-21 | 0.0121 | 重新分化：各自吸收 AI，韩国战斗精神达到顶峰 |
| 2022-25 | 0.0065 | 再次收敛：Oracle Codex 稳定 |

这不是单调趋同，而是：

```text
independent traditions
  -> shock convergence
  -> differentiated absorption
  -> oracle stabilization
```

## 4. 韩国战斗指数

韩国的战斗指数给出最清晰的区域机制读数。

| Era | Combat index | 解释 |
|-----|-------------:|------|
| 1990s | +0.018 | 李昌镐时代：最“日本化” |
| 2008-15 | +0.027 | 李世石巅峰 |
| 2018-21 | +0.038 | AI 扩散期：战斗精神达到历史最高 |
| 2022-25 | +0.032 | Oracle 时代：开始回落 |

AI 最初没有抹平韩国风格，而是放大了韩国的战斗倾向。到 Oracle Codex 稳定后，这种极化才开始回落。

## 5. 与 Phase 3 的独立对应

区域三阶段与 Phase 3 的 Codex Δ 年代波动完全对应：

| Phase 3 | 区域视角 | 解释 |
|---------|----------|------|
| E1 peak | 2016-17 区域距离最低 | AlphaGo shock 造成共同收敛 |
| E2 trough | 2018-21 区域重新分化 | 各区域开始以自身风格吸收 AI，历史 Codex 暂时退化 |
| E3 recovery | 2022-25 再次收敛 | Oracle Codex 稳定，新操作点重新沉积 |

因此，Phase 4E 独立验证了 Phase 3 的核心模式：AI 扩散不是立即稳定的新均衡，而是先冲击、再分化、再沉积。

## 6. 对主叙事的修正

Phase 4D 的主句是：

> AI 没有重写围棋的棋步结构——它重写了围棋 Codex 被发现、传播和锁定的速度。

Phase 4E 增加区域层的修正：

> AI 也没有简单抹平区域风格；它先制造共同震荡，再放大区域性吸收，最后让 Oracle Codex 稳定收敛。

合并后的叙事是：

```text
global structure: within historical envelope
archive structure: CWI is a codex flow fossil
operation structure: codex predicts future adoption
speed structure: AI accelerates discovery and lock-in
regional structure: shock -> differentiated absorption -> oracle stabilization
```

## 7. 边界

1. 区域标签来自 CWI 赛事 / 来源 / 地域分类，仍需在 metadata 层复核。
2. 中国样本量 (`N=18K`) 小于日本和韩国，应避免过度解释绝对强度。
3. 韩国战斗指数是 rhythm proxy，不等于完整棋风描述。
4. 仍需要 player-level network 区分“区域风格”与“少数顶尖棋手影响”。

## 8. 下一步

1. 将区域 rhythm 三阶段与 Phase 3 Codex Δ 画成同一张 era-alignment 图。
2. 做 player-level decomposition：李昌镐、李世石、朴廷桓、申真谞等是否驱动韩国曲线。
3. 对中国样本做年代与赛事分层，检查 `N=18K` 的稳定性。
4. 将 regional distance 与 pattern adoption lag 关联，检查速度革命是否先从某一区域出现。

## 9. 里程碑句

Phase 4E 的结论：

> AI 没有简单抹平围棋区域风格。AlphaGo shock 先让区域 rhythm 瞬间收敛，AI diffusion 期又放大各区域的吸收差异，其中韩国战斗指数达到历史最高；到 Oracle Codex 稳定后，区域距离才再次收敛。这从区域视角独立验证了 Codex Δ 的 E1 峰值、E2 低谷和 E3 恢复。
