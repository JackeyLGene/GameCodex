"""Phase 4C: 1910s→1920s Drift Decomposition.

The largest decade drift in Go history (|drift|=0.034, 2.6× AI-era).
Is it a real playing-style shift or an archive transition?

Decompose into:
  1. Composition effect: new players, new events, sample size change
  2. Move effect: actual rhythm change within same player/event subsets
  3. Opening vs midgame: was drift concentrated in opening moves?
"""
import csv, json, statistics, math, random
from collections import defaultdict, Counter

random.seed(42)
SGF_COLS = 'abcdefghijklmnopqrs'

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

# ═══ Load 1910s and 1920s ═══
parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'
decade_data = {1910: [], 1920: []}

with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','')
        if not y or y=='None': continue
        year = int(y)
        if 1910 <= year <= 1929:
            moves = json.loads(row.get('moves','[]'))
            if len(moves) < 30: continue
            event = row.get('event','')
            black = row.get('black_player','')
            white = row.get('white_player','')
            decade = 1910 if year < 1920 else 1920
            decade_data[decade].append({
                'year': year, 'event': event,
                'black': black, 'white': white,
                'moves': moves,
            })

print(f"1910s: {len(decade_data[1910])} games")
print(f"1920s: {len(decade_data[1920])} games")

# ═══ 1. Composition analysis ═══
print(f"\n{'='*60}")
print(f"1. COMPOSITION CHANGE: 1910s -> 1920s")
print(f"{'='*60}")

# Compute player sets first
p1910 = set()
for g in decade_data[1910]: p1910.add(g['black']); p1910.add(g['white'])
p1920 = set()
for g in decade_data[1920]: p1920.add(g['black']); p1920.add(g['white'])
overlap = p1910 & p1920

for dec, label in [(1910, '1910s'), (1920, '1920s')]:
    games = decade_data[dec]
    players = set()
    for g in games: players.add(g['black']); players.add(g['white'])
    events = Counter(g['event'] for g in games)
    print(f"\n  {label}:")
    print(f"    Games: {len(games)}, Players: {len(players)}")
    print(f"    Top events: {events.most_common(5)}")
    other_set = p1920 if dec == 1910 else p1910
    print(f"    Player overlap with other decade: "
          f"{len(players & other_set)} / {len(players)}")

print(f"\n  Player overlap 1910s∩1920s: {len(overlap)} | "
      f"1910s={len(overlap)}/{len(p1910)}, 1920s={len(overlap)}/{len(p1920)}")
print(f"\n  Player overlap 1910s∩1920s: {len(overlap)}/{len(p1910)} (1910s) "
      f"{len(overlap)}/{len(p1920)} (1920s)")

# ═══ 2. Rhythm centroids ═══
print(f"\n{'='*60}")
print(f"2. RHYTHM CENTROIDS: Full, Overlap-players, Non-overlap")
print(f"{'='*60}")

# Also need all_players_other for the previous section
# (already computed)

def compute_centroid(games):
    feats = {f: [] for f in FEATURES}
    for g in games:
        moves = g['moves']
        for n in range(15, min(len(moves)-1, 50)):
            prefix = [(c,coord) for c,coord in moves[:n]]
            actual = moves[n][1]
            if sgf_to_xy(actual) is None: continue
            rhy = move_rhythm(prefix, actual)
            if rhy is None: continue
            for f in FEATURES:
                feats[f].append(rhy[f])
    return {f: statistics.mean(vals) for f, vals in feats.items() if vals}, \
           sum(len(vals) for vals in feats.values())//len(FEATURES)

# Full
c1910_full, n1910 = compute_centroid(decade_data[1910])
c1920_full, n1920 = compute_centroid(decade_data[1920])
drift_full = math.sqrt(sum((c1910_full[f]-c1920_full[f])**2 for f in FEATURES))

# Overlap players only
g1910_ov = [g for g in decade_data[1910]
            if g['black'] in overlap or g['white'] in overlap]
g1920_ov = [g for g in decade_data[1920]
            if g['black'] in overlap or g['white'] in overlap]
c1910_ov, _ = compute_centroid(g1910_ov)
c1920_ov, _ = compute_centroid(g1920_ov)
drift_ov = math.sqrt(sum((c1910_ov[f]-c1920_ov[f])**2 for f in FEATURES))

# Non-overlap players only
g1910_no = [g for g in decade_data[1910]
             if g['black'] not in overlap and g['white'] not in overlap]
g1920_no = [g for g in decade_data[1920]
             if g['black'] not in overlap and g['white'] not in overlap]
c1910_no, _ = compute_centroid(g1910_no)
c1920_no, _ = compute_centroid(g1920_no)
drift_no = math.sqrt(sum((c1910_no[f]-c1920_no[f])**2 for f in FEATURES)) if c1910_no and c1920_no else 0

print(f"\n  |drift| Full:              {drift_full:.4f}")
print(f"  |drift| Overlap players:    {drift_ov:.4f} (N={len(g1910_ov)}/{len(g1920_ov)})")
print(f"  |drift| Non-overlap:       {drift_no:.4f} (N={len(g1910_no)}/{len(g1920_no)})")

print(f"\n  Feature breakdown:")
print(f"  {'Feature':<16} {'1910s full':>12} {'1920s full':>12} {'1910s ov':>12} {'1920s ov':>12}")
for f in FEATURES:
    v1910f = c1910_full.get(f, 0)
    v1920f = c1920_full.get(f, 0)
    v1910o = c1910_ov.get(f, 0)
    v1920o = c1920_ov.get(f, 0)
    print(f"  {f:<16} {v1910f:>12.4f} {v1920f:>12.4f} {v1910o:>12.4f} {v1920o:>12.4f}")

# ═══ 3. Opening vs midgame split ═══
print(f"\n{'='*60}")
print(f"3. OPENING (moves 15-25) vs MIDGAME (moves 30-50)")
print(f"{'='*60}")

for label, games in [('1910s', decade_data[1910]), ('1920s', decade_data[1920])]:
    open_feats = {f: [] for f in FEATURES}
    mid_feats = {f: [] for f in FEATURES}
    for g in games:
        moves = g['moves']
        for n in range(15, min(25, len(moves)-1)):
            prefix = [(c,coord) for c,coord in moves[:n]]
            actual = moves[n][1]
            if sgf_to_xy(actual) is None: continue
            rhy = move_rhythm(prefix, actual)
            if rhy is None: continue
            for f in FEATURES: open_feats[f].append(rhy[f])
        for n in range(30, min(50, len(moves)-1)):
            prefix = [(c,coord) for c,coord in moves[:n]]
            actual = moves[n][1]
            if sgf_to_xy(actual) is None: continue
            rhy = move_rhythm(prefix, actual)
            if rhy is None: continue
            for f in FEATURES: mid_feats[f].append(rhy[f])

    print(f"\n  {label}:")
    for f in FEATURES:
        ov = statistics.mean(open_feats[f]) if open_feats[f] else 0
        mv = statistics.mean(mid_feats[f]) if mid_feats[f] else 0
        delta = mv - ov
        print(f"    {f:<16} opening={ov:+.4f}  midgame={mv:+.4f}  Δ={delta:+.4f}")

# ═══ 4. Verdict ═══
print(f"\n{'='*60}")
print(f"VERDICT: 1910s -> 1920s DRIFT DECOMPOSITION")
print(f"{'='*60}")

# Compare drift magnitudes
print(f"\n  |drift| Full:           {drift_full:.4f}")
if drift_ov > 0:
    print(f"  |drift| Overlap only:   {drift_ov:.4f}")
    pct_ov = drift_ov / max(0.001, drift_full) * 100
    print(f"  Overlap % of full:     {pct_ov:.0f}%")
if drift_no > 0:
    print(f"  |drift| Non-overlap:    {drift_no:.4f}")

print(f"\n  Reference: AI-era drift (2010s->2020s): 0.0130 (Phase 0.5)")
print(f"  Reference: Pre-2016 mean decade drift:   0.0146")

if drift_ov > 0.02:
    print(f"\n  -> Overlap players STILL show large drift -> real style change")
    print(f"  -> Oteai institution did more than just change who played")
else:
    print(f"\n  -> Most of the drift is from player turnover -> archive transition")
    print(f"  -> Oteai primarily changed who was recorded, not how they played")
