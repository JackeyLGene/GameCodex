# External Oracles Accelerate Cultural Codex Circulation Without Rewriting Structural Grammar

**Target:** PNAS  
**Status:** v4 — Internal review ready. 2026-06-15.  
**Figures:** Fig 0 (paired vignette), Fig 1–5 (main), Figs S1–S3 (supplementary).  

---

## Significance Statement

Using 95,000 recorded Go games spanning four centuries, we show how an
external AI system changed not what professional players could play, but how
quickly new opening patterns were discovered and stabilized in a centuries-old
cultural record. The results establish that external oracles accelerate
cultural transmission without necessarily rewriting structural grammar.

## Abstract

The advent of superhuman AI in Go has been widely described as a rupture in
traditional playing knowledge. Using 95,000 recorded games from the CWI
archive (1600–2026), we factorize each move into separable game-phase and
spatial-relation coordinates, measuring decade-level structural drift across
four centuries. The AI-era drift magnitude (0.013) lies within the pre-2016
historical envelope (mean 0.015; empirical 95% range [0.000, 0.034]). The
largest drift—1910s to 1920s (0.034)—was an institutional revolution
(Oteai professional ranking); the AI era is an oracle-speed revolution.
Among qualifying recurrent opening patterns, observed adoption lag shortened
from 6.3 years (pre-1980) to 1.5 years (post-2016), subject to right-censoring
in the post-2016 window. Observed reuse density rose from 0.35 to 0.78. These
findings are not artifacts of archive composition: Japan-only replication
preserves the full-signal drift magnitude (0.0159 vs 0.0160). Regional
event-stream dynamics reveal a three-phase response—shock convergence,
divergent absorption, partial oracle re-stabilization—consistent with the
held-out Codex operation trajectory (Human Codex exceeds Frequency baseline in
22 of 22 years; sign test *p* < 0.001). Our results establish that external
oracles reshape cultural evolution not by rewriting structural grammar but by
accelerating the discovery, transmission, and persistence of new patterns
within existing structural constraints.

---

## 1. Introduction

In March 2016, AlphaGo defeated Lee Sedol 4–1 in a five-game match watched by
over 200 million people [1,2]. Professional Go players rapidly adopted
AI-influenced strategies, leading to widespread claims that AI had "rewritten
Go." But what exactly changed: the structural grammar of move choice, or the
speed at which new moves are discovered and adopted?

Here, *structural grammar* refers to stable constraints linking game phase and
spatial move-choice features, operationalized by chroma-rhythm coupling and
rhythm-centroid drift across eras. These two possibilities—structural
rewriting versus circulation acceleration—are confounded in qualitative
accounts. Disentangling them requires (a) a structural encoding that separates
game-phase from spatial-choice, (b) a century-scale baseline against which to
measure deviation, and (c) a method for tracking pattern adoption speed
independent of pattern content. We address all three.

### 1.1 Case Study: Two AlphaGo Encounters as Microcosm

To motivate the framework, we analyze two landmark human-AI encounters at the
single-game level. Fig. 0 shows per-move retrospective KataGo policy alignment
and winrate trajectories.

**Lee Sedol (Game 4, 2016).** Before his celebrated move 78, Lee's moves were
rarely among KataGo's top recommendations (mean zero-indexed policy rank = 20;
25% in top-1; estimated winrate 1.6%). The move itself ranked second—within
KataGo's top-3 but not its top-1. After move 78, Lee's choices aligned sharply
with KataGo (mean rank = 4; 39% top-1; 83% top-3), and his winrate rose from
1.4% to 99.6%. His post-78 play systematically differed from his play in games
he lost to AlphaGo (adj_opp Cohen's d = +0.19; adj_own d = +0.32), and
AlphaGo's subsequent moves became more spatially displaced (dist_last
d = +0.55). Lee appears to have entered an AI-aligned regime through a phase
transition.

**Ke Jie (Game 1, 2017 Future of Go Summit).** One year later, Ke Jie began
his game already in an AI-aligned regime (mean zero-indexed rank = 1.4; 61%
top-1; 83% top-3). His alignment did not shift—it was high from the start. He
nonetheless lost, with his estimated winrate declining steadily from near-even
toward zero.

This paired contrast illustrates that retrospective AI alignment is not
equivalent to victory. Lee entered an AI-aligned regime through a phase
transition; Ke Jie was already there but faced a stronger opponent. Both cases
show, in microcosm, how external oracles restructure move-choice regimes
without guaranteeing outcomes. The claim of this paper is not about individual
moves or games—it is that this pattern characterizes the structural response
of professional Go to external AI oracles at scale.

---

## 2. Results

### 2.1 AI-era drift lies within the historical envelope

We computed decade-to-decade structural drift across four centuries using a
five-dimensional spatial-relation vector per move (adj_opp, adj_own,
dens_delta, dist_last, is_corner_open). The game-phase coordinate captures
move index, board occupancy, and phase bin; the spatial-relation coordinate
captures distances, adjacencies, densities, and corner proximity to existing
stones. Full encoding details are provided in Methods.

The pre-2016 decade-to-decade drift distribution has mean 0.0146, standard
deviation 0.0098, and empirical 95% range [0.000, 0.034]. The AI-era
transition (2010s to 2020s) has |drift| = 0.0130, with Z-score −0.16 relative
to the pre-2016 distribution. The AI-era drift lies within the historical
envelope (Fig. 1).

The largest drift in our record—1910s to 1920s (|drift| = 0.034, 2.6× the
AI-era magnitude)—corresponds to the institutionalization of professional Go
through the Oteai ranking system and the founding of the Nihon Ki-in (1924).
AI is not the most structurally disruptive event in Go history.

None of the five rhythm dimensions individually exceeded the pre-2016
historical range in the AI era (all Z < 1.96; is_corner_open showed the
largest displacement at Z = +1.42).

### 2.2 Chroma-rhythm coupling remained stable

Cross-harm coupling between game-phase and spatial-relation coordinates was
measured across 44,368 post-2000 games. No global shift was detected across AI
eras (Cohen's d, E0 vs E3 = −0.029). The observed AI-era change is best
characterized as an operating-point shift: rhythm features moved (Section 2.1)
within a stable chroma-rhythm coupling structure.

### 2.3 Selective convergence toward AI policy (Supplementary)

We compared human move choices with KataGo policy recommendations across 200
sampled positions (50 per era, ply 30). The overall human-KataGo rhythm gap
did not change across eras (Cohen's d, E0 vs E3 = −0.008). Feature-level
analysis suggested selective convergence on opponent-proximal dimensions
(adj_opp, adj_own, dens_delta) but not on pacing or corner strategy. We treat
this result as supplementary: it is consistent with the main findings but is
based on a limited sample. KataGo analysis used
*kata1-b28c512nbt-s13255194368-d5935380940*, maxVisits = 100, Japanese rules,
komi 6.5. Full details in SI.

### 2.4 Pattern adoption accelerated; reuse density increased

We tracked 74,501 unique opening patterns (first 15 moves), of which 546 met
the qualifying threshold of ≥3 years with ≥5 total uses. Per-era metrics are
reported in Table 1.

**Table 1. Pattern adoption and reuse by era of first appearance.**

| Era | N patterns | Observed adoption lag (yr) | Observed reuse density | Half-life (yr) |
|-----|-----------|---------------------------|----------------------|---------------|
| pre-1980 | 190 | 6.3 | 0.35 | 1.1 |
| 1980–1999 | 154 | 5.7 | 0.37 | 1.1 |
| 2000–2015 | 87 | 2.6 | 0.67 | 1.0 |
| 2016+ | 115 | 1.5 | 0.78 | 1.1 |

Adoption lag is measured as years from first observed appearance to first year
with ≥3 unique players, among qualifying recurrent patterns. These metrics are
conditional on the qualifying filter and on the observed follow-up window;
post-2016 patterns have shorter available follow-up (maximum 9 years vs 50+
years for pre-1980 patterns). Fixed-horizon adoption analysis confirms the
acceleration is not solely a right-censoring artifact: the probability of
reaching ≥3 unique players within 5 years rose from 0.44 (pre-1980) to 0.91
(2016+) (Fig. 2). Bootstrap resampling of the adoption lag ratio yields
4.2× (95% CI [2.9×, 5.9×]). Reuse density—the fraction of years between
first and last observed appearance with active usage—increased 2.3× (95% CI
[2.1×, 2.5×]). Pattern half-life remained approximately 1.1 years across all
eras.

Long-term adoption acceleration is robust to prefix length: prefix 10 shows
9.0→1.3 yr, prefix 15 shows 6.3→1.5 yr, prefix 20 shows 4.1→1.4 yr. The
additional post-2016 reduction is strongest for prefix lengths 10 and 15, but
not detectable at prefix length 20, where both 2000–2015 and 2016+ show
1.4-year observed lag (Fig. S2).

### 2.5 The archive is not a transparent window

The CWI archive is itself a product of Codex circulation. Table 2 reports true
game counts by decade and event stream.

**Table 2. CWI archive composition by decade.**

| Decade | JPN-coded | KOR-coded | CHN-coded | INTL/Other | Total |
|--------|----------|----------|----------|-----------|-------|
| 1950s | 1,668 | 0 | 0 | 200 | 1,868 |
| 1980s | 9,640 | 1 | 0 | 106 | 9,747 |
| 2000s | 9,198 | 1,078 | 4 | 831 | 11,111 |
| 2020s | 12,175 | 1,642 | 207 | 523 | 14,547 |

To verify that our structural findings are not artifacts of this composition
shift, we replicated the decade drift analysis on a Japan-only subset—the only
continuous archival record across all decades. The Japan-only drift magnitude
(0.0159) was nearly identical to the full-archive value (0.0160). The signal
is in the moves, not in the archive composition.

### 2.6 Two revolutions, two mechanisms

The 1910s→1920s structural drift (0.034) was decomposed by splitting games
into overlap players (20 players appearing in both decades) and non-overlap
players. Overlap players accounted for 85% of the total drift magnitude
(0.0291 of 0.0342), indicating a true playing-style shift rather than roster
turnover. This drift accompanied the institutionalization of professional Go
(Oteai ranking, Nihon Ki-in founding). The 2010s→2020s drift (0.013) occurred
within a stable institutional framework and at average historical magnitude,
yet the AI era produced a large increase in pattern circulation speed (Section
2.4) that the institutional revolution did not. The two revolutions operated
through different mechanisms: institutional reorganization versus oracle-speed
circulation (Fig. 3).

### 2.7 Regional event-stream dynamics echo the Codex destabilization-recovery pattern

Games were classified into event streams by tournament-name keyword matching
into Japan-coded, Korea-coded, and China-coded subsets. Event-stream labels
reflect tournament provenance and archival pathway, not player nationality.
Inter-stream five-feature spatial-relation distance reveals a three-phase
response (Fig. 4):

- Pre-AI (1990–2015): 0.0144 [95% CI 0.0109, 0.0361]
- AlphaGo shock (2016–2017): 0.0066 [95% CI 0.0037, 0.0151]
- AI diffusion (2018–2021): 0.0167 [95% CI 0.0109, 0.0323]
- Oracle era (2022–2025): 0.0102 [95% CI 0.0056, 0.0212]

The Korea-coded event-stream fighting index (adj_opp − adj_own) peaked during
AI diffusion (2018–2021: +0.038), above its pre-AI level (2008–2015: +0.027).
AI initially amplified stream-specific signatures before the oracle era pulled
them toward the full-archive centroid. This three-phase pattern is consistent
with the Codex operation trajectory observed in held-out prediction: Human
Codex exceeds the Frequency baseline in all 22 held-out years (sign test
*p* < 0.001), with era-level mean Δ values showing a peak at E1, a dip at E2,
and recovery at E3 (bootstrap 95% CIs all above zero; see SI). Leave-one-out
control confirms the Korea-coded stream fighting index is not driven by any
single top player (Δ < 0.001 per player).

---

## 3. Discussion

Our findings resolve an apparent paradox. Qualitatively, players and
commentators report that AI "changed everything." Quantitatively, the
move-level structural drift of the AI era lies within the historical envelope.
The resolution is that what changed was not move structure but Codex
circulation speed.

This distinction matters beyond Go. It suggests a general property of external
oracles in cultural evolution: they accelerate the discovery–transmission–
persistence cycle without necessarily rewriting structural grammar. The
grammar—the coupling between game-phase position and spatial-choice—is
constrained by the geometry of the board and the deep structure of the game.
An oracle can reduce search costs, enabling faster pattern discovery and
stronger reuse once a pattern is validated.

The three-phase regional dynamics further suggest that oracle adoption follows
a characteristic destabilization-recovery trajectory: initial convergence
under shock, followed by asymmetric absorption where pre-existing signatures
are temporarily amplified, culminating in partial re-stabilization at
permanently higher circulation speed.

Several limitations apply. First, the CWI archive is Japan-dominant; while
Japan-only replication validates the main drift signal, Korea-coded and
China-coded event streams remain underpowered relative to the Japan-coded
stream. Second, our pattern metrics are conditional on qualifying recurrent
patterns and on the observed follow-up window, though fixed-horizon analysis
confirms the acceleration is not solely a censoring artifact. Third, the
KataGo analysis is based on a small sample (200 positions) and serves as
supplementary confirmation. Fourth, event-stream labels reflect tournament
and archival provenance, not player nationality; the "fighting index" refers
to the Korea-coded event stream and should not be interpreted as a national
style claim without player-level nationality data.

---

## 4. Methods

### 4.1 Data

CWI Professional Go Archive: 95,076 SGF records spanning 1600–2026, with five
sparse pre-1600 records excluded from the main century-scale analysis [7].
The archive is predominantly Japanese professional and institutional records;
Korean and Chinese games enter substantially from the 1990s onward.

### 4.2 Move encoding

Each move is factorized into two separable coordinate sets. **Game-phase**
(chroma): move index, normalized move index (by fixed horizon 300), board
occupancy fraction, occupancy bin, and five phase bins (opening, early-mid,
mid, late-mid, endgame). **Spatial-relation** (rhythm): distance to last move,
distance to nearest stone (any, own, opponent), own/opponent local stone
density within radius 3, adjacent own/opponent stone count, edge distance,
corner distance, corner-openness indicator, and own-minus-opponent density
difference. Key paper analyses use five rhythm features (adj_opp, adj_own,
dens_delta, dist_last, is_corner_open); the full 9 + 12 vectors are used for
cross-harm coupling.

### 4.3 Decade drift

Games are grouped by decade. Per-decade rhythm centroids are computed for the
five key features. Decade-to-decade drift is the Euclidean distance between
consecutive centroids. The pre-2016 envelope is defined by all decade-pair
drifts where the later decade ends ≤ 2010 (N = 15 decade transitions).

### 4.4 Pattern analysis

Opening patterns are defined as the first 15-move prefix string. Qualifying
threshold: ≥3 years and ≥5 total uses across all years. Adoption lag: years
from first observed year to first year with ≥3 unique players. Reuse density:
fraction of years between first and last observed year in which the pattern
was actively used. Fixed-horizon adoption: probability of reaching ≥3 unique
players within a fixed follow-up window (1, 2, 3, or 5 years). Bootstrap CIs
use 5,000 per-pattern resamples within each era.

### 4.5 Event-stream classification

Tournament-name keyword matching. Japan-coded: Meijin, Kisei, Honinbo, Oza,
Tengen, Gosei, Judan, NHK, Oteai, and related terms. Korea-coded: Samsung,
LG, BC Card, GS Caltex, and related terms. China-coded: Mlily, Bailing,
Chinese City League, Mingren, Tianyuan, and related terms. Default
classification is Japan-coded (the archive is Japan-origin). The classifier
was audited by manual inspection of the top 50 events per category.

### 4.6 Codex operation

Human Codex: per-position next-move frequency from all training years.
Baselines: global move frequency (Frequency), last-three-years per-position
frequency (Recency). Held-out protocol: train on years < *t*, evaluate on year
*t*, repeated for each test year 2005–2026. Statistical validation: sign test
for Human Codex exceeding Frequency (22/22 years); bootstrap CI (5,000
resamples) on era-level Δ values.

### 4.7 KataGo analysis

KataGo v1.16.4 OpenCL backend, network *kata1-b28c512nbt-s13255194368-
d5935380940*. For the cross-era comparison: 50 positions per era, sampled at
ply 30, maxVisits = 100, Japanese rules, komi 6.5. For the paired vignette
(Fig. 0): every second move of the human player, maxVisits = 100, same rules
and komi. Policy top-1 compared to the actual move via rhythm feature
distance. All KataGo results are treated as retrospective policy proxies and
reported as supplementary or case-study material.

### 4.8 Robustness checks

Prefix length: adoption lag acceleration replicated at prefix lengths 10, 15,
and 20 (Fig. S2). Japan-only: all drift and operation analyses replicated on
the Japan-only subset. Event-stream top-player leave-one-out: fighting index
stable under removal of any individual top player. Bootstrap CIs: reported for
all key ratios using 5,000 per-sample resamples.

---

## 5. Data Availability

Analysis scripts and derived aggregate result tables are available at a public
repository to be deposited upon acceptance. Source SGF records are available
from the CWI Professional Go Archive (https://homepages.cwi.nl/~aeb/go/games/)
subject to the archive's terms. Parsed intermediate data and per-game feature
files supporting the main figures are available from the authors upon request.

---

## 6. References

1. Silver D, Huang A, Maddison CJ, et al. (2016) Mastering the game of Go
with deep neural networks and tree search. *Nature* 529:484–489.
doi:10.1038/nature16961

2. Silver D, Schrittwieser J, Simonyan K, et al. (2017) Mastering the game
of Go without human knowledge. *Nature* 550:354–359. doi:10.1038/nature24270

3. Beheim BA (2025) Opening strategies in the game of Go from feudalism to
superhuman AI. *Evolutionary Human Sciences* 7:e35.
doi:10.1017/ehs.2025.35

4. Choi S, Kang H, Kim J, Park J (2025) The dual edges of AI: advancing
knowledge while reducing diversity in Go. *PNAS Nexus* 4:pgaf138.
doi:10.1093/pnasnexus/pgaf138

5. Fortuna MA, Zaman L, Ofria C, Wagner A (2017) The genotype-phenotype map
of an evolving digital organism. *PLoS Computational Biology* 13(2):e1005414.
doi:10.1371/journal.pcbi.1005414

6. Misevic D, Ofria C, Lenski RE (2006) Sexual reproduction reshapes the
genetic architecture of digital organisms. *Proceedings of the Royal Society B*
273:457–464. doi:10.1098/rspb.2005.3338

7. Brouwer AE. CWI Professional Go Archive.
https://homepages.cwi.nl/~aeb/go/games/ (accessed 2026-06-14).

---

## Figures

**Fig. 0** — Two AlphaGo Encounters as Microcosm. Paired per-move KataGo
policy rank and winrate trajectories for Lee Sedol (Game 4, 2016) and Ke Jie
(Game 1, 2017).  
*Source trace:* `results/figures/fig0_paired_vignette_trace.csv`

**Fig. 1** — Century-scale structural drift envelope. (A) Decade-to-decade
drift timeline with AI-era marked. (B) AI-era drift position relative to the
pre-2016 drift distribution.  

**Fig. 2** — Fixed-horizon adoption probability by era of first appearance.
Probability of reaching ≥3 unique players within 1, 2, 3, and 5 years.  

**Fig. 3** — Institutional revolution vs. oracle-speed revolution. 1910s→1920s
overlap-player decomposition.  

**Fig. 4** — Regional event-stream three-phase distance. Five-feature
Euclidean distance with bootstrap 95% CIs.  

**Fig. 5** — Pattern adoption lag and reuse density by era.  

**Fig. S1** — KataGo feature-level selective convergence.  

**Fig. S2** — Prefix-length robustness: adoption lag at prefix lengths 10, 15,
and 20.  

**Fig. S3** — Event-stream top-player leave-one-out control.  

---

*Internal review version. v4. 2026-06-15.*
