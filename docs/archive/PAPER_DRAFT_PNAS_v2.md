# External Oracles Accelerate Cultural Codex Circulation Without Rewriting Structural Grammar

**Target:** PNAS
**Status:** v2 draft, 2026-06-15. P0/P1 fixes applied per audit.
**Core claim:** AI did not rewrite the move structure of professional Go;
it rewrote the speed at which the Go Codex is discovered, transmitted, and
locked in.

---

## Significance Statement

Using 95,000 recorded Go games spanning four centuries, we show how an
external AI system changed not what professional players could play, but how
quickly new opening patterns were discovered and stabilized in a centuries-old
cultural record. The findings establish that external oracles accelerate
cultural transmission without necessarily rewriting structural grammar.

## Abstract

The advent of superhuman AI in Go has been widely described as a rupture in
traditional playing knowledge. Using a dataset of 95,000 recorded games from
the CWI archive (1600-2026), we factorize each move into separable game-phase
and spatial-relation coordinates, measuring decade-level structural drift
across four centuries. We find that the AI-era drift magnitude (0.013) lies
within the pre-2016 historical envelope (mean 0.015 ± 0.010, 95% CI). The
largest drift in the record—1910s to 1920s (0.034)—was an institutional
revolution (Oteai professional ranking); the AI era is an oracle-speed
revolution. Observed adoption lag among qualifying recurrent opening patterns
fell from 6.3 years (pre-1980) to 1.5 years (post-2016), and reuse density
rose from 0.35 to 0.78. These structural findings are not artifacts of archive
composition: Japan-only replication preserves the full-signal drift magnitude
(0.0159 vs 0.0160). Regional event-stream dynamics reveal a three-phase
response—shock convergence (2016-17), divergent absorption (2018-21), oracle
re-stabilization (2022-25)—independently replicating the
destabilization-and-recovery pattern observed in held-out Codex operation
metrics. Our results establish that external oracles reshape cultural
evolution not by rewriting structural grammar but by accelerating the
discovery, transmission, and persistence of new patterns within existing
structural constraints.

---

## 1. Introduction

The 2016 victory of AlphaGo over Lee Sedol was widely interpreted as a
watershed moment for human culture [refs]. Professional Go players rapidly
adopted AI-influenced strategies. But did AI rewrite the structural grammar of
move choice, or did it accelerate the speed at which new moves are discovered
and adopted?

These two possibilities are confounded in qualitative accounts. Disentangling
them requires (a) a structural encoding that separates game-phase from
spatial-choice, (b) a century-scale baseline against which to measure
deviation, and (c) a method for tracking pattern adoption speed independent of
pattern content. We address all three.

## 2. Results

### 2.1 AI-era drift lies within the historical envelope

We computed decade-to-decade structural drift across four centuries using a
five-dimensional spatial-relation vector per move (adj_opp, adj_own,
dens_delta, dist_last, is_corner_open). The game-phase coordinate (chroma)
captures move index, board occupancy, and phase bin; the spatial-relation
coordinate (rhythm) captures distances, adjacencies, densities, and corner
proximity to existing stones.

```
Pre-2016 decade drift:   mean |drift| = 0.0146 ± 0.0098
AI-era (2010s to 2020s): |drift| = 0.0130
Z-score: -0.16
95% CI (pre-2016): [0.000, 0.034]
```

The AI-era drift lies well within the pre-2016 envelope. The largest drift in
our record—1910s to 1920s (|drift| = 0.034, 2.6× the AI-era magnitude)—
corresponds to the institutionalization of professional Go through the Oteai
ranking system and the founding of the Nihon Ki-in (1924). AI is not the most
structurally disruptive event in Go history.

None of the five rhythm dimensions individually exceeded the pre-2016 95%
envelope in the AI era (all Z < 1.96; is_corner_open Z = +1.42, marginally
elevated).

### 2.2 Chroma-rhythm coupling remained stable in the observed period

Phase 1 analysis of chroma-rhythm cross-harm coupling across 44,368 post-2000
games showed no global shift across AI eras (d(E0 vs E3) = -0.029). The
observed AI-era structural change is best characterized as an operating-point
shift within a stable coupling structure: both the game-phase and
spatial-relation axes shifted, but their interaction did not.

### 2.3 Selective convergence toward AI policy (Supplementary)

We compared human move choices with KataGo policy recommendations across 200
sampled positions (50 per era, ply 30). The overall human-KataGo rhythm gap
did not change across eras (d(E0 vs E3) = -0.008). Feature-level analysis
suggested selective convergence on opponent-proximal dimensions (adj_opp,
dens_delta) but not on pacing or corner strategy. We treat this result as
consistent-with the main findings but do not build the primary argument on it,
given the limited sample (see Methods, KataGo analysis used
`kata1-b28c512nbt-s13255194368-d5935380940`, maxVisits=100, Japanese rules,
komi 6.5).

### 2.4 Pattern adoption accelerated; reuse density increased

We tracked 74,501 unique opening patterns (first 15 moves) across 546
patterns meeting the qualifying threshold of ≥3 years and ≥5 uses.

```
                     pre-1980  1980-1999  2000-2015  2016+
Observed adoption lag:  6.3 yr    5.7 yr     2.6 yr   1.5 yr
Observed reuse density:  0.35      0.37       0.67     0.78
Half-life:               1.1 yr    1.1 yr     1.0 yr   1.1 yr
```

Adoption lag is measured as years from first observed appearance to first year
with ≥3 unique players, among qualifying recurrent patterns. Reuse density is
the fraction of years between first and last observed appearance in which the
pattern was actively used. These metrics are conditional on the qualifying
filter and on the observed follow-up window; post-2016 patterns have shorter
available follow-up, which may contribute to the observed lag reduction.
Pattern half-life remained approximately 1.1 years across all eras, suggesting
that while adoption and reuse changed, the basic lifecycle of a Go opening
pattern remained stable.

The findings are robust to prefix length: adoption lag acceleration is
observed at prefix 10 (9.0→1.3 yr, 6.9×), prefix 15 (6.3→1.5 yr, 4.2×), and
prefix 20 (4.1→1.4 yr, 2.9×).

### 2.5 The archive is not a transparent window

The CWI archive is itself a product of Codex circulation. True game counts
show the archive composition changed dramatically:

| Decade | JPN | KOR | CHN | Total |
|--------|-----|-----|-----|-------|
| 1950s | 1,668 | 0 | 0 | 1,868 |
| 1980s | 9,640 | 1 | 0 | 9,747 |
| 2000s | 9,198 | 1,078 | 4 | 11,111 |
| 2020s | 12,175 | 1,642 | 207 | 14,547 |

To verify that our findings are not artifacts of this composition shift, we
replicated the decade drift analysis on a Japan-only subset (the only
continuous record across all decades). The Japan-only drift magnitude (0.0159)
was nearly identical to the full-archive value (0.0160). The signal is in the
moves, not in the archive composition.

### 2.6 Two revolutions, two mechanisms

The 1910s→1920s structural drift (0.034) was decomposed by splitting games
into overlap players (20 players appearing in both decades) and non-overlap
players. Overlap players accounted for 85% of the total drift magnitude
(0.0291 of 0.0342), indicating a true playing-style shift rather than mere
roster turnover. This drift accompanied the institutionalization of
professional Go (Oteai ranking, Nihon Ki-in founding).

The 2010s→2020s drift (0.013) occurred within a stable institutional
framework and at average historical magnitude. However, the AI era produced a
large increase in pattern circulation speed (Section 2.4) that the
institutional revolution did not. Two revolutions, two mechanisms: one
restructured who played and how; the other accelerated how fast innovations
spread.

### 2.7 Regional event-stream dynamics independently validate the three-phase model

We classified games into event streams by tournament-name keyword matching
into Japan-coded, Korea-coded, and China-coded subsets. Event-stream labels
reflect the tournament's organizational and archival provenance, not player
nationality. Inter-stream spatial-relation distance reveals a three-phase
response:

```
1990s (pre-AI):         0.0186  (three independent event streams)
2016-17 (AlphaGo shock):  0.0070  (convergence)
2018-21 (AI diffusion):   0.0121  (re-divergence — asymmetric absorption)
2022-25 (oracle era):     0.0065  (re-convergence)
```

The Korea-coded event-stream fighting index (adj_opp − adj_own) peaked during
AI diffusion (2018-21: +0.038), above its pre-AI level (2008-15: +0.027). AI
initially amplified event-stream-specific signatures before the oracle era
pulled them toward the global mean. This three-phase pattern—shock
convergence, divergent absorption, oracle re-stabilization—independently
replicates the Codex operation pattern observed in held-out prediction
analysis across 22 years (Human Codex Δ > Frequency, 22/22 years, p ≈ 0;
E1 peak → E2 dip → E3 recovery).

## 3. Discussion

Our findings resolve an apparent paradox. Qualitatively, players and
commentators uniformly report that AI has "changed everything." Quantitatively,
the move-level structural drift of the AI era lies within the historical
envelope. The resolution is that what changed was not move structure but Codex
circulation speed.

This distinction matters beyond Go. It suggests a general property of external
oracles in cultural evolution: they accelerate the
discovery-transmission-persistence cycle without necessarily rewriting
structural grammar. The grammar—the coupling between game-phase position and
spatial-choice—is constrained by the geometry of the board and the deep
structure of the game. An oracle can reduce search costs, enabling faster
pattern discovery and stronger reuse once a pattern is validated.

The three-phase regional dynamics further suggest that oracle adoption follows
a characteristic destabilization-recovery trajectory: initial convergence
under shock, followed by a period of asymmetric absorption where pre-existing
signatures are temporarily amplified, culminating in a new equilibrium at
permanently higher circulation speed.

Several limitations apply. First, the CWI archive is Japan-dominant; while
Japan-only replication validates the main signal, Korea-coded and China-coded
event streams remain underpowered. Second, our pattern metrics are conditional
on qualifying recurrent patterns and on the observed follow-up window;
post-2016 patterns have shorter available follow-up, and the reported adoption
lag reduction should be interpreted with this censoring caveat. Third, the
KataGo analysis is based on a small sample (200 positions) and serves as
supplementary confirmation, not a primary pillar. Fourth, event-stream labels
reflect tournament and archival provenance, not player nationality; a
player-level decomposition is left for future work.

## 4. Methods Summary

**Data.** CWI Professional Go Archive, 95,076 SGF records spanning 1600-2026
[ref]. Majority Japanese professional and institutional records; Korean and
Chinese games enter substantially from the 1990s onward. Data availability and
licensing: see SI.

**Encoding.** Each move is factorized into two separable coordinate sets.
Game-phase (chroma): move index, normalized move index, board occupancy,
occupancy bin, and five phase bins (opening/early-mid/mid/late-mid/endgame).
Spatial-relation (rhythm): distance to last move, distance to nearest stone
(any, own, opponent), own/opponent local density (r=3), adjacent own/opponent
counts, edge distance, corner distance, corner-openness indicator, and
own-opponent density difference. Each move produces a 9-dim chroma vector and
a 12-dim rhythm vector.

**Decade drift.** Games grouped by decade. Per-decade rhythm centroid (5 key
features) computed. Decade-to-decade drift is the Euclidean distance between
centroids. Pre-2016 envelope: mean and 95% range of all decade-pair drifts
where the later decade ends ≤ 2010.

**Pattern analysis.** Opening patterns defined as the first 10/15/20-move
prefix string. Qualifying threshold: ≥3 years and ≥5 total uses. Adoption lag:
years from first observed year to first year with ≥3 unique players, among
qualifying recurrent patterns. Reuse density: fraction of years between first
and last observed year with active usage.

**Regional event-stream classification.** Tournament name keyword matching.
Japan-coded: Meijin, Kisei, Honinbo, Oza, Tengen, Gosei, Judan, NHK, Oteai,
and related terms. Korea-coded: Samsung, LG, BC Card, GS Caltex, and related
terms. China-coded: Mlily, Bailing, Chinese City League, Mingren, Tianyuan,
and related terms. Default: Japan-coded (the archive is Japan-origin).

**Codex operation.** Human Codex: per-position next-move frequency from all
training years. Baselines: global move frequency, recency (last 3 years).
Held-out: train on years < t, evaluate on year t. Statistical validation: sign
test (22/22 years, p ≈ 0), bootstrap CI on era-level Δ values.

**KataGo analysis.** KataGo v1.16.4 OpenCL,
`kata1-b28c512nbt-s13255194368-d5935380940`. 50 positions per era, sampled at
ply 30. maxVisits=100, Japanese rules, komi 6.5. Policy top-1 compared to
human move via rhythm feature distance.

**Robustness.** Prefix length: adoption lag acceleration replicated at 10, 15,
and 20 moves. Japan-only: all drift and operation analyses replicated on the
Japan-only subset. Leave-one-out player control: Korea-coded event-stream
fighting index stable under removal of any individual top player (Δ < 0.001).

## 5. Data Availability

CWI Professional Go Archive: publicly available at
https://homepages.cwi.nl/~aeb/go/games/. Parsed data, analysis scripts, and
result tables available at [repository URL] under CC-BY 4.0.

## 6. References

[1] Silver D, et al. (2016) Mastering the game of Go with deep neural
networks and tree search. Nature 529:484-489.

[2] Silver D, et al. (2017) Mastering the game of Go without human
knowledge. Nature 550:354-359.

[3] Beheim BA (2025) Opening strategies in the game of Go from feudalism to
superhuman AI. Cambridge University Press.

[4] [PNAS Nexus 2025 paper on AI and Go knowledge/diversity — to be added]

[5] Wu DJ (2025) The dual edges of AI: advancing knowledge while reducing
diversity. PNAS Nexus.

[6] Fortuna MA, Zaman L, Ofria C, Wagner A (2017) The genotype-phenotype map
of an evolving digital organism. PLoS Comput Biol 13(2):e1005414.

[7] Misevic D, Ofria C, Lenski RE (2006) Sexual reproduction reshapes the
genetic architecture of digital organisms. Proc R Soc B 273:457-464.

## 7. Figures

| Fig | Content | Status |
|-----|---------|--------|
| 1 | Encoding schematic + archive composition timeline | ready |
| 2 | Decade drift envelope + AI-era position | ready |
| 3 | 1910s→1920s decomposition (overlap vs non-overlap) | ready |
| 4 | Pattern adoption lag and reuse density by era | ready |
| 5 | Regional event-stream three-phase distance | ready |
| S1 | KataGo feature-level alignment | ready |
| S2 | Prefix-length robustness (10/15/20) | ready |
| S3 | Player-level decomposition of Korea-coded stream | ready |

---

*This draft supersedes PAPER_DRAFT_PNAS.md. All factual claims have been
verified against the source scripts and data. Unit labels, sample sizes, and
confidence statements follow the audit recommendations. P0 issues resolved.*
