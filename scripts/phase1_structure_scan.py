"""Phase 1: SHP structure scan — year-level trends, era separation, variance.

Reads shp_game_level.csv, produces:
  1. Year-level cross-harm trend
  2. Chroma/rhythm centroid displacement (E0 vs E3)
  3. Variance change by era
  4. Opening-only (first 50 moves) re-analysis
"""
import csv, json, statistics, math, os
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════
# Load data
# ═══════════════════════════════════════════════════════════════

annual = []
with open('G:/GameCodex/results/shp_annual.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        row['year'] = int(row['year'])
        row['n_games'] = int(row['n_games'])
        row['mean_cross_harm'] = float(row['mean_cross_harm'])
        row['sd_cross_harm'] = float(row['sd_cross_harm'])
        row['chroma_mean'] = json.loads(row['chroma_mean'])
        row['rhythm_mean'] = json.loads(row['rhythm_mean'])
        annual.append(row)

annual.sort(key=lambda r: r['year'])

game_level = defaultdict(list)  # year -> [cross_harm_values]
with open('G:/GameCodex/results/shp_game_level.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = int(row['year'])
        game_level[y].append(float(row['mean_cross_harm']))

# ═══════════════════════════════════════════════════════════════
# 1. Year-level cross-harm trend
# ═══════════════════════════════════════════════════════════════

print("=" * 60)
print("1. YEAR-LEVEL CROSS-HARM TREND")
print("=" * 60)
print(f"  {'Year':<6} {'N':>6} {'CrossHarm':>10} {'SD':>8} {'Era':>5}")
print(f"  {'-'*6} {'-'*6} {'-'*10} {'-'*8} {'-'*5}")

for r in annual:
    era = 'E0' if r['year'] <= 2015 else ('E1' if r['year'] <= 2017 else
           ('E2' if r['year'] <= 2021 else 'E3'))
    print(f"  {r['year']:<6} {r['n_games']:>6} {r['mean_cross_harm']:>10.1f} "
          f"{r['sd_cross_harm']:>8.1f} {era:>5}")

# ═══════════════════════════════════════════════════════════════
# 2. Era comparison with effect sizes
# ═══════════════════════════════════════════════════════════════

def cohen_d(a, b):
    if len(a) < 2 or len(b) < 2:
        return 0
    pooled = ((statistics.stdev(a)**2 + statistics.stdev(b)**2) / 2) ** 0.5
    return (statistics.mean(a) - statistics.mean(b)) / max(0.001, pooled)

print(f"\n{'='*60}")
print(f"2. ERA COMPARISON (Cohen d)")
print(f"{'='*60}")

eras = {'E0': (2000, 2015), 'E1': (2016, 2017), 'E2': (2018, 2021), 'E3': (2022, 2026)}
era_ch = {}
for era, (y0, y1) in eras.items():
    vals = []
    for y, ch_list in game_level.items():
        if y0 <= y <= y1:
            vals.extend(ch_list)
    era_ch[era] = vals
    print(f"  {era}: mean={statistics.mean(vals):.1f}  sd={statistics.stdev(vals):.1f}  n={len(vals)}")

for era_a, era_b in [('E0', 'E3'), ('E0', 'E1'), ('E1', 'E3')]:
    if era_a in era_ch and era_b in era_ch:
        d = cohen_d(era_ch[era_a], era_ch[era_b])
        print(f"  d({era_a} vs {era_b}) = {d:+.3f}")

# ═══════════════════════════════════════════════════════════════
# 3. Chroma centroid displacement
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"3. CHROMA CENTROID DISPLACEMENT (E0 -> E3)")
print(f"{'='*60}")

e0_chroma = [r['chroma_mean'] for r in annual if r['year'] <= 2015]
e3_chroma = [r['chroma_mean'] for r in annual if r['year'] >= 2022]

if e0_chroma and e3_chroma:
    nc = len(e0_chroma[0])
    e0c = [statistics.mean([v[d] for v in e0_chroma]) for d in range(nc)]
    e3c = [statistics.mean([v[d] for v in e3_chroma]) for d in range(nc)]
    chroma_names = ['move_idx_raw', 'move_norm_300', 'board_occ', 'occ_bin',
                    'open', 'early_mid', 'mid', 'late_mid', 'endgame']
    print(f"  {'Dim':<14} {'E0':>8} {'E3':>8} {'Δ':>8} {'d':>8}")
    for d in range(min(nc, len(chroma_names))):
        # Compute per-game values for Cohen's d
        e0_vals = [r['chroma_mean'][d] for r in annual if r['year'] <= 2015]
        e3_vals = [r['chroma_mean'][d] for r in annual if r['year'] >= 2022]
        d_val = cohen_d(e0_vals, e3_vals)
        delta = e3c[d] - e0c[d]
        print(f"  {chroma_names[d]:<14} {e0c[d]:>8.3f} {e3c[d]:>8.3f} {delta:>+8.3f} {d_val:>+8.3f}")

# ═══════════════════════════════════════════════════════════════
# 4. Rhythm centroid displacement
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"4. RHYTHM CENTROID DISPLACEMENT (E0 -> E3)")
print(f"{'='*60}")

e0_rhythm = [r['rhythm_mean'] for r in annual if r['year'] <= 2015]
e3_rhythm = [r['rhythm_mean'] for r in annual if r['year'] >= 2022]

if e0_rhythm and e3_rhythm:
    nr = len(e0_rhythm[0])
    e0r = [statistics.mean([v[d] for v in e0_rhythm]) for d in range(nr)]
    e3r = [statistics.mean([v[d] for v in e3_rhythm]) for d in range(nr)]
    rhythm_names = ['dist_last', 'dist_near_any', 'dist_near_own', 'dist_near_opp',
                    'own_dens_r3', 'opp_dens_r3', 'adj_own', 'adj_opp',
                    'edge_d', 'corner_d', 'is_corner_open', 'dens_delta']
    print(f"  {'Dim':<16} {'E0':>8} {'E3':>8} {'Δ':>8} {'d':>8}")
    for d in range(min(nr, len(rhythm_names))):
        e0_vals = [r['rhythm_mean'][d] for r in annual if r['year'] <= 2015]
        e3_vals = [r['rhythm_mean'][d] for r in annual if r['year'] >= 2022]
        d_val = cohen_d(e0_vals, e3_vals)
        delta = e3r[d] - e0r[d]
        marker = '*' if abs(d_val) > 0.5 else ('+' if abs(d_val) > 0.2 else '')
        print(f"  {rhythm_names[d]:<16} {e0r[d]:>8.4f} {e3r[d]:>8.4f} {delta:>+8.4f} {d_val:>+8.3f} {marker}")

# ═══════════════════════════════════════════════════════════════
# 5. Variance structure
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"5. VARIANCE STRUCTURE BY ERA")
print(f"{'='*60}")

# Within-era variance of cross-harm
print(f"  Cross-harm SD by era:")
for era, vals in era_ch.items():
    print(f"    {era}: sd={statistics.stdev(vals):.1f}")

# Coefficient of variation
print(f"\n  Cross-harm CV (sd/mean) by era:")
for era, vals in era_ch.items():
    cv = statistics.stdev(vals) / max(0.001, statistics.mean(vals))
    print(f"    {era}: cv={cv:.4f}")

# ═══════════════════════════════════════════════════════════════
# 6. Year-level correlation: cross-harm vs sample size
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"6. CONTROL: Cross-harm vs sample size")
print(f"{'='*60}")

years_list = [r['year'] for r in annual]
ch_list = [r['mean_cross_harm'] for r in annual]
n_list = [r['n_games'] for r in annual]

def spearman(x, y):
    n = len(x)
    def rk(v):
        idx = sorted(range(n), key=lambda i: v[i]); r = [0]*n; i = 0
        while i < n:
            j = i
            while j < n and v[idx[j]] == v[idx[i]]: j += 1
            for k in range(i, j): r[idx[k]] = (i+j-1)/2; i = j
        return r
    rx, ry = rk(x), rk(y); mx, my = statistics.mean(rx), statistics.mean(ry)
    return sum((rx[i]-mx)*(ry[i]-my) for i in range(n)) / max(.001,
        math.sqrt(sum((rx[i]-mx)**2 for i in range(n)) *
                 sum((ry[i]-my)**2 for i in range(n))))

rho_n = spearman(ch_list, n_list)
print(f"  ρ(cross_harm, n_games) = {rho_n:+.3f}")

# ═══════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")

max_ch_year = max(annual, key=lambda r: r['mean_cross_harm'])
min_ch_year = min(annual, key=lambda r: r['mean_cross_harm'])
print(f"  Cross-harm range: {min_ch_year['mean_cross_harm']:.1f} ({min_ch_year['year']}) "
      f"- {max_ch_year['mean_cross_harm']:.1f} ({max_ch_year['year']})")

d_e0e3 = cohen_d(era_ch.get('E0', []), era_ch.get('E3', []))
print(f"  d(E0 vs E3) cross-harm: {d_e0e3:+.3f}")

# Which features changed most?
if e0_rhythm and e3_rhythm:
    nr = len(e0_rhythm[0])
    changes = []
    for d in range(nr):
        e0v = [r['rhythm_mean'][d] for r in annual if r['year'] <= 2015]
        e3v = [r['rhythm_mean'][d] for r in annual if r['year'] >= 2022]
        d_val = cohen_d(e0v, e3v)
        changes.append((d, rhythm_names[d], d_val))
    changes.sort(key=lambda x: -abs(x[2]))
    print(f"\n  Top 5 rhythm changes (E0->E3):")
    for d, name, d_val in changes[:5]:
        print(f"    {name:<20} d={d_val:+.3f}")

# Decision
print(f"\n  Phase 1 conclusion:")
if abs(d_e0e3) > 0.3:
    print(f"    → AI transition detected in SHP cross-harm (d={d_e0e3:+.2f}).")
    print(f"    → Proceed to Phase 2 (KataGo alignment).")
elif any(abs(c[2]) > 0.5 for c in changes[:3]):
    print(f"    → Cross-harm stable, but specific rhythm dimensions shifted.")
    print(f"    → Proceed to Phase 2 with focus on {changes[0][1]}.")
else:
    print(f"    → SHP cross-harm shows no meaningful AI-era shift (d={d_e0e3:+.2f}).")
    print(f"    → No individual dimension shows strong change.")
    print(f"    → Go timeline plan: Phase 1 null. Continue to Phase 2 or stop per rules.")
