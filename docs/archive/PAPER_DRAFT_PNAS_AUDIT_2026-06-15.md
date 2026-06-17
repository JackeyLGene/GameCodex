# PAPER_DRAFT_PNAS Audit Report

**Date:** 2026-06-15  
**Target draft:** `docs/PAPER_DRAFT_PNAS.md`  
**Audit status:** detailed internal review. Not submission-ready yet.  
**Overall verdict:** strong PNAS-level narrative, but several factual/methodological inconsistencies must be fixed before external review.

---

## 1. Executive Verdict

The paper has a real, coherent core:

> AI did not rewrite the move structure of professional Go; it rewrote the speed at which the Go Codex is discovered, transmitted, and locked in.

The strongest evidence chain is:

1. AI-era drift is inside the historical envelope.
2. CWI is an archive/circulation fossil, not a transparent global record.
3. Japan-only controls preserve the full-CWI drift signal.
4. 1910s->1920s was an institutional revolution; 2010s->2020s is an oracle-speed revolution.
5. Pattern adoption accelerates, and reuse/lock-in increases.
6. Regional rhythm dynamics independently echo the E1/E2/E3 Codex pattern.

However, the current draft overstates several claims and mixes units, labels, and evidence layers. The paper should enter Phase 5, but Phase 5 should be a **defense-and-rewrite phase**, not submission.

Recommended decision:

> Begin paper convergence now, but do not submit until P0/P1 issues below are resolved.

---

## 2. Scope Of Audit

Reviewed:

- `docs/PAPER_DRAFT_PNAS.md`
- `results/PHASE05_PHASE4_CONVERGENCE_2026-06-14.md`
- `results/PHASE4E_REGIONAL_RHYTHM_ORACLE_CONVERGENCE_2026-06-14.md`
- `results/PHASE2_KATAGO_ALIGNMENT_2026-06-14.md`
- `results/PHASE3_CODEX_OPERATION_2026-06-14.md`
- `scripts/phase2_full.py`
- `scripts/phase4a_archive_composition.py`
- `scripts/phase4d_pattern_adoption.py`
- `scripts/phase4e_regional_history.py`
- `scripts/phase5_defense.py`
- `data/katago/MODEL_SOURCE.md`

Also ran:

```powershell
python G:\GEME\EE\game_codex\scripts\phase5_defense.py
```

The defense script completed and exposed several important issues listed below.

---

## 3. P0 Blockers

### P0.1 Internal contradiction: AI-era drift is both 0.013 and "~0.03"

**Draft locations:** `PAPER_DRAFT_PNAS.md:30-31`, `PAPER_DRAFT_PNAS.md:83-86`, `PAPER_DRAFT_PNAS.md:150-153`

The draft correctly states:

```text
AI-era drift = 0.013
1910s->1920s drift = 0.034
```

But later it says:

```text
Both produced ~0.03 drift magnitude
```

This directly contradicts the paper's central claim that AI-era structural drift is inside the historical envelope and much smaller than the 1910s->1920s maximum.

**Risk:** An editor or reviewer will read this as either numerical sloppiness or an unstable main claim.

**Required fix:** Replace the `~0.03` sentence with:

> The 1910s->1920s institutional revolution produced the largest observed move-structure drift, whereas the 2010s->2020s oracle era produced average-level structural drift but a large increase in pattern circulation speed.

---

### P0.2 Archive composition table is mislabeled as games, but values are not game counts

**Draft locations:** `PAPER_DRAFT_PNAS.md:126-142`

The draft says Korean and Chinese games were absent/entered the archive and shows values such as:

```text
1950s JPN = 58,371
2020s JPN = 426,114
```

But the Phase 4A archive composition matrix gives actual decade-level game counts:

```text
1950s total games = 1,868
2020s total games = 14,547
```

The large values in the draft appear to be **move/rhythm observations**, not games. This creates a unit mismatch.

**Risk:** A reviewer will immediately notice that the table values exceed the stated 95,000-game dataset.

**Required fix:** Either:

1. Replace the table with true game counts from `archive_composition_by_decade.csv`, or
2. Keep the large values but label them explicitly as `rhythm move-observations`, not games.

The safer paper version is to use true game counts in the main text and move-observation counts in Methods/SI.

---

### P0.3 "Korea/China/Japan style" is currently event-stream classification, not player nationality

**Draft locations:** `PAPER_DRAFT_PNAS.md:155-173`, `PAPER_DRAFT_PNAS.md:199-205`

The regional classifier is event-name keyword based and defaults unknown events to JPN in several scripts. When `phase5_defense.py` was run, the "Top 10 Korean players" list included:

```text
Ke Jie
Yang Dingxin
Nakamura Sumire
Cho Chikun
```

This shows that the current "KOR" stream means **Korea-classified event/archive stream**, not Korean-nationality players.

**Risk:** The regional result can be attacked as mislabeling event location/sponsor/source as national style.

**Required fix:** In the main paper, relabel:

```text
Korea's fighting index
```

as:

```text
the Korea-coded event stream fighting index
```

unless player nationality metadata is added. The claim "Korean fighting style" should be downgraded to "Korea-coded professional stream" until player-level decomposition is complete.

---

### P0.4 Pattern adoption acceleration is not yet right-censoring safe

**Draft locations:** `PAPER_DRAFT_PNAS.md:107-124`, `PAPER_DRAFT_PNAS.md:217-219`

Pattern adoption lag is computed only for patterns that meet the qualifying filter and are observed to reach adoption. Post-2016 patterns have much shorter follow-up time than pre-1980 patterns.

Current metric:

```text
adoption_lag = first_seen -> first year with >=3 unique players
```

Potential issue:

- Long-lag post-2016 patterns may be right-censored and excluded.
- The filter `>=3 years and >=5 uses` conditions on survival.
- Reuse rate is measured between first and last appearance, not from first appearance to a fixed follow-up horizon.

**Risk:** A reviewer can argue that the 4.2x speedup is partly a censoring/selection artifact.

**Required fix:** Add survival-style or horizon-controlled analysis:

1. Fixed follow-up windows, e.g. adoption within 1, 2, 3, 5 years.
2. Kaplan-Meier / Cox model, treating not-yet-adopted patterns as censored.
3. Reuse rate over a fixed window after first appearance, not only between first and last observed year.

Until then, phrase as:

> observed adoption lag among qualifying recurrent patterns

not as unconditional adoption speed of all new patterns.

---

## 4. P1 Major Issues

### P1.1 KataGo methods are inconsistent with the actual model and script

**Draft locations:** `PAPER_DRAFT_PNAS.md:96-105`, `PAPER_DRAFT_PNAS.md:222`

The draft says:

```text
OpenCL v1.16.4, b20c256x2 network, 200 visits/position
```

But `MODEL_SOURCE.md` records:

```text
kata1-b28c512nbt-s13255194368-d5935380940
```

And `scripts/phase2_full.py` uses:

```text
MAX = 50 per era
maxVisits = 100
rules = japanese
komi = 6.5
```

The earlier smoke test used `maxVisits=20`.

**Risk:** Reproducibility failure.

**Required fix:** Replace the Methods line with the exact actual model, rules, komi, sample design, and maxVisits used for the reported Phase 2 result.

Recommended wording:

> KataGo analysis used `kata1-b28c512nbt-s13255194368-d5935380940`, 50 positions per era, one move at ply 30, `maxVisits=100`, Japanese rules, komi 6.5. Results are treated as a modern-policy proxy and reported as secondary.

---

### P1.2 KataGo result is too small to carry main-claim weight

**Draft locations:** `PAPER_DRAFT_PNAS.md:34-36`, `PAPER_DRAFT_PNAS.md:94-105`

The KataGo comparison uses 200 positions total, 50 per era. It is useful, but it should not be framed as a major pillar unless expanded or given confidence intervals.

**Risk:** PNAS reviewers will expect robust sampling over positions, players, years, and openings.

**Required fix:** Either:

1. Move KataGo alignment to a secondary/supplementary analysis, or
2. Scale it and add uncertainty: more positions, stratification by year/region/player, bootstrap CI.

The main paper can survive without KataGo as a primary pillar because Phase 4D/E already provide the stronger mechanism.

---

### P1.3 "Chroma-rhythm coupling" is claimed, but Results mostly report rhythm centroid drift

**Draft locations:** `PAPER_DRAFT_PNAS.md:14-16`, `PAPER_DRAFT_PNAS.md:28-31`, `PAPER_DRAFT_PNAS.md:75-92`, `PAPER_DRAFT_PNAS.md:184-188`

The draft claims AI did not alter fundamental coupling between game phase and spatial choice. But the result section primarily reports rhythm centroid drift. The Phase 1 result `cross-harm d=-0.029` is not presented in the paper body, and the long-history coupling stability is not quantified.

**Risk:** Reviewers may ask: where is the coupling statistic?

**Required fix:** Add a dedicated result:

```text
2.x Chroma-rhythm coupling remains stable
```

Report the coupling metric, effect size, era split, and uncertainty. If only Phase 1 has this statistic, narrow the claim to:

> rhythm operating point changed within a stable short-era chroma-rhythm coupling estimate

Do not say "fundamental coupling across four centuries" unless that exact analysis exists.

---

### P1.4 Regional distance bootstrap does not match the reported 5-feature metric

**Draft locations:** `PAPER_DRAFT_PNAS.md:155-173`, `PAPER_DRAFT_PNAS.md:237-240`

The reported regional distances are from the 5-feature Phase 4E rhythm vector:

```text
0.0186 -> 0.0070 -> 0.0121 -> 0.0065
```

But `phase5_defense.py` bootstraps a 2-feature distance (`adj_opp`, `adj_own`) and gives different values:

```text
Pre-AI = 0.0043
Shock = 0.0030
Diffusion = 0.0066
Oracle = 0.0040
```

**Risk:** CI/uncertainty cannot be transferred to the main 5-feature result.

**Required fix:** Bootstrap the exact same distance metric used in the paper. Then report CIs for:

- 1990s/pre-AI distance
- 2016-17 shock distance
- 2018-21 diffusion distance
- 2022-25 oracle distance

---

### P1.5 The "reuse rate = lock-in" interpretation is too strong

**Draft locations:** `PAPER_DRAFT_PNAS.md:119-124`, `PAPER_DRAFT_PNAS.md:217-219`

The script defines:

```text
reuse_rate = n_years_used / (last_seen - first_seen + 1)
```

This is not a direct probability that a pattern is locked in after adoption. It is conditional on the observed first-last interval and on the qualifying recurrent pattern set.

**Risk:** "2.2x stronger lock-in" may be viewed as overinterpretation.

**Required fix:** Either compute lock-in with a fixed post-adoption horizon, or call the current metric:

> observed reuse density among recurrent patterns

instead of "lock-in probability."

---

### P1.6 "Professional games from 1600" is historically overbroad

**Draft locations:** `PAPER_DRAFT_PNAS.md:13`, `PAPER_DRAFT_PNAS.md:26-27`, `PAPER_DRAFT_PNAS.md:63-64`, `PAPER_DRAFT_PNAS.md:209`

The archive includes early historical records, castle games, private games, and sparse pre-modern material. Calling the entire 1600-2026 set "professional games" overstates continuity.

**Risk:** A historically informed reviewer may object.

**Required fix:** Use:

> 95,000 recorded games from the CWI Professional Go Archive, including professional, institutional, and historical records.

In Methods, explicitly distinguish early historical records from modern professional tournament records.

---

### P1.7 The paper needs references before PNAS-facing review

**Draft locations:** throughout, especially `PAPER_DRAFT_PNAS.md:25-26`, `PAPER_DRAFT_PNAS.md:48-53`, `PAPER_DRAFT_PNAS.md:184-197`

Claims about AlphaGo, AI changing Go, cultural evolution, and external oracles need citations. The draft currently has no references.

**Required fix:** Add a compact reference spine:

1. AlphaGo / AlphaGo Zero / KataGo papers.
2. Existing empirical work on AI and professional Go.
3. Cultural evolution / transmission / external memory.
4. PNAS Nexus or related "AI and Go knowledge" paper already noted in `DATA_AUDIT.md`.
5. CWI archive/data source citation.

---

## 5. P2 Moderate Issues

### P2.1 "Orthogonal" may be too strong

**Draft locations:** `PAPER_DRAFT_PNAS.md:27-29`, `PAPER_DRAFT_PNAS.md:63-65`

Unless orthogonality is mathematically shown, use "separable" or "factorized". Keep "orthogonal" only if the Methods include the actual construction and independence/correlation checks.

---

### P2.2 "SHP / Saussurean Hash Projection" needs definition or removal from main text

**Draft location:** `PAPER_DRAFT_PNAS.md:65`

PNAS readers will not know SHP. Either define it in plain language or move the term to Methods/SI.

Suggested main-text replacement:

> We factor each move into a game-phase coordinate and a spatial-relation coordinate.

---

### P2.3 Significance Statement may be too jargon-heavy

**Draft locations:** `PAPER_DRAFT_PNAS.md:11-21`

The statement is strong but uses "chroma-rhythm", "Codex", "external oracles", and "structural grammar" in 10 lines. For PNAS, the statement should foreground broad significance in plainer terms.

Suggested direction:

> We show how an external AI system changed not what professional players could play, but how quickly new patterns were discovered and stabilized in a centuries-old cultural record.

---

### P2.4 Defense checklist has now been partially run; draft should reflect that

**Draft locations:** `PAPER_DRAFT_PNAS.md:235-241`

`phase5_defense.py` has now been run. Results:

- Prefix 10 and 15 show strong acceleration.
- Prefix 20 still shortens pre-1980 -> post-2016, but 2000-2015 and 2016+ both show 1.4-year mean lag; the AI-specific step is weaker at prefix 20.
- Player control currently shows event-stream labels, not player nationality.
- Bootstrap CI exists only for a 2-feature regional distance, not the reported 5-feature metric.

Update checklist from "to do" to "partially run; requires exact-metric rerun."

---

### P2.5 Figure plan should separate primary and supplementary results

**Draft locations:** `PAPER_DRAFT_PNAS.md:224-233`

Recommended primary figures:

1. Data/encoding + archive composition.
2. Historical drift envelope and AI-era location.
3. Region-controlled replication + 1910s decomposition.
4. Pattern adoption/reuse speed.
5. Regional three-phase dynamics.

Recommended supplementary:

- KataGo feature-level alignment.
- Prefix-length robustness.
- Event label audit.
- Player-level decomposition.

---

## 6. Additional Observations

### What is strongest

The strongest paper title/claim is no longer "AI changed Go." It is:

> External oracles accelerate cultural Codex circulation without necessarily rewriting structural grammar.

This is a PNAS-style general claim.

### What should be downgraded

Downgrade:

- "Korean style" -> "Korea-coded event stream" until player nationality metadata exists.
- "lock-in probability" -> "reuse density / observed persistence" until fixed-horizon metric exists.
- "KataGo validates" -> "KataGo proxy is consistent with" unless scaled.
- "professional games from 1600" -> "recorded CWI games spanning 1600-2026."

### What should be added

Add:

- Units for every table: games, moves, move-observations, patterns, or years.
- Exact train/test splits.
- Exact region classifier.
- Exact prefix filters.
- Censoring treatment.
- Confidence intervals for the main ratios.
- Data availability and licensing paragraph.

---

## 7. Recommended Rewrite Order

1. Fix all unit errors in tables and text.
2. Replace the `~0.03 drift` contradiction.
3. Rewrite regional claims as event-stream claims.
4. Add a short "Archive and measurement units" subsection to Methods.
5. Add censoring-aware adoption analysis or downgrade the adoption claim.
6. Correct KataGo model/methods and move it to secondary unless scaled.
7. Add missing coupling statistic or narrow the coupling claim.
8. Add references and data availability.
9. Update figures to emphasize the main causal/mechanistic chain.

---

## 8. Submission Readiness

Current readiness:

```text
Story:              strong
Novelty:            strong
PNAS fit:           plausible
Numerical hygiene:  not ready
Methods clarity:    not ready
Defense analyses:   partially ready
Submission status:  no-submit
```

Recommended next milestone:

> Produce `PAPER_DRAFT_PNAS_v2.md` after resolving P0/P1 issues, then run a second audit focused on PNAS desk-review framing.

