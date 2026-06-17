# AI Rewrote the Speed, Not the Structure, of Go Codex Evolution

**Target:** PNAS
**Status:** Phase 5 skeleton draft. 2026-06-14.
**Core claim:** AI did not rewrite the move structure of professional Go;
it rewrote the speed at which the Go Codex is discovered, transmitted, and
locked in.

---

## Significance Statement

Analyzing 95,000 professional Go games spanning four centuries through a
chroma-rhythm decomposition of move geometry, we find that the AI era
(2016-present) did not alter the fundamental coupling between game phase and
spatial choice. Instead, it accelerated the speed at which new opening
patterns are adopted (4.2× faster) and locked in (2.2× stickier). The
three-phase regional dynamics—shock convergence, divergent absorption, oracle
re-stabilization—independently validate this pattern. Our findings establish a
quantitative framework for measuring how external oracles reshape cultural
Codex evolution without rewriting its structural grammar.

## Abstract

The advent of superhuman AI in Go (AlphaGo, 2016) has been widely described as
a rupture in millennia-old playing traditions. Using a dataset of 95,000
professional games from 1600-2026, we decompose each move into orthogonal
chroma (game-phase) and rhythm (spatial-relation) axes, measuring cross-harm
coupling across four centuries. We find that the AI era did not alter the
chroma-rhythm coupling structure—the AI-era drift magnitude (0.013) lies
within the pre-2016 historical envelope (0.015 ± 0.010). What the AI era did
change was Codex circulation speed: adoption lag for new opening patterns fell
from 6.3 years (pre-1980) to 1.5 years (post-2016), and reuse rates rose from
0.35 to 0.78. Selective convergence toward KataGo policy is observed on
opponent-proximal features (adj_opp, dens_delta) but not on pacing or corner
strategy. Regional dynamics reveal a three-phase response—shock convergence
(2016-17), divergent absorption (2018-21), and oracle re-stabilization
(2022-25)—independently validating the Codex destabilization-and-recovery
model. Our results establish that external oracles reshape cultural evolution
not by rewriting structural grammar but by accelerating the discovery,
transmission, and locking of new patterns within existing structural
constraints.

---

## 1. Introduction

The 2016 victory of AlphaGo over Lee Sedol was widely interpreted as a
watershed moment—not only for artificial intelligence but for human culture.
Professional Go players rapidly adopted AI-influenced strategies, leading to
widespread claims that "AI has rewritten Go." But has it? And if so, what
exactly was rewritten: the structural grammar of move choice, or the speed at
which new moves are discovered and adopted?

These two possibilities are confounded in qualitative accounts. A novel move
may reflect a genuine restructuring of the space of play, or simply the faster
circulation of innovations that would have emerged under any sufficiently
connected information network. Disentangling them requires (a) a structural
encoding of move geometry that separates game-phase from spatial-choice, (b) a
century-scale baseline against which to measure deviation, and (c) a method
for tracking pattern adoption speed independent of pattern content.

We address all three. We decompose every move in 95,000 professional Go games
(1600-2026) into orthogonal chroma (game-phase) and rhythm (spatial-relation)
dimensions, an approach derived from Saussurean Hash Projection (SHP). We
construct a pre-2016 historical drift envelope from century-scale decade
drift. And we define a pattern-level Codex operation metric that measures how
historical pattern frequency predicts future adoption, independent of what the
pattern is.

## 2. Results

### 2.1 AI-era drift lies within the historical envelope

We computed decade-to-decade rhythm centroid drift across four centuries.

```
Pre-2016 decade drift: mean |drift| = 0.0146 ± 0.0098
AI-era (2010s → 2020s): |drift| = 0.0130
Z-score: -0.16
```

The largest drift in Go history was 1910s→1920s (|drift|=0.034, 2.6× the
AI-era magnitude), corresponding to the institutionalization of professional
Go through the Oteai ranking system and the founding of the Nihon Ki-in
(1924). AI is not the most structurally disruptive event in Go history.

Five rhythm dimensions were examined. None exceeded the pre-2016 95% envelope,
with is_corner_open approaching but not crossing the boundary (Z = +1.42,
marginal). Adjacency to opponent stones (adj_opp, d = +0.0075), self-extension
(adj_own, d = +0.0005), local density pressure (dens_delta, d = -0.0043), and
pacing (dist_last, d = -0.0010) all remained within historical norms.

### 2.2 Selective convergence toward AI policy

We compared human move choices with KataGo policy recommendations across 200
sampled positions (50 per era). The overall human-KataGo rhythm gap did not
change across eras (d(E0 vs E3) = -0.008). However, feature-level analysis
revealed selective convergence: three of five rhythm dimensions showed E3
moves moving closer to KataGo preferences (adj_opp: E3 d = -0.016 vs E0
d = -0.220; adj_own: E3 d = +0.007 vs E0 d = -0.209; dens_delta: E3
d = -0.043 vs E0 d = +0.216). The other two dimensions (dist_last,
is_corner_open) showed divergence. Professional players selectively absorbed AI
preferences on opponent-proximal fighting dimensions while maintaining
independent pacing and corner strategies.

### 2.3 Pattern adoption accelerated 4.2× in the AI era

We tracked 74,501 unique opening patterns (first 15 moves) across 546
qualifying patterns appearing in ≥3 years.

```
                    pre-1980  1980-1999  2000-2015  2016+
Adoption lag (yr):     6.3       5.7        2.6      1.5
Reuse rate:           0.35      0.37       0.67     0.78
Half-life (yr):        1.1       1.1        1.0      1.1
```

Adoption lag decreased from 6.3 years (pre-1980) to 1.5 years (post-2016), a
4.2× acceleration. Reuse rate—the fraction of years a pattern persists once
introduced—increased from 0.35 to 0.78, indicating 2.2× stronger pattern
lock-in. Pattern half-life remained approximately 1.1 years across all eras,
suggesting that while adoption and locking changed dramatically, the basic
lifecycle of a Go pattern remained stable.

### 2.4 The archive is not a transparent window

The dataset we use (CWI Professional Go Archive) is itself a product of
Codex circulation. Korean and Chinese games were essentially absent before the
1990s:

| Decade | JPN | KOR | CHN |
|--------|-----|-----|-----|
| 1950s | 58,371 | 0 | 0 |
| 1980s | 336,450 | 35 | 0 |
| 2000s | 320,158 | 37,730 | 140 |
| 2020s | 426,114 | 57,453 | 7,245 |

To verify that our findings are not artifacts of archive composition, we
replicated all drift analyses on a Japan-only subset (N = 426K+). The
Japan-only drift magnitude (0.0159) was nearly identical to the full-archive
value (0.0160). The signal is in the moves, not in the archive composition.

### 2.5 Two revolutions, two mechanisms

The 1910s→1920s drift (the largest in our record) decomposed into 85% overlap
contribution—players who appeared in BOTH decades showed 85% of the total
drift magnitude. This was a true playing-style shift driven by institutional
reorganization (Oteai professional ranking, Nihon Ki-in founding). The
2010s→2020s drift, in contrast, occurred within a stable institutional
framework, driven by external oracle alignment. Both produced ~0.03 drift
magnitude but through fundamentally different Codex mechanisms: one through
institutional reorganization, the other through oracle acceleration.

### 2.6 Regional dynamics independently validate the three-phase model

Inter-region rhythm distance across Japan, Korea, and China reveals a
three-phase response:

```
1990s (pre-AI):        0.0186  (three independent traditions)
2016-17 (AlphaGo shock): 0.0070  (convergence—everyone froze)
2018-21 (AI diffusion):  0.0121  (re-divergence—asymmetric absorption)
2022-25 (oracle era):    0.0065  (re-convergence as Codex stabilizes)
```

Korea's "fighting index" (adj_opp − adj_own) peaked during AI diffusion
(2018-21: +0.038), not during the pre-AI Lee Sedol era (2008-15: +0.027). AI
initially amplified national stylistic signatures before the oracle era pulled
them toward the global mean. This three-phase pattern—shock convergence,
divergent absorption, oracle re-stabilization—independently replicates the
Codex Δ pattern from held-out prediction analysis (E1 peak → E2 dip → E3
recovery).

## 3. Discussion

Our findings resolve an apparent paradox in the cultural impact of AI on Go.
Qualitatively, players, commentators, and the public uniformly report that AI
has "changed everything." Quantitatively, the move-level structural drift of
the AI era lies squarely within the century-scale historical envelope. The
resolution is that what changed was not the structure of move choice, but the
speed of Codex circulation.

This distinction matters beyond Go. It suggests a general property of external
oracles in cultural evolution: they accelerate the discovery-transmission-locking
cycle without necessarily rewriting the underlying structural grammar. The
grammar—chroma-rhythm coupling—is constrained by the geometry of the board and
the deep structure of the game. What an oracle can do is reduce search costs,
enabling faster pattern discovery and stronger lock-in once a pattern is
validated.

The three-phase regional dynamics further suggest that oracle adoption follows
a characteristic destabilization-recovery trajectory: initial convergence
under shock, followed by a period of asymmetric absorption where pre-existing
stylistic signatures are temporarily amplified, culminating in a new
equilibrium where Codex stability returns but at a permanently higher
circulation speed.

Four limitations should be noted. First, our dataset is Japan-dominant; while
Japan-only replication validates the main signal, Korean and Chinese samples
remain underpowered. Second, our pattern definition (15-move opening prefixes)
captures only one level of Go strategy. Third, the KataGo analysis was
performed on a limited sample (200 positions). Fourth, player-level confounds
(Korea's signal may be driven by a few dominant players) require further
control.

## 4. Methods Summary

**Data:** CWI Professional Go Archive, 95,000+ SGF records, 1600-2026.
**Encoding:** SHP chroma-rhythm decomposition. Chroma = game-phase position
(move index, board occupancy, phase bin). Rhythm = spatial relation to
existing stones (adjacency, density, distance, corner proximity). Five
dimensions per move.
**Codex Operation:** Held-out prediction of moves from historical position
frequency, compared against frequency and recency baselines. Sign test and
bootstrap CI for statistical validation.
**Pattern Analysis:** 15-move opening prefixes as pattern keys. Adoption lag
= years from first appearance to ≥3 unique players. Reuse rate = fraction of
years between first and last appearance with active usage.
**Regional Classification:** Event-name keyword matching for JPN/KOR/CHN.
Japan-only replication controls for archive composition.
**KataGo Analysis:** OpenCL v1.16.4, b20c256x2 network, 200 visits/position.

## 5. Figures

| Figure | Content |
|--------|---------|
| Fig 1 | Chroma-rhythm encoding schematic + data overview |
| Fig 2 | Decade drift envelope + AI-era position (Phase 0.5) |
| Fig 3 | Feature-wise KataGo alignment (Phase 2) |
| Fig 4 | Pattern adoption lag and reuse rate by era (Phase 4D) |
| Fig 5 | Regional inter-distance three-phase trajectory (Phase 4E) |
| Fig 6 | Korea fighting index + Japan-only replication |

## 6. Defense Analyses (Review-Ready)

- [ ] Pattern prefix length robustness (10/15/20 moves)
- [ ] Player-level control for Korea fighting index
- [ ] Region label audit with manual spot-check
- [ ] Bootstrap CI on 4.2×, 2.2×, and regional distances
- [ ] KataGo historical replay (supplementary)
