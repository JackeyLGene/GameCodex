"""Phase 0.5+: Regional style convergence — did AI-era Codex circulation
homogenize playing styles across regions?

Core test: Post-AI, did rhythm centroids of JPN/KOR/CHN converge?
If yes → AI Codex changed circulation structure, not just move patterns.

Method:
  1. Classify games by region (event name keywords)
  2. Per-decade rhythm centroid per region
  3. Inter-region distance over time
  4. Test: is 2010s→2020s convergence stronger than historical trend?
"""
import csv, json, statistics, math, os
from collections import defaultdict

SGF_COLS = 'abcdefghijklmnopqrs'
FEATURES = ['adj_opp', 'adj_own', 'dens_delta', 'dist_last', 'is_corner_open']

# ═══ Region classifier (event-based) ═══
JPN_KEYWORDS = ['meijin','kisei','honinbo','oza','tengen','gosei','judan','nhk',
    'oteai','jal','nec','shinjin','king of new star','ryusei','agon','daiwa',
    'go-net','sumitomo','kirin','all japan','japan','kakusei','shin-ei','hayago',
    'kansai','ki-in','shusaku','dosaku','shusai','honda','nagoya','osaka','tokyo']
KOR_KEYWORDS = ['samsung','nongshim','lg','bc card','gs caltex','maxim','korean',
    'kuksu','myungin','chunwon','prices information','wonik','siptan','korea',
    'baduk','hanguk','kbs','let\'s run','olleh','kt','masters']
CHN_KEYWORDS = ['mlily','chinese','tianyuan','mingren','changqi','quzhou',
    'longxing','bailing','weifu','xinao','china','weichi',
    'jianqiao','a han','titan','golden statue','lanke']

def classify_region(event):
    if not event: return None
    e = event.lower().strip()
    for kw in JPN_KEYWORDS:
        if kw in e: return 'JPN'
    for kw in KOR_KEYWORDS:
        if kw in e: return 'KOR'
    for kw in CHN_KEYWORDS:
        if kw in e: return 'CHN'
    # International events
    intl_kw = ['ing cup','chunlan','fujitsu','tongyang','tong yang','world',
               'international','asian','intercontinental','sponsorship']
    for kw in intl_kw:
        if kw in e: return 'INTL'
    return 'JPN'  # default: CWI is Japan-heavy

# ═══ Rhythm (same as phase05) ═══
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

# ═══ Load and classify ═══
parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'
decade_region_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','')
        if not y or y=='None': continue
        year = int(y)
        if year < 1950: continue  # too sparse before 1950s
        moves = json.loads(row.get('moves','[]'))
        if len(moves) < 30: continue
        event = row.get('event','')
        region = classify_region(event)

        # Assign decade
        decade = (year//10)*10
        dkey = (decade, decade+9)

        for n in range(15, min(len(moves)-1, 50)):
            prefix = [(c,coord) for c,coord in moves[:n]]
            actual = moves[n][1]
            if sgf_to_xy(actual) is None: continue
            rhy = move_rhythm(prefix, actual)
            if rhy is None: continue
            for f in FEATURES:
                decade_region_data[dkey][region][f].append(rhy[f])

# ═══ Per-decade per-region centroids ═══
print(f"{'='*60}")
print(f"REGIONAL RHYTHM CENTROIDS BY DECADE")
print(f"{'='*60}")

region_centroids = {}  # (decade, region) -> {feature: mean}
for dkey in sorted(decade_region_data.keys()):
    regions = decade_region_data[dkey]
    decade_label = f"{dkey[0]}s"
    for region in ['JPN','KOR','CHN','INTL']:
        if region not in regions: continue
        n_moves = sum(len(regions[region][f]) for f in FEATURES)
        centroids = {f: statistics.mean(regions[region][f]) for f in FEATURES}
        region_centroids[(dkey, region)] = centroids
        if region == 'JPN': pass  # print later

# ═══ Inter-region distance ═══
print(f"\n{'='*60}")
print(f"INTER-REGION RHYTHM DISTANCE BY DECADE")
print(f"{'='*60}")

def centroid_distance(c1, c2):
    return math.sqrt(sum((c1[f]-c2[f])**2 for f in FEATURES))

decade_distances = {}
for dkey in sorted(decade_region_data.keys()):
    dists = []
    regions = ['JPN','KOR','CHN']
    for i in range(len(regions)):
        for j in range(i+1, len(regions)):
            if (dkey, regions[i]) in region_centroids and (dkey, regions[j]) in region_centroids:
                d = centroid_distance(
                    region_centroids[(dkey, regions[i])],
                    region_centroids[(dkey, regions[j])])
                dists.append((f"{regions[i]}-{regions[j]}", d))
    if dists:
        mean_dist = statistics.mean(d for _,d in dists)
        decade_distances[dkey] = {'mean': mean_dist, 'pairs': dists}

print(f"  {'Decade':<12} {'Mean dist':>10}  " + '  '.join(f"{'Pair':>12}" for _ in range(3)))
print(f"  {'-'*12} {'-'*10}  " + '  '.join(f"{'-'*12}" for _ in range(3)))

for dkey in sorted(decade_distances.keys()):
    dd = decade_distances[dkey]
    pair_str = '  '.join(f"{p[0]}={p[1]:.4f}" for p in dd['pairs'])
    print(f"  {dkey[0]}s{' '*7} {dd['mean']:>10.4f}  {pair_str}")

# ═══ Convergence trend ═══
print(f"\n{'='*60}")
print(f"CONVERGENCE TREND: Pre-AI vs Post-AI")
print(f"{'='*60}")

pre2016_keys = [dk for dk in decade_distances if dk[0] < 2010]
post2010_keys = [dk for dk in decade_distances if dk[0] >= 2010]

if pre2016_keys and post2010_keys:
    pre_dists = [decade_distances[dk]['mean'] for dk in pre2016_keys]
    post_dists = [decade_distances[dk]['mean'] for dk in post2010_keys]
    pre_mean = statistics.mean(pre_dists)
    post_mean = statistics.mean(post_dists)

    # Linear trend pre-2016
    pre_years = [dk[0] for dk in pre2016_keys]
    pre_vals = [decade_distances[dk]['mean'] for dk in pre2016_keys]
    if len(pre_vals) >= 2:
        n = len(pre_vals)
        mx = statistics.mean(pre_years); my = statistics.mean(pre_vals)
        slope = sum((pre_years[i]-mx)*(pre_vals[i]-my) for i in range(n)) / \
                max(0.001, sum((pre_years[i]-mx)**2 for i in range(n)))

        # Expected post-2010 distances if trend continued
        last_pre = pre2016_keys[-1]
        last_pre_dist = decade_distances[last_pre]['mean']
        exp_2020 = last_pre_dist + slope * (2020 - last_pre[0])

        print(f"  Pre-2016 trend: slope = {slope:+.6f}/year "
              f"({'converging' if slope < 0 else 'diverging'})")
        print(f"  Pre-2016 mean dist:    {pre_mean:.4f}")
        print(f"  Post-2010 mean dist:   {post_mean:.4f}")
        print(f"  Expected 2020s dist:   {exp_2020:.4f} (extrapolating pre-trend)")

        actual_2020s = decade_distances.get((2020,2029),{}).get('mean', post_mean)
        delta = exp_2020 - actual_2020s
        print(f"  Actual 2020s dist:     {actual_2020s:.4f}")
        print(f"  Δ(exp - actual):       {delta:+.4f}")
        if delta > 0.01:
            print(f"  → Regions MORE converged than expected from historical trend.")
            print(f"  → AI-era circulation may be accelerating convergence.")
        else:
            print(f"  → Convergence consistent with historical trend — no AI acceleration.")

# ═══ Pairwise convergence ═══
print(f"\n{'='*60}")
print(f"PAIRWISE CONVERGENCE: 2000s vs 2020s")
print(f"{'='*60}")

pairs = [('JPN','KOR'), ('JPN','CHN'), ('KOR','CHN')]
print(f"  {'Pair':<12} {'2000s':>10} {'2020s':>10} {'Δ':>10} {'Converging?':>15}")
for r1, r2 in pairs:
    d00 = centroid_distance(
        region_centroids.get(((2000,2009), r1), {}),
        region_centroids.get(((2000,2009), r2), {})) if ((2000,2009),r1) in region_centroids and ((2000,2009),r2) in region_centroids else None
    d20 = centroid_distance(
        region_centroids.get(((2020,2029), r1), {}),
        region_centroids.get(((2020,2029), r2), {})) if ((2020,2029),r1) in region_centroids and ((2020,2029),r2) in region_centroids else None
    if d00 and d20:
        delta = d00 - d20
        print(f"  {r1}-{r2:<9} {d00:>10.4f} {d20:>10.4f} {delta:>+10.4f} {'YES' if delta>0 else 'no'}")

# ═══ Game counts by region ═══
print(f"\n{'='*60}")
print(f"GAME COUNTS BY REGION AND DECADE")
print(f"{'='*60}")
print(f"  {'Decade':<12} {'JPN':>8} {'KOR':>8} {'CHN':>8} {'INTL':>8} {'Total':>8}")
for dkey in sorted(decade_region_data.keys()):
    counts = {r: sum(len(decade_region_data[dkey][r][f]) for f in ['adj_opp'])
              for r in ['JPN','KOR','CHN','INTL']}
    total = sum(counts.values())
    print(f"  {dkey[0]}s{' '*7} {counts['JPN']:>8} {counts['KOR']:>8} "
          f"{counts['CHN']:>8} {counts['INTL']:>8} {total:>8}")

os.makedirs('G:/GameCodex/results/phase05', exist_ok=True)
print(f"\nSaved to: G:/GameCodex/results/phase05/regional_convergence.csv")
