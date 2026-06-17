# Data Audit — Go Professional Game Records

**Date:** 2026-06-14
**Status:** Phase 0 data audit for GoCodex timeline plan.

---

## 1. Data Sources

### Primary: CWI Japanese Professional Go SGF Archive

| Field | Value |
|-------|-------|
| URL | https://homepages.cwi.nl/~aeb/go/games/games/ |
| Size | ~46 MB compressed (.tar.gz) |
| Games | 90,000+ Japanese professional games |
| Period | ~1600–2025, continuously updated |
| Format | SGF (Smart Game Format) |
| License | Freely downloadable; academic use standard |
| Key fields | Date, players, rank, result, komi, moves, event |

**Coverage by era:**
- E0 (2000-2015): Well covered, Japanese pro leagues active
- E1 (2016-2017): Covered
- E2 (2018-2021): Covered
- E3 (2022+): Covered through 2025

**Limitations:**
- Japan-centric (Kansai Ki-in, Nihon Ki-in). Missing Korean (Hanguk Kiwon) and Chinese (Zhongguo Qiyuan) games.
- May under-represent international tournaments.
- Player rank is Japanese dan/kyu system.

### Secondary: GoGoD Database

| Field | Value |
|-------|-------|
| Source | GoGoD (Games of Go on Disk) |
| Games | 124,534 (July 2024) |
| Coverage | All major pro leagues, global |
| Format | SGF |
| License | Commercial; academic access may be available |
| Used by | Beheim 2025 (Cambridge), GoGoD Summer 2024 |

**Advantage over CWI:** Global coverage (Japan + Korea + China + international).
**Disadvantage:** Commercial license needs clearance.

### Supplementary: Go4Go

| Field | Value |
|-------|-------|
| Games | ~70,000 professional (2003-2021) |
| Used by | PNAS Nexus 2025 "The Dual Edges of AI" |
| License | Subscription-based |

### Fallback: Hugging Face go_pgn_string_v2

| Field | Value |
|-------|-------|
| URL | https://huggingface.co/datasets/kenhktsui/go_pgn_string_v2 |
| Format | PGN-like text, includes Elo ratings |
| Source | Derived from GoGoD |
| License | Check dataset card |

---

## 2. First-Step Action Plan

### Step 1: Download CWI archive (immediate)
```bash
wget https://homepages.cwi.nl/~aeb/go/games/games.tar.gz
```
Size: 46 MB. Can be done immediately. This gives us a working dataset.

### Step 2: Parse SGF to standardized format
- Extract: date, black_player, white_player, black_rank, white_rank, result, komi, rules, moves (B/W alternating).
- Map date to year, assign era.
- Validate year field — critical for time-series analysis.
- Count games per year. Ensure >= 500/year for E0-E2 eras.

### Step 3: Assess coverage gaps
- What years have < 500 games?
- Is there a systematic Japan bias (e.g., Korean Baduk / Chinese Weiqi under-sampled)?
- Is player rank consistently available?

### Step 4: Decision
- If CWI covers E0-E2 adequately (>= 500 games/year), proceed with Phase 1.
- If coverage gaps are significant, pursue GoGoD academic access.
- If neither works, fall back to International Chess.

---

## 3. Minimum Viable Data Requirements

| Requirement | Threshold | Check |
|-------------|-----------|-------|
| Total games | >= 10,000 | CWI: 90,000+ ✓ |
| Games/year E0 | >= 500 | TBD |
| Games/year E1 | >= 500 | TBD |
| Games/year E2 | >= 500 | TBD |
| Date field usable | Year granularity | TBD |
| Player rank | Available for stratification | TBD |
| License publishable | Academic use OK | TBD |
| Korea/China coverage | Supplementary | TBD (GoGoD if needed) |

---

## 4. Related Academic Work

| Paper | Year | Data | Key finding |
|-------|------|------|-------------|
| Beheim, "Opening Strategies in Go from Feudalism to Superhuman AI" | 2025 | GoGoD 124K games | Move diversity, network analysis, AI impact |
| "The Dual Edges of AI" (PNAS Nexus) | 2025 | Go4Go 70K games | Post-AI: new knowledge created but diversity decreased |
| PAGE dataset | ? | Professional Go games | Need to verify existence/access |

**Key gap we fill:** None of these ask the Codex operation question — does historical opening structure improve future move prediction? They analyze diversity and knowledge creation; we analyze whether the externalized Codex changes how players choose moves.

---

## 5. Stop/Go Decision

After Step 2 (SGF parse + year validation):
- **Go:** if >= 10,000 games with valid year fields across E0-E2.
- **Go with caveats:** if Japan-only but >= 500/year per era. Note geographic bias in paper.
- **Fallback to Chess:** if SGF data insufficient or license unclear for publication.
