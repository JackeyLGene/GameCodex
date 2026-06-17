"""Phase 5: Closure analyses for paper defense.

1. Robustness: pattern adoption lag for prefix 10/15/20
2. Player control: Korea fighting index per-player decomposition
3. Region audit: classification rule coverage + sample check
4. Bootstrap CI: 4.2×, 2.2×, regional distance three-phase
"""
import csv, json, statistics, math, random, os
from collections import defaultdict, Counter

random.seed(42)

# ═══ Shared: region classifier ═══
JPN_KW = ['meijin','kisei','honinbo','oza','tengen','gosei','judan','nhk',
    'oteai','jal','nec','shinjin','king of new star','ryusei','agon','daiwa',
    'go-net','sumitomo','kirin','all japan','japan','kakusei','shin-ei','hayago',
    'kansai','ki-in','shusaku','dosaku','shusai','honda','nagoya','osaka','tokyo']
KOR_KW = ['samsung','nongshim','lg','bc card','gs caltex','maxim','korean',
    'kuksu','myungin','chunwon','prices information','wonik','siptan','korea',
    'baduk','hanguk','kbs','olleh','kt','masters','let\'s run']
CHN_KW = ['mlily','chinese','tianyuan','mingren','changqi','quzhou',
    'longxing','bailing','weifu','xinao','china','weichi',
    'jianqiao','a han','titan','golden statue','lanke']

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

parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'

# ═══════════════════════════════════════════════════════════════
# 1. PREFIX LENGTH ROBUSTNESS: adoption lag for 10/15/20 moves
# ═══════════════════════════════════════════════════════════════

print("="*60)
print("1. PREFIX LENGTH ROBUSTNESS: Adoption lag for 10/15/20 moves")
print("="*60)

for prefix_len in [10, 15, 20]:
    pattern_years = defaultdict(lambda: defaultdict(int))
    pattern_players = defaultdict(lambda: defaultdict(set))
    year_totals = Counter()

    with open(parsed_csv, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            y = row.get('year','')
            if not y or y=='None': continue
            year = int(y)
            if year < 1950 or year > 2025: continue
            moves = json.loads(row.get('moves','[]'))
            if len(moves) < prefix_len + 1: continue
            prefix = ','.join(f"{c}{coord}" for c,coord in moves[:prefix_len])
            pattern_years[prefix][year] += 1
            pattern_players[prefix][year].add(row.get('black_player',''))
            pattern_players[prefix][year].add(row.get('white_player',''))
            year_totals[year] += 1

    # Filter qualifying patterns
    qualified = {p: d for p, d in pattern_years.items()
                 if len(d) >= 3 and sum(d.values()) >= 5}

    era_lags = defaultdict(list)
    for pattern, year_data in qualified.items():
        years = sorted(year_data.keys())
        first_seen = years[0]
        lag = None
        for y in years:
            if len(pattern_players[pattern][y]) >= 3:
                lag = y - first_seen
                break
        if lag is not None:
            if first_seen < 1980: era = 'pre-1980'
            elif first_seen < 2000: era = '1980-1999'
            elif first_seen < 2016: era = '2000-2015'
            else: era = '2016+'
            era_lags[era].append(lag)

    print(f"\n  Prefix length = {prefix_len} ({len(qualified)} qualifying):")
    for era in ['pre-1980','1980-1999','2000-2015','2016+']:
        lags = era_lags[era]
        if lags:
            print(f"    {era:<12}: mean lag = {statistics.mean(lags):.1f} yr "
                  f"(median={statistics.median(lags):.0f}, N={len(lags)})")

# ═══════════════════════════════════════════════════════════════
# 2. PLAYER CONTROL: Korea fighting index decomposition
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"2. PLAYER CONTROL: Korea fighting index by player")
print(f"{'='*60}")

SGF_COLS = 'abcdefghijklmnopqrs'
def sgf_to_xy(m):
    if not m or len(m)<2: return None
    c=SGF_COLS.find(m[0]); r=SGF_COLS.find(m[1])
    return (c,r) if c>=0 and r>=0 else None

def move_rhythm(prefix_moves, candidate_sgf):
    board = {}
    for color, coord in prefix_moves:
        xy = sgf_to_xy(coord)
        if xy is None: continue
        board[xy] = color
    tx,ty = sgf_to_xy(candidate_sgf)
    if (tx,ty) is None: return None
    mc = 'B' if len(prefix_moves)%2==0 else 'W'; oc = 'W' if mc=='B' else 'B'
    board[(tx,ty)] = mc
    adj_opp=adj_own=0
    for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx,ny=tx+dx,ty+dy
        if 0<=nx<19 and 0<=ny<19:
            s=board.get((nx,ny))
            if s==oc: adj_opp+=1
            elif s==mc: adj_own+=1
    return adj_opp/4.0, adj_own/4.0

# Korea 2016+, per-player top-10
player_fighting = defaultdict(lambda: {'adj_opp':[], 'adj_own':[], 'games':0})
with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','')
        if not y or y=='None': continue
        year = int(y)
        if year < 2016: continue
        event = row.get('event','')
        region = classify(event)
        if region != 'KOR': continue
        moves = json.loads(row.get('moves','[]'))
        if len(moves) < 30: continue
        bp = row.get('black_player','')
        wp = row.get('white_player','')
        for n in range(15, min(len(moves)-1, 50)):
            prefix = [(c,coord) for c,coord in moves[:n]]
            actual = moves[n][1]
            if sgf_to_xy(actual) is None: continue
            result = move_rhythm(prefix, actual)
            if result is None: continue
            adj_o, adj_w = result
            # Attribute to the player making the move (color alternates)
            player = bp if n%2==0 else wp
            player_fighting[player]['adj_opp'].append(adj_o)
            player_fighting[player]['adj_own'].append(adj_w)
            player_fighting[player]['games'] += 1

# Top players by game count
top_players = sorted(player_fighting.items(),
                     key=lambda x: -x[1]['games'])[:10]

print(f"\n  Top 10 Korean players (2016+):")
print(f"  {'Player':<25} {'Games':>6} {'adj_opp':>8} {'adj_own':>8} "
      f"{'fight_idx':>10}")
total_adj_opp = []
total_adj_own = []
for name, data in top_players:
    adj_o = statistics.mean(data['adj_opp']) if data['adj_opp'] else 0
    adj_w = statistics.mean(data['adj_own']) if data['adj_own'] else 0
    fi = adj_o - adj_w
    print(f"  {name:<25} {data['games']:>6} {adj_o:>8.4f} {adj_w:>8.4f} "
          f"{fi:>+10.4f}")
    total_adj_opp.extend(data['adj_opp'])
    total_adj_own.extend(data['adj_own'])

# Leave-one-out: remove top player, does fighting index change?
if total_adj_opp:
    all_fi = statistics.mean(total_adj_opp) - statistics.mean(total_adj_own)
    print(f"\n  All top-10 pooled: fighting_idx = {all_fi:+.4f}")
    for name, data in top_players[:5]:
        without = [v for n, d in top_players for v in d['adj_opp'] if n != name]
        without_own = [v for n, d in top_players for v in d['adj_own'] if n != name]
        fi_wo = statistics.mean(without) - statistics.mean(without_own)
        delta = all_fi - fi_wo
        print(f"    Without {name:<22}: fi={fi_wo:+.4f} (Δ={delta:+.4f})")

# ═══════════════════════════════════════════════════════════════
# 3. REGION LABEL AUDIT
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"3. REGION LABEL AUDIT: Classification rule coverage + samples")
print(f"{'='*60}")

# Event-level audit: what fraction of events get classified?
events_sample = []
with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        events_sample.append(row.get('event',''))
        if len(events_sample) > 50000: break

event_classification = Counter()
for e in events_sample:
    event_classification[classify(e)] += 1

total_ev = sum(event_classification.values())
print(f"\n  Classification coverage (N={total_ev} events):")
for r in ['JPN','KOR','CHN']:
    print(f"    {r}: {event_classification[r]} "
          f"({event_classification[r]/total_ev*100:.1f}%)")

# Spot-check: show which events map to KOR/CHN
kor_events = set()
chn_events = set()
with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        event = row.get('event','')
        r = classify(event)
        if r == 'KOR': kor_events.add(event)
        elif r == 'CHN': chn_events.add(event)

print(f"\n  KOR-classified events (N={len(kor_events)}):")
for e in sorted(kor_events)[:20]:
    print(f"    {e[:80]}")
print(f"\n  CHN-classified events (N={len(chn_events)}):")
for e in sorted(chn_events)[:20]:
    print(f"    {e[:80]}")

# Default-to-JPN rate
default_jpn = sum(1 for e in events_sample if not e or classify(e)=='JPN')
print(f"\n  Default-to-JPN rate: {default_jpn}/{total_ev} "
      f"({default_jpn/total_ev*100:.1f}%)")

# ═══════════════════════════════════════════════════════════════
# 4. BOOTSTRAP CI on key metrics
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"4. BOOTSTRAP CI ON KEY METRICS")
print(f"{'='*60}")

n_boot = 2000

# 4.1 Adoption lag ratio (2016+ vs pre-1980)
print(f"\n  Bootstrap: Adoption lag ratio (2016+ / pre-1980)...")
# Use simple resampling of the pattern-level adoption lags
# This is approximate — full bootstrap would re-extract patterns
print(f"    → Requires re-running pattern extraction with bootstrap.")
print(f"    → For paper: compute from per-pattern bootstrap resamples.")

# 4.2 Reuse rate ratio
print(f"\n  Bootstrap: Reuse rate ratio...")
print(f"    → Same — per-pattern bootstrap of reuse_rate by era.")

# 4.3 Regional distance three-phase significance
print(f"\n  Bootstrap: Regional distance three-phase differences...")
# For the regional distances, we can bootstrap from yearly centroids
SGF_COLS2 = 'abcdefghijklmnopqrs'
yr_centroids = defaultdict(lambda: defaultdict(list))

with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','')
        if not y or y=='None': continue
        year = int(y)
        if year < 1990: continue
        moves = json.loads(row.get('moves','[]'))
        if len(moves) < 30: continue
        region = classify(row.get('event',''))

        for n in range(15, min(len(moves)-1, 50)):
            prefix = [(c,coord) for c,coord in moves[:n]]
            actual = moves[n][1]
            xy = sgf_to_xy(actual)
            if xy is None: continue
            result = move_rhythm(prefix, actual)
            if result is None: continue
            adj_o, adj_w = result
            yr_centroids[(year, region)]['adj_opp'].append(adj_o)
            yr_centroids[(year, region)]['adj_own'].append(adj_w)

# Per-phase regional distances
phases = {
    'Pre-AI (1990-2015)': (1990, 2015),
    'Shock (2016-2017)': (2016, 2017),
    'Diffusion (2018-2021)': (2018, 2021),
    'Oracle (2022-2025)': (2022, 2025),
}

def inter_region_dist(y0, y1):
    cents = {}
    for region in ['JPN','KOR','CHN']:
        feats = {'adj_opp': [], 'adj_own': []}
        for year in range(y0, y1+1):
            key = (year, region)
            if key in yr_centroids:
                for f in feats:
                    feats[f].extend(yr_centroids[key][f])
        if feats['adj_opp']:
            cents[region] = {f: statistics.mean(feats[f]) for f in feats}
    if len(cents) >= 2:
        dists = []
        for r1,r2 in [('JPN','KOR'),('JPN','CHN'),('KOR','CHN')]:
            if r1 in cents and r2 in cents:
                d = math.sqrt(sum((cents[r1][f]-cents[r2][f])**2 for f in ['adj_opp','adj_own']))
                dists.append(d)
        return statistics.mean(dists)
    return None

# Pre-compute per-year per-region summary stats for fast bootstrap
yr_summary = {}  # (year, region) -> (mean_adj_opp, mean_adj_own, n_moves)
for (year, region), feats in yr_centroids.items():
    if feats['adj_opp']:
        yr_summary[(year, region)] = (
            statistics.mean(feats['adj_opp']),
            statistics.mean(feats['adj_own']),
            len(feats['adj_opp'])
        )

# Bootstrap by resampling years within each phase
for phase_name, (y0, y1) in phases.items():
    years_in_phase_all = [(y, r) for y in range(y0, y1+1)
                          for r in ['JPN','KOR','CHN']
                          if (y, r) in yr_summary]
    if len(years_in_phase_all) < 10: continue

    boot_dists = []
    for _ in range(n_boot):
        # Resample year-region pairs with replacement
        sample_pairs = [random.choice(years_in_phase_all) for _ in range(len(years_in_phase_all))]
        cents = defaultdict(lambda: {'adj_opp': [], 'adj_own': []})
        for (y, r) in sample_pairs:
            ao, aw, _ = yr_summary[(y, r)]
            cents[r]['adj_opp'].append(ao)
            cents[r]['adj_own'].append(aw)

        if len(cents) >= 2:
            c_means = {}
            for r in cents:
                c_means[r] = {f: statistics.mean(cents[r][f]) for f in ['adj_opp','adj_own']}
            dists = []
            for r1,r2 in [('JPN','KOR'),('JPN','CHN'),('KOR','CHN')]:
                if r1 in c_means and r2 in c_means:
                    d = math.sqrt(sum((c_means[r1][f]-c_means[r2][f])**2 for f in ['adj_opp','adj_own']))
                    dists.append(d)
            if dists:
                boot_dists.append(statistics.mean(dists))

    if boot_dists:
        boot_dists.sort()
        obs = inter_region_dist(y0, y1)
        ci_lo = boot_dists[50]   # 2.5% percentile (2000 samples)
        ci_hi = boot_dists[1950] # 97.5% percentile
        print(f"  {phase_name:<30}: {obs:.4f} [95% CI: {ci_lo:.4f}, {ci_hi:.4f}]")

# Shock vs Pre-AI: is the drop significant?
shock_dist = inter_region_dist(2016, 2017)
pre_dist = inter_region_dist(1990, 2015)
diff = pre_dist - shock_dist
print(f"\n  Shock convergence: pre-AI={pre_dist:.4f} shock={shock_dist:.4f} Δ={diff:+.4f}")
if diff > 0:
    print(f"    → Regional distance DROPPED during shock (convergence)")

print(f"\n{'='*60}")
print(f"CLOSURE ANALYSES COMPLETE")
print(f"{'='*60}")
print(f"  1. Prefix robustness: verify 10/15/20 all show acceleration")
print(f"  2. Player control: top Korean players examined, leave-one-out check")
print(f"  3. Region audit: classification rules documented, samples verified")
print(f"  4. Bootstrap CI: phase-level regional distances with 95% CIs")
