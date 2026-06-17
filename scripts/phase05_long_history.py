"""Phase 0.5: Long-History Baseline — decade-level drift envelope.

Core question: Are AI-era shifts (Phase 1-3) beyond the historical drift
envelope, or within normal century-scale Codex evolution?

Method:
  1. Decade-level SHP rhythm centroid
  2. Decade-to-decade drift vector
  3. Pre-2016 95% envelope
  4. E2/E3 position relative to envelope
  5. Codex Δ by decade
  6. Novelty rate + survival half-life by decade

No KataGo needed — purely from SGF move data.
"""
import csv, json, statistics, math, os
from collections import defaultdict, Counter

# ═══ Constants ═══
SGF_COLS = 'abcdefghijklmnopqrs'
FEATURES = ['adj_opp', 'adj_own', 'dens_delta', 'dist_last', 'is_corner_open']
DECADES = [(1600,1699),(1700,1799),(1800,1849),(1850,1899),
           (1900,1909),(1910,1919),(1920,1929),(1930,1939),
           (1940,1949),(1950,1959),(1960,1969),(1970,1979),
           (1980,1989),(1990,1999),(2000,2009),(2010,2019),
           (2020,2026)]

# ═══ Rhythm features (same as Phase 1/2) ═══
def sgf_to_xy(m):
    if not m or len(m)<2: return None
    c=SGF_COLS.find(m[0]); r=SGF_COLS.find(m[1])
    return (c,r) if c>=0 and r>=0 else None

def move_rhythm(prefix_moves, candidate_sgf):
    """Compute 5-dim rhythm vector for a candidate move."""
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
    if last:
        dist_last = math.sqrt((tx-last[0])**2+(ty-last[1])**2)/20.0
    else:
        dist_last = 1.0
    corner_d = min(math.sqrt(tx**2+ty**2),math.sqrt(tx**2+(18-ty)**2),
                   math.sqrt((18-tx)**2+ty**2),math.sqrt((18-tx)**2+(18-ty)**2))/13.0

    return {
        'adj_opp': adj_opp/4.0,'adj_own': adj_own/4.0,
        'dens_delta': (own_cnt-opp_cnt)/10.0,
        'dist_last': dist_last,
        'is_corner_open': 1.0 if corner_d*13.0<4 else 0.0,
    }

# ═══ Load and group by decade ═══
parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'
decade_games = defaultdict(list)

with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','')
        if not y or y=='None': continue
        year = int(y)
        moves = json.loads(row.get('moves','[]'))
        if len(moves) < 30: continue

        for y0,y1 in DECADES:
            if y0 <= year <= y1:
                decade_games[(y0,y1)].append(moves)
                break

print(f"Loaded games across {len(decade_games)} decades")

# ═══ Per-decade SHP ═══
decade_stats = {}
for (y0,y1), games in sorted(decade_games.items()):
    if len(games) < 20: continue  # minimum sample

    n_games = len(games)
    label = f"{y0}s" if y1-y0==9 else f"{y0}-{y1}"

    # Rhythm features for all moves
    feat_vals = {f: [] for f in FEATURES}
    cross_harms = []
    novelty_hashes = set()
    total_moves = 0

    for moves in games:
        for n in range(15, min(len(moves)-1, 50)):
            prefix = [(c,coord) for c,coord in moves[:n]]
            actual = moves[n][1]
            if sgf_to_xy(actual) is None: continue
            rhy = move_rhythm(prefix, actual)
            if rhy is None: continue
            for f in FEATURES:
                feat_vals[f].append(rhy[f])
            # Cross-harm: sum of absolute rhythm values (simplified)
            cross_harms.append(sum(abs(rhy[f]) for f in FEATURES))
            # Novelty: position prefix hash
            pos_key = ','.join(f"{c}{coord}" for c,coord in moves[:n])
            novelty_hashes.add(pos_key)
            total_moves += 1

    # Compute statistics
    centroids = {}
    for f in FEATURES:
        vals = feat_vals[f]
        centroids[f] = (statistics.mean(vals), statistics.stdev(vals))

    decade_stats[(y0,y1)] = {
        'label': label, 'y0': y0, 'n_games': n_games,
        'n_moves': total_moves,
        'centroids': {f: centroids[f][0] for f in FEATURES},
        'centroid_sd': {f: centroids[f][1] for f in FEATURES},
        'mean_cross_harm': statistics.mean(cross_harms) if cross_harms else 0,
        'novelty_rate': len(novelty_hashes) / max(1, total_moves),
    }

# ═══ Decade-to-decade drift ═══
print(f"\n{'='*60}")
print(f"PHASE 0.5: DECADE-LEVEL RHYTHM DRIFT")
print(f"{'='*60}")

decades_sorted = sorted(decade_stats.keys())
drift_vectors = []

for i in range(1, len(decades_sorted)):
    prev_d = decade_stats[decades_sorted[i-1]]
    curr_d = decade_stats[decades_sorted[i]]
    drift = {}
    for f in FEATURES:
        drift[f] = curr_d['centroids'][f] - prev_d['centroids'][f]
    drift_mag = math.sqrt(sum(d**2 for d in drift.values()))
    drift_vectors.append({
        'from': prev_d['label'], 'to': curr_d['label'],
        'from_y0': prev_d['y0'], 'to_y0': curr_d['y0'],
        'drift': drift, 'magnitude': drift_mag,
    })

print(f"\n  {'From':<10} {'To':<10} {'|Drift|':>8}  " +
      '  '.join(f'{f:>10}' for f in FEATURES))
print(f"  {'-'*10} {'-'*10} {'-'*8}  " +
      '  '.join(f"{'-'*10}" for f in FEATURES))

for dv in drift_vectors:
    print(f"  {dv['from']:<10} {dv['to']:<10} {dv['magnitude']:>8.4f}  " +
          '  '.join(f"{dv['drift'][f]:>+10.4f}" for f in FEATURES))

# ═══ Pre-2016 envelope ═══
print(f"\n{'='*60}")
print(f"PRE-2016 HISTORICAL ENVELOPE")
print(f"{'='*60}")

pre2016_drifts = [dv for dv in drift_vectors if dv['to_y0'] <= 2010]
pre2016_magnitudes = [dv['magnitude'] for dv in pre2016_drifts]
if pre2016_magnitudes:
    envelope_mean = statistics.mean(pre2016_magnitudes)
    envelope_sd = statistics.stdev(pre2016_magnitudes)
    envelope_95 = envelope_mean + 1.96 * envelope_sd
    print(f"  Pre-2016 decade drifts (N={len(pre2016_drifts)}):")
    print(f"    Mean |drift|: {envelope_mean:.4f}")
    print(f"    SD:           {envelope_sd:.4f}")
    print(f"    95% envelope: {envelope_95:.4f}")

# E0→E1, E1→E2, E2→E3 as "decade-scale" drifts
for era_pair, label in [(('E0','E1'), 'E0→E1 (2016 shock)'),
                          (('E1','E2'), 'E1→E2 (AI diffusion)'),
                          (('E2','E3'), 'E2→E3 (oracle recovery)')]:
    # Map eras to decade pairs
    pass  # Will use actual year-ranges instead

# ═══ AI-era position vs envelope ═══
print(f"\n{'='*60}")
print(f"AI-ERA SHIFT vs HISTORICAL ENVELOPE")
print(f"{'='*60}")

# Use decade stats directly: 2000s = E0, 2010s = E1+E2, 2020s = E3
e0_decade = decade_stats.get((2000,2009))
e12_decade = decade_stats.get((2010,2019))
e3_decade = decade_stats.get((2020,2026))

if e0_decade and e3_decade:
    print(f"\n  {'Feature':<16} {'2000s':>10} {'2020s':>10} {'Δ':>10} {'Z(Δ)':>8} {'Exceed?':>10}")
    print(f"  {'-'*16} {'-'*10} {'-'*10} {'-'*10} {'-'*8} {'-'*10}")

    for f in FEATURES:
        e0_val = e0_decade['centroids'][f]
        e3_val = e3_decade['centroids'][f]
        delta = e3_val - e0_val
        # Z-score relative to pre-2016 decade drift distribution
        if pre2016_magnitudes and envelope_sd > 0:
            # Use feature-specific pre-2016 drift distribution
            pre_feat_drifts = [dv['drift'][f] for dv in pre2016_drifts]
            feat_mean = statistics.mean(pre_feat_drifts)
            feat_sd = statistics.stdev(pre_feat_drifts) if len(pre_feat_drifts)>1 else 1.0
            z = (abs(delta) - abs(feat_mean)) / max(0.001, feat_sd)
        else:
            z = 0.0
        exceed = 'YES' if z > 1.96 else ('marginal' if z > 1.0 else 'no')
        print(f"  {f:<16} {e0_val:>10.4f} {e3_val:>10.4f} {delta:>+10.4f} {z:>+8.2f} {exceed:>10}")

# ═══ Codex Δ by decade ═══
print(f"\n{'='*60}")
print(f"CODEX Δ BY DECADE")
print(f"{'='*60}")

# Build per-decade Codex and test on next decade
def build_decade_codex(games_by_decade, decade_key):
    games = games_by_decade.get(decade_key, [])
    codex = defaultdict(Counter)
    for moves in games:
        for n in range(15, min(len(moves)-1, 50)):
            prefix = ','.join(f"{c}{coord}" for c,coord in moves[:n])
            codex[prefix][moves[n][1]] += 1
    return dict(codex)

# For each decade, build Codex and test on next decade
codex_deltas = {}
for i in range(len(decades_sorted)-1):
    train_key = decades_sorted[i]
    test_key = decades_sorted[i+1]
    train_games = decade_games[train_key]
    test_games = decade_games[test_key]

    if len(train_games) < 20 or len(test_games) < 20: continue

    codex = build_decade_codex(decade_games, train_key)
    freq = Counter()
    for g in train_games:
        for _, coord in g:
            freq[coord] += 1
    ftot = sum(freq.values())

    fbits = []; cbits = []
    sample = test_games[:min(200, len(test_games))]
    for moves in sample:
        for n in range(15, min(len(moves)-1, 50)):
            prefix = ','.join(f"{c}{coord}" for c,coord in moves[:n])
            actual = moves[n][1]
            pf = freq.get(actual,1)/max(1,ftot)
            pf = max(0.001, min(0.999, pf))
            fbits.append(-math.log2(pf))

            if prefix in codex and actual in codex[prefix]:
                pc = codex[prefix][actual]/sum(codex[prefix].values())
                pc = max(0.001, min(0.999, pc))
            else:
                pc = pf
            cbits.append(-math.log2(pc))

    if fbits and cbits:
        codex_deltas[train_key] = {
            'label': decade_stats[train_key]['label'],
            'test_label': decade_stats[test_key]['label'],
            'freq_bits': statistics.mean(fbits),
            'codex_bits': statistics.mean(cbits),
            'delta': statistics.mean(fbits) - statistics.mean(cbits),
        }

print(f"  {'Train':<10} {'Test':<10} {'Freq bits':>10} {'Codex bits':>10} {'Δ':>8}")
for key in sorted(codex_deltas.keys()):
    cd = codex_deltas[key]
    print(f"  {cd['label']:<10} {cd['test_label']:<10} "
          f"{cd['freq_bits']:>10.3f} {cd['codex_bits']:>10.3f} {cd['delta']:>+8.4f}")

# ═══ Novelty rate by decade ═══
print(f"\n{'='*60}")
print(f"NOVELTY RATE BY DECADE")
print(f"{'='*60}")
print(f"  {'Decade':<12} {'N games':>8} {'N moves':>10} {'Novelty rate':>14}")
for key in decades_sorted:
    ds = decade_stats[key]
    print(f"  {ds['label']:<12} {ds['n_games']:>8} {ds['n_moves']:>10} {ds['novelty_rate']:>14.4f}")

# ═══ Summary ═══
print(f"\n{'='*60}")
print(f"SUMMARY: AI-ERA vs HISTORICAL DRIFT")
print(f"{'='*60}")

if pre2016_magnitudes:
    # Find 2010s→2020s drift
    drift_2010s_2020s = [dv for dv in drift_vectors if dv['from_y0']==2010]
    if drift_2010s_2020s:
        ai_drift = drift_2010s_2020s[0]['magnitude']
        z_ai = (ai_drift - envelope_mean) / max(0.001, envelope_sd)
        print(f"\n  AI-era drift (2010s→2020s): |drift| = {ai_drift:.4f}")
        print(f"  Pre-2016 mean |drift|:      {envelope_mean:.4f} ± {envelope_sd:.4f}")
        print(f"  Z-score:                     {z_ai:+.2f}")
        if z_ai > 1.96:
            print(f"  → AI shift EXCEEDS historical envelope (regime change).")
        elif z_ai > 1.0:
            print(f"  → AI shift is marginal — at the edge of historical variation.")
        else:
            print(f"  → AI shift WITHIN historical envelope (continuity).")

os.makedirs('G:/GameCodex/results/phase05', exist_ok=True)
out = 'G:/GameCodex/results/phase05/decade_drift.csv'
with open(out, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['decade','label','n_games','n_moves','mean_cross_harm',
                'novelty_rate'] + FEATURES)
    for key in decades_sorted:
        ds = decade_stats[key]
        w.writerow([ds['y0'], ds['label'], ds['n_games'], ds['n_moves'],
                    ds['mean_cross_harm'], ds['novelty_rate']] +
                   [ds['centroids'][f] for f in FEATURES])
print(f"\nSaved: {out}")
