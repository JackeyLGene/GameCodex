# External Oracles Accelerate Cultural Codex Circulation Without Rewriting Structural Grammar

**Target:** PNAS
**Status:** v3 draft, 2026-06-15. v2 audit repairs applied. Submission hardening.
**Core claim:** AI did not rewrite the move structure of professional Go;
it rewrote the speed at which the Go Codex is discovered, transmitted, and
stabilized.

---

## Significance Statement

Using 95,000 recorded Go games spanning four centuries, we show how an
external AI system changed not what professional players could play, but how
quickly new opening patterns were discovered and stabilized in a centuries-old
cultural record. The results establish that external oracles accelerate
cultural transmission without necessarily rewriting structural grammar.

## Abstract

The advent of superhuman AI in Go has been widely described as a rupture in
traditional playing knowledge. Using a dataset of 95,000 recorded games from
the CWI archive (1600-2026), we factorize each move into separable game-phase
and spatial-relation coordinates, measuring decade-level structural drift
across four centuries. We find that the AI-era drift magnitude (0.013) lies
within the pre-2016 historical envelope (mean 0.015, empirical 95% range
[0.000, 0.034]). The largest drift in the record—1910s to 1920s (0.034)—was
an institutional revolution (Oteai professional ranking); the AI era is an
oracle-speed revolution. Among qualifying recurrent opening patterns, observed
adoption lag shortened from 6.3 years (pre-1980) to 1.5 years (post-2016),
subject to right-censoring in the post-2016 window. Observed reuse density
rose from 0.35 to 0.78. These structural findings are not artifacts of archive
composition: Japan-only replication preserves the full-signal drift magnitude
(0.0159 vs 0.0160). Regional event-stream dynamics reveal a three-phase
response—shock convergence, divergent absorption, partial oracle
re-stabilization—
consistent with the destabilization-and-recovery pattern observed in held-out
Codex operation analysis across 22 years (Human Codex > Frequency, 22/22
years, sign test p < 0.001). Our results establish that external oracles
reshape cultural evolution not by rewriting structural grammar but by
accelerating the discovery, transmission, and persistence of new patterns
within existing structural constraints.

## 1. Introduction

The 2016 victory of AlphaGo over Lee Sedol was widely interpreted as a
watershed moment for human culture [1,2]. Professional Go players rapidly
adopted AI-influenced strategies. But did AI rewrite the structural grammar of
move choice, or did it accelerate the speed at which new moves are discovered
and adopted?

Here, structural grammar refers to stable constraints linking game phase and
spatial move-choice features, operationalized by chroma-rhythm coupling and
rhythm-centroid drift. These two possibilities are confounded in qualitative
accounts. Disentangling them requires (a) a structural encoding that separates
game-phase from spatial-choice, (b) a century-scale baseline against which to
measure deviation, and (c) a method for tracking pattern adoption speed
independent of pattern content. We address all three.

### Case Study: Two AlphaGo Encounters as Microcosm

To motivate the framework, we analyze two landmark human-AI encounters at the
single-game level. Figure 0 shows per-move retrospective KataGo policy
alignment and winrate trajectories for Lee Sedol (Game 4, 2016) and Ke Jie
(Game 1, 2017 Future of Go Summit).

Lee Sedol's celebrated "divine move" (move 78) is widely credited with turning
the game. Before move 78, Lee's moves were rarely among KataGo's top
recommendations (mean policy rank = 20; 25% in top-1; estimated winrate 1.6%).
The divine move itself had zero-indexed policy rank 2—within KataGo's top-3
recommendations, but not the top recommendation. After move 78, Lee's choices
aligned sharply with KataGo policy (mean rank = 4; 39% in top-1; 83% in
top-3), and his winrate rose from 1.4% to 99.6%. His post-78 play also
systematically differed from his play in games he lost to AlphaGo (higher
adj_opp: d = +0.19; higher adj_own: d = +0.32). AlphaGo's subsequent moves
became more spatially displaced by our rhythm metric (dist_last: d = +0.55).
Lee appears to have entered an AI-aligned move-choice regime only after the
shock of a single catalytic move.

Ke Jie, playing AlphaGo Master one year later, began his game already in an
AI-aligned regime (mean zero-indexed rank = 1.4; 61% in top-1 and 83% in
top-3 across the plotted retrospective trace). His alignment did not shift—it
was high from the start. He nonetheless lost: the normalized human-perspective
winrate trace was near even early and then declined toward zero as AlphaGo
Master consolidated the game.

This paired contrast illustrates that retrospective AI alignment is not
equivalent to victory. Lee entered an AI-aligned regime through a phase
transition; Ke Jie was already there but faced a stronger opponent. Both cases
show, in microcosm, how external oracles restructure move-choice regimes
without guaranteeing outcomes. The claim of this paper is not about individual
moves or games—it is that this pattern characterizes the structural response
of professional Go to external AI oracles at scale.

## 2. Results

### 2.1 AI-era drift lies within the historical envelope

We computed decade-to-decade structural drift across four centuries using a
five-dimensional spatial-relation vector per move (adj_opp, adj_own,
dens_delta, dist_last, is_corner_open). The game-phase coordinate captures
move index, board occupancy, and phase bin; the spatial-relation coordinate
captures distances, adjacencies, densities, and corner proximity to existing
stones.

```
Pre-2016 decade drift:        mean = 0.0146, SD = 0.0098
                              empirical 95% range: [0.000, 0.034]
AI-era (2010s to 2020s):      |drift| = 0.0130
Z-score relative to pre-2016: -0.16
```

The AI-era drift lies well within the pre-2016 historical envelope. The
largest drift in our record—1910s to 1920s (|drift| = 0.034, 2.6× the AI-era
magnitude)—corresponds to the institutionalization of professional Go through
the Oteai ranking system and the founding of the Nihon Ki-in (1924). AI is not
the most structurally disruptive event in Go history.

None of the five rhythm dimensions individually exceeded the pre-2016
historical range in the AI era (all Z < 1.96; is_corner_open Z = +1.42,
marginally elevated).

### 2.2 Chroma-rhythm coupling remained stable in the observed period

Phase 1 analysis of chroma-rhythm cross-harm coupling across 44,368 post-2000
games showed no global shift across AI eras (Cohen's d(E0 vs E3) = -0.029).
The observed AI-era structural change is best characterized as an
operating-point shift: rhythm features moved (Section 2.1) within a stable
observed chroma-rhythm coupling structure.

### 2.3 Selective convergence toward AI policy (Supplementary)

We compared human move choices with KataGo policy recommendations across 200
sampled positions (50 per era, ply 30). The overall human-KataGo rhythm gap
did not change across eras (Cohen's d(E0 vs E3) = -0.008). Feature-level
analysis suggested selective convergence on opponent-proximal dimensions
(adj_opp, adj_own, dens_delta) but not on pacing or corner strategy. We treat
this result as consistent with the main findings but do not build the primary
argument on it, given the limited sample. KataGo analysis used
`kata1-b28c512nbt-s13255194368-d5935380940`, maxVisits=100, Japanese rules,
komi 6.5.

### 2.4 Pattern adoption accelerated; reuse density increased

We tracked 74,501 unique opening patterns (first 15 moves) across 546
patterns meeting the qualifying threshold of ≥3 years and ≥5 uses.

```
                          pre-1980  1980-1999  2000-2015  2016+
Observed adoption lag:      6.3 yr    5.7 yr     2.6 yr   1.5 yr
Observed reuse density:      0.35      0.37       0.67     0.78
Half-life:                   1.1 yr    1.1 yr     1.0 yr   1.1 yr
```

Adoption lag is measured as years from first observed appearance to first year
with ≥3 unique players, among qualifying recurrent patterns. These metrics are
conditional on the qualifying filter and on the observed follow-up window;
post-2016 patterns have shorter available follow-up (maximum 9 years compared
to 50+ years for pre-1980 patterns), and the observed lag reduction should be
interpreted subject to this right-censoring caveat. Reuse density is the
fraction of years between first and last observed appearance in which the
pattern was actively used. Pattern half-life remained approximately 1.1 years
across all eras.

A fixed-horizon check gave the same direction while reducing right-censoring
dependence: 2016+ qualifying patterns reached the ≥3-player threshold within
1, 2, 3, and 5 years at rates of 0.57, 0.73, 0.80, and 0.91, compared with
0.31, 0.37, 0.39, and 0.44 for pre-1980 patterns. Per-pattern bootstrap
resampling gave an observed adoption-lag ratio of 4.2× (95% CI: 2.9×-5.9×)
and a reuse-density ratio of 2.3× (95% CI: 2.1×-2.5×).

Long-term adoption acceleration is robust to prefix length:
prefix 10 shows 9.0→1.3 yr, prefix 15 shows 6.3→1.5 yr, prefix 20 shows
4.1→1.4 yr. The additional post-2016 reduction is strongest for prefix
lengths 10 and 15, but not detectable at prefix length 20, where 2000-2015 and
2016+ both show 1.4-year observed lag.

### 2.5 The archive is not a transparent window

The CWI archive is itself a product of Codex circulation. True game counts
show the archive composition changed substantially:

| Decade | JPN | KOR | CHN | INTL/Unk | Total |
|--------|-----|-----|-----|----------|-------|
| 1950s | 1,668 | 0 | 0 | 200 | 1,868 |
| 1980s | 9,640 | 1 | 0 | 106 | 9,747 |
| 2000s | 9,198 | 1,078 | 4 | 831 | 11,111 |
| 2020s | 12,175 | 1,642 | 207 | 523 | 14,547 |

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
restructured who played and how (institutional reorganization); the other
accelerated how fast innovations spread (oracle-speed circulation).

### 2.7 Regional event-stream dynamics are consistent with the three-phase Codex model

We classified games into event streams by tournament-name keyword matching
into Japan-coded, Korea-coded, and China-coded subsets. Event-stream labels
reflect the tournament's organizational and archival provenance, not player
nationality. Inter-stream spatial-relation distance reveals a three-phase
response:

```
1990-2015 (pre-AI):          0.0144  (independent event streams)
2016-17 (AlphaGo shock):     0.0066  (convergence)
2018-21 (AI diffusion):      0.0167  (re-divergence)
2022-25 (oracle era):        0.0102  (partial re-convergence)
```

The Korea-coded event-stream fighting index (adj_opp − adj_own) peaked during
AI diffusion (2018-21: +0.038), above its pre-AI level (2008-15: +0.027). AI
initially amplified event-stream-specific signatures before the oracle era
partially pulled them back toward the full-archive centroid. Bootstrap
intervals for the exact five-feature distance were [0.0109, 0.0361] pre-AI,
[0.0037, 0.0151] during shock, [0.0109, 0.0323] during diffusion, and
[0.0056, 0.0212] in the oracle era. This three-phase pattern is
consistent with the Codex operation trajectory observed in held-out prediction
analysis across 22 years (Human Codex Δ > Frequency, 22/22 years, sign test
p < 0.001; E1 peak → E2 dip → E3 recovery).

## 3. Discussion

Our findings resolve an apparent paradox. Qualitatively, players and
commentators uniformly report that AI has "changed everything." Quantitatively,
the move-level structural drift of the AI era lies within the historical
envelope. The resolution is that what changed was not move structure but Codex
circulation speed.

This distinction matters beyond Go. It suggests a general property of external
oracles in cultural evolution: they accelerate the discovery-transmission-
persistence cycle without necessarily rewriting structural grammar. The
grammar—the coupling between game-phase position and spatial-choice—is
constrained by the geometry of the board and the deep structure of the game.
An oracle can reduce search costs, enabling faster pattern discovery and
stronger reuse once a pattern is validated.

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
lag reduction should be interpreted subject to right-censoring. Third, the
KataGo analysis is based on a small sample (200 positions) and serves as
supplementary confirmation. Fourth, event-stream labels reflect tournament and
archival provenance, not player nationality.

## 4. Methods Summary

**Data.** CWI Professional Go Archive, 95,076 SGF records mostly spanning
1600-2026, with sparse earlier records excluded from the main century-scale
analysis [CWI ref]. Majority Japanese professional and institutional records;
Korean and Chinese games enter substantially from the 1990s onward.

**Encoding.** Each move is factorized into two separable coordinate sets.
Game-phase: move index, normalized move index, board occupancy, occupancy bin,
and five phase bins (opening through endgame). Spatial-relation: distance to
last move, distance to nearest stone (any, own, opponent), own/opponent local
density (r=3), adjacent own/opponent counts, edge distance, corner distance,
corner-openness indicator, and own-opponent density difference.

**Decade drift.** Games grouped by decade. Per-decade rhythm centroid (5 key
features) computed. Decade-to-decade drift is the Euclidean distance between
centroids. Pre-2016 envelope: mean and empirical range of all decade-pair
drifts where the later decade ends ≤ 2010.

**Pattern analysis.** Opening patterns defined as first 15-move prefix string.
Qualifying threshold: ≥3 years and ≥5 total uses. Adoption lag: years from
first observed year to first year with ≥3 unique players, among qualifying
recurrent patterns. Fixed-horizon adoption checks measure whether this threshold
is reached within 1, 2, 3, and 5 years after first observed appearance. Reuse
density: fraction of years between first and last observed year with active
usage. Bootstrap intervals use per-pattern resampling within eras.

**Regional event-stream classification.** Tournament name keyword matching.
Japan-coded: Meijin, Kisei, Honinbo, Oza, Tengen, Gosei, Judan, NHK, Oteai,
and related terms. Korea-coded: Samsung, LG, BC Card, GS Caltex, and related
terms. China-coded: Mlily, Bailing, Chinese City League, Mingren, Tianyuan,
and related terms. Default: Japan-coded (the archive is Japan-origin).

**Codex operation.** Human Codex: per-position next-move frequency from all
training years. Baselines: global move frequency, recency (last 3 years).
Held-out: train on years < t, evaluate on year t. Statistical validation: sign
test (22/22 years, p < 0.001), bootstrap CI on era-level Δ values.

**KataGo analysis.** KataGo v1.16.4 OpenCL,
`kata1-b28c512nbt-s13255194368-d5935380940`. 50 positions per era, sampled at
ply 30. maxVisits=100, Japanese rules, komi 6.5. Policy top-1 compared to
human move via rhythm feature distance (Supplementary).

**Robustness.** Prefix length: adoption lag acceleration replicated at 10, 15,
and 20 moves; post-2016 additional reduction strongest at prefixes 10 and 15.
Japan-only: all drift and operation analyses replicated on the Japan-only
subset. Event-stream top-player leave-one-out control: fighting index stable
under removal of any individual top player (Δ < 0.001).

## 5. Data Availability

Analysis scripts and derived aggregate result tables will be released at a
public repository upon publication. Source SGF records are available from the
CWI Professional Go Archive (https://homepages.cwi.nl/~aeb/go/games/) subject
to the archive's terms. Parsed intermediate data files supporting the main
figures are available from the authors upon request.

## 6. References

[1] Silver D, et al. (2016) Mastering the game of Go with deep neural
networks and tree search. Nature 529:484-489.
doi:10.1038/nature16961

[2] Silver D, et al. (2017) Mastering the game of Go without human
knowledge. Nature 550:354-359. doi:10.1038/nature24270

[3] Beheim BA (2025) Opening strategies in the game of Go from feudalism to
superhuman AI. Evolutionary Human Sciences 7:e28.
doi:10.1017/ehs.2025.10016

[4] Choi S, Kang M, Kim J, Kim J (2025) The dual edges of AI: advancing
knowledge while reducing diversity. PNAS Nexus 4(5):pgaf138.
doi:10.1093/pnasnexus/pgaf138

[5] Fortuna MA, Zaman L, Ofria C, Wagner A (2017) The genotype-phenotype map
of an evolving digital organism. PLoS Comput Biol 13(2):e1005414.
doi:10.1371/journal.pcbi.1005414

[6] Misevic D, Ofria C, Lenski RE (2006) Sexual reproduction reshapes the
genetic architecture of digital organisms. Proc R Soc B 273:457-464.
doi:10.1098/rspb.2005.3338

[7] CWI Professional Go Archive. https://homepages.cwi.nl/~aeb/go/games/

## 7. Figures

| Fig | Content | Status |
|-----|---------|--------|
| 0 | Paired AlphaGo encounters: Lee Sedol and Ke Jie retrospective alignment | generated |
| 1 | Encoding schematic + archive composition timeline | data ready |
| 2 | Decade drift envelope with AI-era position marked | data ready |
| 3 | 1910s→1920s overlap-player decomposition | data ready |
| 4 | Pattern adoption lag and reuse density by era | data ready |
| 5 | Regional event-stream three-phase distance | data ready |
| S1 | KataGo feature-level selective convergence | data ready |
| S2 | Prefix-length robustness (10, 15, 20 moves) | data ready |
| S3 | Event-stream top-player leave-one-out control | data ready |

---

*v3 incorporates the v2 audit's major repairs and the Phase 5 hardening checks.
Remaining task: verify final repository/data availability language before
external submission.*
