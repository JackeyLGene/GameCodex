"""Phase 4D: Pattern Adoption & Survival.

Track opening patterns through time: when they appear, how they spread
across players and regions, and whether historical Codex predicts adoption.

Pattern: opening prefix hash (first 10/15 moves as string key).

Metrics:
  - first_seen: year of first appearance
  - adoption_lag: years from first_seen to >=3 unique players
  - survival_half_life: years from peak usage to half-peak
  - cross_region_lag: years between first regions
  - reuse_rate: fraction of subsequent years with usage
  - Codex Δ: does historical frequency predict next-year adoption?
"""
import csv, json, statistics, math, os, random
from collections import defaultdict, Counter

random.seed(42)

# ═══ Region classifier ═══
JPN_KW = ['meijin','kisei','honinbo','oza','tengen','gosei','judan','nhk',
    'oteai','jal','nec','shinjin','king of new star','ryusei','agon','daiwa',
    'go-net','sumitomo','kirin','all japan','japan','kakusei','shin-ei','hayago']
KOR_KW = ['samsung','nongshim','lg','bc card','gs caltex','maxim','korean',
    'kuksu','myungin','chunwon','prices information','wonik','siptan','korea',
    'baduk','hanguk','kbs','olleh','kt','masters']
CHN_KW = ['mlily','chinese','tianyuan','mingren','changqi','quzhou',
    'longxing','bailing','weifu','xinao','china','weichi']

def classify(event):
    if not event: return 'JPN'
    e = event.lower().strip()
    for kw in JPN_KW:
        if kw in e: return 'JPN'
    for kw in KOR_KW:
        if kw in e: return 'KOR'
    for kw in CHN_KW:
        if kw in e: return 'CHN'
    return 'JPN'

# ═══ Pattern extraction ═══
parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'

# pattern -> {year: usage_count}
pattern_years = defaultdict(lambda: defaultdict(int))
# pattern -> {year: set of players}
pattern_players = defaultdict(lambda: defaultdict(set))
# pattern -> {year: set of regions}
pattern_regions = defaultdict(lambda: defaultdict(set))
# year -> total games
year_totals = Counter()

PREFIX_LEN = 15  # first 15 moves

with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','')
        if not y or y=='None': continue
        year = int(y)
        if year < 1950 or year > 2025: continue
        moves = json.loads(row.get('moves','[]'))
        if len(moves) < PREFIX_LEN + 1: continue

        # Pattern: first 15 moves as comma-separated string
        prefix = ','.join(f"{c}{coord}" for c,coord in moves[:PREFIX_LEN])
        pattern_years[prefix][year] += 1
        pattern_players[prefix][year].add(row.get('black_player',''))
        pattern_players[prefix][year].add(row.get('white_player',''))
        event = row.get('event','')
        region = classify(event)
        pattern_regions[prefix][year].add(region)
        year_totals[year] += 1

# Filter: patterns appearing in >=3 years with >=5 total uses
min_patterns = {p: d for p, d in pattern_years.items()
                if len(d) >= 3 and sum(d.values()) >= 5}
print(f"Total patterns: {len(pattern_years)}, "
      f"Qualifying (>=3 years, >=5 uses): {len(min_patterns)}")

# ═══ Per-pattern metrics ═══
pattern_metrics = []
for pattern, year_data in min_patterns.items():
    years = sorted(year_data.keys())
    first_seen = years[0]
    last_seen = years[-1]
    total_uses = sum(year_data.values())
    n_years = len(years)

    # Peak year and usage
    peak_year = max(years, key=lambda y: year_data[y])
    peak_usage = year_data[peak_year]

    # Survival half-life: years from peak to <= half peak
    half_life = None
    for y in range(peak_year, last_seen + 1):
        if year_data.get(y, 0) <= peak_usage / 2:
            half_life = y - peak_year
            break
    if half_life is None:
        half_life = last_seen - peak_year

    # Adoption lag: years from first_seen to >=3 unique players
    adoption_lag = None
    for y in years:
        if len(pattern_players[pattern][y]) >= 3:
            adoption_lag = y - first_seen
            break

    # Cross-region lag: years between first and second region
    regions_seen = sorted(pattern_regions[pattern][y] for y in years)
    all_regions = set()
    region_years = []
    for y in years:
        prev = all_regions.copy()
        all_regions.update(pattern_regions[pattern][y])
        if len(all_regions) > len(prev):
            region_years.append(y)
    cross_region_lag = (region_years[1] - region_years[0]) if len(region_years) >= 2 else None

    # Reuse rate: fraction of years between first and last with usage
    reuse_rate = n_years / max(1, last_seen - first_seen + 1)

    pattern_metrics.append({
        'pattern': pattern[:60],
        'first_seen': first_seen,
        'last_seen': last_seen,
        'peak_year': peak_year,
        'peak_usage': peak_usage,
        'total_uses': total_uses,
        'n_years': n_years,
        'adoption_lag': adoption_lag,
        'half_life': half_life,
        'cross_region_lag': cross_region_lag,
        'reuse_rate': reuse_rate,
        'n_regions': len(all_regions),
    })

# ═══ Report ═══
print(f"\n{'='*60}")
print(f"PHASE 4D: PATTERN ADOPTION & SURVIVAL")
print(f"{'='*60}")

print(f"\n  Pattern metrics summary (N={len(pattern_metrics)}):")
for name, key in [('First seen', 'first_seen'), ('Last seen', 'last_seen'),
                   ('Peak usage', 'peak_usage'), ('Adoption lag (yr)', 'adoption_lag'),
                   ('Half-life (yr)', 'half_life'), ('Cross-region lag (yr)', 'cross_region_lag'),
                   ('Reuse rate', 'reuse_rate'), ('N regions', 'n_regions')]:
    vals = [m[key] for m in pattern_metrics if m[key] is not None]
    if vals:
        print(f"    {name:<22}: mean={statistics.mean(vals):.1f}  "
              f"median={statistics.median(vals):.1f}  "
              f"N={len(vals)}")

# ═══ By era of first_seen ═══
print(f"\n{'='*60}")
print(f"PATTERN METRICS BY ERA OF FIRST APPEARANCE")
print(f"{'='*60}")
print(f"  {'Era':<12} {'N_patterns':>12} {'Mean adopt_lag':>14} {'Mean half_life':>14} {'Mean reuse':>12}")
for era, y0, y1 in [('pre-1980', 1950, 1979), ('1980-1999', 1980, 1999),
                        ('2000-2015', 2000, 2015), ('2016+', 2016, 2025)]:
    era_m = [m for m in pattern_metrics if y0 <= m['first_seen'] <= y1]
    if not era_m: continue
    al = statistics.mean(m['adoption_lag'] for m in era_m if m['adoption_lag'] is not None)
    hl = statistics.mean(m['half_life'] for m in era_m if m['half_life'] is not None)
    rr = statistics.mean(m['reuse_rate'] for m in era_m)
    print(f"  {era:<12} {len(era_m):>12} {al:>14.1f} {hl:>14.1f} {rr:>12.3f}")

# ═══ Codex Δ: does historical freq predict next-year adoption? ═══
print(f"\n{'='*60}")
print(f"CODEX Δ: Historical pattern frequency -> next-year prediction")
print(f"{'='*60}")

# For each year t (1990+), predict which patterns will be used in t+1
# Codex model: patterns used in year t are more likely to be reused in t+1
# Frequency baseline: random pattern from the pool

years = sorted(y for y in year_totals if 1990 <= y <= 2024)
codex_hits = []
freq_hits = []
n_predictions = 0

for i in range(len(years)-1):
    t = years[i]
    t1 = years[i+1]

    # Patterns used in year t
    active_t = {p for p, d in pattern_years.items() if d.get(t, 0) > 0}
    # Patterns used in year t+1
    active_t1 = {p for p, d in pattern_years.items() if d.get(t1, 0) > 0}

    if len(active_t) < 10 or len(active_t1) < 10: continue

    # Codex: predict top-N patterns from year t will persist
    top_n = 50
    top_t = sorted(active_t, key=lambda p: pattern_years[p].get(t, 0), reverse=True)[:top_n]
    codex_correct = len(set(top_t) & active_t1)
    codex_hits.append(codex_correct / top_n)

    # Frequency baseline: random patterns from all-time pool
    all_patterns = list(min_patterns.keys())
    if len(all_patterns) >= top_n:
        random_sample = set(random.sample(all_patterns, top_n))
        freq_correct = len(random_sample & active_t1)
        freq_hits.append(freq_correct / top_n)

    n_predictions += 1

if codex_hits:
    mean_codex = statistics.mean(codex_hits)
    mean_freq = statistics.mean(freq_hits)
    delta = mean_codex - mean_freq

    print(f"  Years tested: {n_predictions}")
    print(f"  Codex hit rate:     {mean_codex:.4f} (top-50 from year t)")
    print(f"  Frequency hit rate: {mean_freq:.4f} (random patterns)")
    print(f"  Δ:                  {delta:+.4f}")
    if delta > 0:
        print(f"  → Historical pattern frequency predicts future adoption")
        print(f"    beyond random baseline.")
    else:
        print(f"  → Pattern recency does not beat random baseline.")

# ═══ Longest-lived patterns ═══
print(f"\n{'='*60}")
print(f"TOP 20 LONGEST-LIVED PATTERNS")
print(f"{'='*60}")

for m in sorted(pattern_metrics, key=lambda x: -x['total_uses'])[:20]:
    lifespan = m['last_seen'] - m['first_seen']
    print(f"  {m['pattern'][:50]:<52} "
          f"first={m['first_seen']} peak={m['peak_year']}({m['peak_usage']}) "
          f"span={lifespan}yr reuse={m['reuse_rate']:.2f}")

# ═══ Save ═══
out_dir = 'G:/GameCodex/results/phase4'
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, 'pattern_metrics.csv')
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(pattern_metrics[0].keys()))
    w.writeheader()
    for m in pattern_metrics:
        w.writerow(m)
print(f"\nSaved {len(pattern_metrics)} patterns to {out}")
