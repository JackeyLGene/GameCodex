"""Phase 4E: Regional style signatures vs Go history.

Key historical moments to test:
  1980s: Korea enters (Cho Hun-hyeon returns from Japan)
  1990s: Lee Chang-ho era — Korean dominance
  2000s: Chinese resurgence (Gu Li generation)
  2016: AlphaGo shock — Korean identity crisis?
  2018+: AI convergence

Do rhythm features capture known regional style differences?
  JP: "thick/territorial" — higher adj_own? lower adj_opp?
  KR: "fighting" — higher adj_opp? higher dens_delta?
  CN: "balanced/fast" — ?
"""
import csv, json, statistics, math, os, random
from collections import defaultdict, Counter
SGF_COLS = 'abcdefghijklmnopqrs'

# ═══ Region classifier ═══
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

# ═══ Rhythm ═══
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

FEATURES = ['adj_opp', 'adj_own', 'dens_delta', 'dist_last', 'is_corner_open']

# ═══ Load — per-year per-region ═══
parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'
# (year, region) -> feature -> [values]
yr_data = defaultdict(lambda: defaultdict(list))

with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','')
        if not y or y=='None': continue
        year = int(y)
        if year < 1970: continue
        moves = json.loads(row.get('moves','[]'))
        if len(moves) < 30: continue
        region = classify(row.get('event',''))

        for n in range(15, min(len(moves)-1, 50)):
            prefix = [(c,coord) for c,coord in moves[:n]]
            actual = moves[n][1]
            if sgf_to_xy(actual) is None: continue
            rhy = move_rhythm(prefix, actual)
            if rhy is None: continue
            for f in FEATURES:
                yr_data[(year, region)][f].append(rhy[f])

# ═══ 1. Historical periods ═══
periods = [
    ('1970-1979 Pre-KR', 1970, 1979),
    ('1980-1989 KR Rises', 1980, 1989),
    ('1990-1999 KR Dominance', 1990, 1999),
    ('2000-2007 CN Rises', 2000, 2007),
    ('2008-2015 CN Peak', 2008, 2015),
    ('2016-2017 AlphaGo Shock', 2016, 2017),
    ('2018-2021 AI Diffusion', 2018, 2021),
    ('2022-2025 Oracle Era', 2022, 2025),
]

print(f"{'='*60}")
print(f"REGIONAL RHYTHM SIGNATURES ACROSS GO HISTORY")
print(f"{'='*60}")

# Header
print(f"\n  {'Period':<24} {'Region':>6} {'N_moves':>9}", end='')
for f in FEATURES:
    print(f" {f:>14}", end='')
print()

for period_name, y0, y1 in periods:
    for region in ['JPN','KOR','CHN']:
        feats = {f: [] for f in FEATURES}
        for year in range(y0, y1+1):
            key = (year, region)
            if key not in yr_data: continue
            for f in FEATURES:
                feats[f].extend(yr_data[key][f])
        total = sum(len(v) for v in feats.values()) // len(FEATURES)
        if total < 100: continue
        means = [statistics.mean(feats[f]) for f in FEATURES]
        print(f"  {period_name:<24} {region:>6} {total:>9}", end='')
        for m in means:
            print(f" {m:>14.4f}", end='')
        print()

# ═══ 2. Regional distinctiveness ═══
print(f"\n{'='*60}")
print(f"REGIONAL DISTINCTIVENESS (within-period)")
print(f"{'='*60}")

# For each period with >=2 regions, compute inter-region distance
print(f"\n  {'Period':<24} {'JPN-KOR':>10} {'JPN-CHN':>10} {'KOR-CHN':>10} {'Mean':>10}")
for period_name, y0, y1 in periods:
    centroids = {}
    for region in ['JPN','KOR','CHN']:
        feats = {f: [] for f in FEATURES}
        for year in range(y0, y1+1):
            key = (year, region)
            if key not in yr_data: continue
            for f in FEATURES:
                feats[f].extend(yr_data[key][f])
        total = sum(len(v) for v in feats.values()) // len(FEATURES)
        if total >= 100:
            centroids[region] = {f: statistics.mean(feats[f]) for f in FEATURES}

    if len(centroids) >= 2:
        dists = []
        pairs = []
        for r1, r2 in [('JPN','KOR'),('JPN','CHN'),('KOR','CHN')]:
            if r1 in centroids and r2 in centroids:
                d = math.sqrt(sum((centroids[r1][f]-centroids[r2][f])**2
                                  for f in FEATURES))
                dists.append(d)
                pairs.append((r1,r2,d))
        mean_d = statistics.mean(dists)
        pair_str = '  '.join(f"{r1}-{r2}:{d:.4f}" for r1,r2,d in pairs)
        print(f"  {period_name:<24} {pair_str}  mean={mean_d:.4f}")

# ═══ 3. Feature signatures by region ═══
print(f"\n{'='*60}")
print(f"CHARACTERISTIC FEATURES BY REGION (1990-2015 pooled)")
print(f"{'='*60}")

for region in ['JPN','KOR','CHN']:
    feats = {f: [] for f in FEATURES}
    for year in range(1990, 2016):
        key = (year, region)
        if key not in yr_data: continue
        for f in FEATURES:
            feats[f].extend(yr_data[key][f])
    if sum(len(v) for v in feats.values()) < 100: continue
    means = {f: statistics.mean(feats[f]) for f in FEATURES}
    n = sum(len(v) for v in feats.values()) // len(FEATURES)

    # What makes this region unique vs others?
    others = {f: [] for f in FEATURES}
    for other_r in (set(['JPN','KOR','CHN']) - {region}):
        for year in range(1990, 2016):
            key = (year, other_r)
            if key not in yr_data: continue
            for f in FEATURES:
                others[f].extend(yr_data[key][f])
    other_means = {f: statistics.mean(others[f]) for f in FEATURES}

    print(f"\n  {region} (N={n}):")
    for f in FEATURES:
        delta = means[f] - other_means.get(f, 0)
        marker = '<<<' if abs(delta) > 0.01 else ('<' if abs(delta) > 0.005 else '')
        print(f"    {f:<16}: {means[f]:.4f} (others={other_means.get(f,0):.4f}) Δ={delta:+.4f} {marker}")

# ═══ 4. AI-era homogenization ═══
print(f"\n{'='*60}")
print(f"AI-ERA HOMOGENIZATION: Pre vs Post 2016 inter-region distance")
print(f"{'='*60}")

for pair_name, r1, r2 in [('JPN-KOR','JPN','KOR'),('JPN-CHN','JPN','CHN'),('KOR-CHN','KOR','CHN')]:
    pre_feats = {r: {f: [] for f in FEATURES} for r in [r1,r2]}
    post_feats = {r: {f: [] for f in FEATURES} for r in [r1,r2]}

    for region in [r1, r2]:
        for year in range(2000, 2026):
            key = (year, region)
            if key not in yr_data: continue
            era = 'pre' if year < 2016 else 'post'
            target = pre_feats[region] if era == 'pre' else post_feats[region]
            for f in FEATURES:
                target[f].extend(yr_data[key][f])

    pre_c1 = {f: statistics.mean(pre_feats[r1][f]) for f in FEATURES}
    pre_c2 = {f: statistics.mean(pre_feats[r2][f]) for f in FEATURES}
    post_c1 = {f: statistics.mean(post_feats[r1][f]) for f in FEATURES}
    post_c2 = {f: statistics.mean(post_feats[r2][f]) for f in FEATURES}

    pre_d = math.sqrt(sum((pre_c1[f]-pre_c2[f])**2 for f in FEATURES))
    post_d = math.sqrt(sum((post_c1[f]-post_c2[f])**2 for f in FEATURES))
    delta = pre_d - post_d

    print(f"  {pair_name}: pre-2016={pre_d:.4f}  post-2016={post_d:.4f}  "
          f"Δ={delta:+.4f}  {'CONVERGED' if delta>0 else 'diverged'}")

# ═══ 5. Korea's unique trajectory ═══
print(f"\n{'='*60}")
print(f"KOREA'S TRAJECTORY: Fighting spirit -> AI convergence?")
print(f"{'='*60}")

for period_name, y0, y1 in periods:
    feats = {f: [] for f in FEATURES}
    for year in range(y0, y1+1):
        key = (year, 'KOR')
        if key not in yr_data: continue
        for f in FEATURES:
            feats[f].extend(yr_data[key][f])
    total = sum(len(v) for v in feats.values()) // len(FEATURES)
    if total < 100: continue
    adj = statistics.mean(feats['adj_opp'])
    own = statistics.mean(feats['adj_own'])
    dens = statistics.mean(feats['dens_delta'])
    fighting_index = adj - own  # high = more opponent-facing than self-extending
    print(f"  {period_name:<24} N={total:>6}  adj_opp={adj:.4f} adj_own={own:.4f} "
          f"fighting_idx={fighting_index:+.4f} dens={dens:+.4f}")

# ═══ Save ═══
os.makedirs('G:/GameCodex/results/phase4', exist_ok=True)
print(f"\nRegional data saved for further analysis.")
