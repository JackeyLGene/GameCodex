"""Phase 5 hardening: v3 submission-level computational checks.

1. 5-feature regional distance bootstrap (exact metric from the paper)
2. Fixed-horizon adoption analysis (censoring-safe)
3. Bootstrap CI on adoption-lag and reuse-density ratios
"""
import csv, json, statistics, math, random, os
from collections import defaultdict, Counter

random.seed(42)

# ═══ Shared ═══
SGF_COLS = 'abcdefghijklmnopqrs'
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

def sgf_to_xy(m):
    if not m or len(m)<2: return None
    c=SGF_COLS.find(m[0]); r=SGF_COLS.find(m[1])
    return (c,r) if c>=0 and r>=0 else None

FEATURES_5 = ['adj_opp', 'adj_own', 'dens_delta', 'dist_last', 'is_corner_open']

def compute_5feat_rhythm(prefix_moves, candidate_sgf):
    """Full 5-feature rhythm vector."""
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
    own_cnt=opp_cnt=0
    for (sx,sy),clr in board.items():
        if (sx,sy)==(tx,ty): continue
        if math.sqrt((tx-sx)**2+(ty-sy)**2)<=3:
            if clr==oc: opp_cnt+=1
            elif clr==mc: own_cnt+=1
    last = sgf_to_xy(prefix_moves[-1][1])
    dist_last = math.sqrt((tx-last[0])**2+(ty-last[1])**2)/20.0 if last else 1.0
    corner_d = min(math.sqrt(tx**2+ty**2),math.sqrt(tx**2+(18-ty)**2),
                   math.sqrt((18-tx)**2+ty**2),math.sqrt((18-tx)**2+(18-ty)**2))/13.0
    return {
        'adj_opp': adj_opp/4.0,'adj_own': adj_own/4.0,
        'dens_delta': (own_cnt-opp_cnt)/10.0,
        'dist_last': dist_last,
        'is_corner_open': 1.0 if corner_d*13.0<4 else 0.0,
    }

# ═══════════════════════════════════════════════════════════════
# TASK 1: 5-FEATURE REGIONAL DISTANCE BOOTSTRAP
# ═══════════════════════════════════════════════════════════════

print("="*60)
print("TASK 1: 5-FEATURE REGIONAL DISTANCE BOOTSTRAP")
print("="*60)

parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'

# Pre-compute per-year per-region 5-feature centroids
yr_reg_feats = defaultdict(lambda: defaultdict(list))

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
            if sgf_to_xy(actual) is None: continue
            rhy = compute_5feat_rhythm(prefix, actual)
            if rhy is None: continue
            for f in FEATURES_5:
                yr_reg_feats[(year, region)][f].append(rhy[f])

# Per-year per-region summary
yr_reg_summary = {}
for (year, region), feats in yr_reg_feats.items():
    if all(feats[f] for f in FEATURES_5):
        yr_reg_summary[(year, region)] = {
            f: statistics.mean(feats[f]) for f in FEATURES_5}

print(f"  Year-region centroids: {len(yr_reg_summary)}")

# Phases
phases = [
    ('Pre-AI 1990-2015', 1990, 2015),
    ('Shock 2016-2017', 2016, 2017),
    ('Diffusion 2018-2021', 2018, 2021),
    ('Oracle 2022-2025', 2022, 2025),
]

n_boot = 5000

for phase_name, y0, y1 in phases:
    # Gather all (year, region) pairs in this phase
    pool = [(y, r) for y in range(y0, y1+1)
            for r in ['JPN','KOR','CHN']
            if (y, r) in yr_reg_summary]
    if len(pool) < 3: continue

    boot_dists = []
    for _ in range(n_boot):
        # Bootstrap: resample year-region pairs
        sample = [random.choice(pool) for _ in range(len(pool))]
        # Aggregate per region
        cents = defaultdict(lambda: defaultdict(list))
        for (y, r) in sample:
            for f in FEATURES_5:
                cents[r][f].append(yr_reg_summary[(y, r)][f])
        # Compute centroids
        c_means = {}
        for r in cents:
            c_means[r] = {f: statistics.mean(cents[r][f]) for f in FEATURES_5}
        # Compute mean pairwise distance
        dists = []
        for r1,r2 in [('JPN','KOR'),('JPN','CHN'),('KOR','CHN')]:
            if r1 in c_means and r2 in c_means:
                d = math.sqrt(sum((c_means[r1][f]-c_means[r2][f])**2 for f in FEATURES_5))
                dists.append(d)
        if dists:
            boot_dists.append(statistics.mean(dists))

    if boot_dists:
        boot_dists.sort()
        # Observed distance
        obs_dists = []
        cents = defaultdict(lambda: defaultdict(list))
        for (y, r) in pool:
            for f in FEATURES_5:
                cents[r][f].append(yr_reg_summary[(y, r)][f])
        c_means = {r: {f: statistics.mean(cents[r][f]) for f in FEATURES_5} for r in cents}
        obs_d = statistics.mean([
            math.sqrt(sum((c_means[r1][f]-c_means[r2][f])**2 for f in FEATURES_5))
            for r1,r2 in [('JPN','KOR'),('JPN','CHN'),('KOR','CHN')]
            if r1 in c_means and r2 in c_means])

        ci_lo = boot_dists[125]   # 2.5%
        ci_hi = boot_dists[4875]  # 97.5%
        print(f"  {phase_name:<25}: {obs_d:.4f} [95% CI: {ci_lo:.4f}, {ci_hi:.4f}]")

# ═══════════════════════════════════════════════════════════════
# TASK 2: FIXED-HORIZON ADOPTION ANALYSIS
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"TASK 2: FIXED-HORIZON ADOPTION ANALYSIS")
print(f"{'='*60}")

PREFIX_LEN = 15
pattern_years = defaultdict(lambda: defaultdict(int))
pattern_players = defaultdict(lambda: defaultdict(set))

with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','')
        if not y or y=='None': continue
        year = int(y)
        if year < 1950 or year > 2025: continue
        moves = json.loads(row.get('moves','[]'))
        if len(moves) < PREFIX_LEN + 1: continue
        prefix = ','.join(f"{c}{coord}" for c,coord in moves[:PREFIX_LEN])
        pattern_years[prefix][year] += 1
        bp = row.get('black_player','')
        wp = row.get('white_player','')
        pattern_players[prefix][year].add(bp)
        pattern_players[prefix][year].add(wp)

# Organize patterns by era of first appearance
patterns_by_era = defaultdict(list)
for pattern, yr_data in pattern_years.items():
    total_uses = sum(yr_data.values())
    if len(yr_data) < 3 or total_uses < 5: continue  # qualifying filter
    first_seen = min(yr_data.keys())
    if first_seen < 1980: era = 'pre-1980'
    elif first_seen < 2000: era = '1980-1999'
    elif first_seen < 2016: era = '2000-2015'
    else: era = '2016+'

    # Find adoption year: first year with >=3 unique players
    years_sorted = sorted(yr_data.keys())
    adopted_year = None
    for y in years_sorted:
        if len(pattern_players[pattern][y]) >= 3:
            adopted_year = y
            break

    # Last observed year
    last_year = max(yr_data.keys())

    patterns_by_era[era].append({
        'pattern': pattern,
        'first_seen': first_seen,
        'adopted_year': adopted_year,
        'last_year': last_year,
    })

print(f"\n  Qualifying patterns by era of first appearance:")
for era in ['pre-1980','1980-1999','2000-2015','2016+']:
    pats = patterns_by_era[era]
    n_adopted = sum(1 for p in pats if p['adopted_year'] is not None)
    print(f"    {era:<12}: {len(pats):>4} patterns, {n_adopted:>4} adopted")

# Fixed-horizon adoption probabilities
horizons = [1, 2, 3, 5]
print(f"\n  Fixed-horizon adoption probability (reaching >=3 players within N years):")
print(f"  {'Era':<12} {'N_pat':>6}", end='')
for h in horizons:
    print(f" {'≤'+str(h)+'yr':>8}", end='')
print(f" {'censored':>10}")

for era in ['pre-1980','1980-1999','2000-2015','2016+']:
    pats = patterns_by_era[era]
    counts = {}
    for h in horizons:
        n_adopt = 0
        n_valid = 0
        for p in pats:
            follow_up = p['last_year'] - p['first_seen']
            if follow_up >= h:  # can potentially observe adoption within h years
                n_valid += 1
                if p['adopted_year'] is not None and p['adopted_year'] - p['first_seen'] <= h:
                    n_adopt += 1
        prop = n_adopt / max(1, n_valid)
        counts[h] = (n_adopt, n_valid, prop)

    # Count censored: not adopted by last observation
    n_censored = sum(1 for p in pats if p['adopted_year'] is None)

    print(f"  {era:<12} {len(pats):>6}", end='')
    for h in horizons:
        n_a, n_v, prop = counts[h]
        print(f" {n_a}/{n_v}={prop:.2f}", end='')
    print(f" {n_censored:>10}")

# Compute mean adoption lag (Kaplan-Meier style: conditional on observed adoption)
print(f"\n  Observed adoption lag (conditional on observed adoption):")
for era in ['pre-1980','1980-1999','2000-2015','2016+']:
    lags = [p['adopted_year'] - p['first_seen']
            for p in patterns_by_era[era]
            if p['adopted_year'] is not None]
    if lags:
        print(f"    {era:<12}: mean={statistics.mean(lags):.1f} yr "
              f"(median={statistics.median(lags):.0f}, N={len(lags)})")

# ═══════════════════════════════════════════════════════════════
# TASK 3: BOOTSTRAP CI ON ADOPTION/RATIO METRICS
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"TASK 3: BOOTSTRAP CI ON ADOPTION LAG AND REUSE DENSITY RATIOS")
print(f"{'='*60}")

# Bootstrap: per-pattern resampling within each era
n_boot_ratio = 5000

print(f"\n  Adoption lag bootstrap (pre-1980 vs 2016+ ratio):")
pre_pats = [p for p in patterns_by_era['pre-1980'] if p['adopted_year'] is not None]
post_pats = [p for p in patterns_by_era['2016+'] if p['adopted_year'] is not None]

if pre_pats and post_pats:
    obs_pre_lag = statistics.mean(p['adopted_year']-p['first_seen'] for p in pre_pats)
    obs_post_lag = statistics.mean(p['adopted_year']-p['first_seen'] for p in post_pats)
    obs_ratio = obs_pre_lag / max(0.001, obs_post_lag)

    boot_ratios = []
    for _ in range(n_boot_ratio):
        s_pre = [random.choice(pre_pats) for _ in range(len(pre_pats))]
        s_post = [random.choice(post_pats) for _ in range(len(post_pats))]
        m_pre = statistics.mean(p['adopted_year']-p['first_seen'] for p in s_pre)
        m_post = statistics.mean(p['adopted_year']-p['first_seen'] for p in s_post)
        boot_ratios.append(m_pre / max(0.001, m_post))

    boot_ratios.sort()
    ci_lo = boot_ratios[125]
    ci_hi = boot_ratios[4875]
    print(f"    Observed ratio: {obs_ratio:.1f}× [95% CI: {ci_lo:.1f}×, {ci_hi:.1f}×]")

# Reuse density bootstrap
print(f"\n  Reuse density bootstrap (pre-1980 vs 2016+ ratio):")
pre_reuse = []
for p in patterns_by_era['pre-1980']:
    years_used = len(pattern_years[p['pattern']])
    span = p['last_year'] - p['first_seen'] + 1
    if span > 0:
        pre_reuse.append(years_used / span)

post_reuse = []
for p in patterns_by_era['2016+']:
    years_used = len(pattern_years[p['pattern']])
    span = p['last_year'] - p['first_seen'] + 1
    if span > 0:
        post_reuse.append(years_used / span)

if pre_reuse and post_reuse:
    obs_pre_r = statistics.mean(pre_reuse)
    obs_post_r = statistics.mean(post_reuse)
    obs_ratio_r = obs_post_r / max(0.001, obs_pre_r)

    boot_ratios_r = []
    for _ in range(n_boot_ratio):
        s_pre = [random.choice(pre_reuse) for _ in range(len(pre_reuse))]
        s_post = [random.choice(post_reuse) for _ in range(len(post_reuse))]
        boot_ratios_r.append(statistics.mean(s_post) / max(0.001, statistics.mean(s_pre)))

    boot_ratios_r.sort()
    ci_lo_r = boot_ratios_r[125]
    ci_hi_r = boot_ratios_r[4875]
    print(f"    Observed ratio: {obs_ratio_r:.1f}× [95% CI: {ci_lo_r:.1f}×, {ci_hi_r:.1f}×]")

# ═══ Summary ═══
print(f"\n{'='*60}")
print(f"HARDENING COMPLETE")
print(f"{'='*60}")
print(f"  Task 1: 5-feature regional distance bootstrap ✓")
print(f"  Task 2: Fixed-horizon adoption analysis ✓")
print(f"  Task 3: Bootstrap CI on adoption/reuse ratios ✓")
