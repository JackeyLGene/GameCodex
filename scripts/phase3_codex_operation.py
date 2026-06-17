"""Phase 3: Codex Operation — held-out move prediction.

Core test: Human Codex vs AI Codex prediction accuracy across eras.
Feature-wise: does AI Codex gain predictive power selectively on
the rhythm features where Phase 2 showed alignment?

Codex definitions:
  Human Codex: P(move | position_prefix) from historical frequency
  AI Codex:    KataGo top-1 move as the "oracle recommendation"
  Frequency:   global move frequency (no position context)
  Recency:      last-3-years move frequency per position

Held-out: train on years < t, evaluate on year t.
"""
import csv, json, statistics, math, random
from collections import defaultdict, Counter

random.seed(42)

SGF_COLS = 'abcdefghijklmnopqrs'

# ═══ Load data ═══
parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'
games_by_year = defaultdict(list)
with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','');
        if not y or y == 'None': continue
        year = int(y)
        if year < 2000 or year > 2025: continue
        moves = json.loads(row.get('moves','[]'))
        if len(moves) < 30: continue
        games_by_year[year].append(moves)

print(f"Loaded {sum(len(v) for v in games_by_year.values())} games from "
      f"{min(games_by_year)}-{max(games_by_year)}")

# ═══ Build Codex from training years ═══

def build_position_codex(games, prefix_len=15):
    """For each position (first N moves), record next-move frequency."""
    codex = defaultdict(Counter)
    for moves in games:
        for n in range(prefix_len, min(len(moves)-1, 50)):
            # Position key: SGF moves as comma-separated string
            prefix = ','.join(f"{c}{coord}" for c, coord in moves[:n])
            next_move = moves[n][1]  # coordinate only, ignore color
            codex[prefix][next_move] += 1
    return dict(codex)

def predict_codex(codex, prefix_moves, top_k=1):
    """Predict the most frequent next move(s) from Codex."""
    prefix = ','.join(f"{c}{coord}" for c, coord in prefix_moves)
    if prefix not in codex:
        return None
    counts = codex[prefix]
    top = counts.most_common(top_k)
    total = sum(c for _, c in top)
    return [(move, count/total) for move, count in top]

def compute_rhythm_simple(prefix_moves, candidate_move_sgf):
    """Quick rhythm: adj_opp, adj_own, dens_delta only (Phase 2 alignment features)."""
    board = {}
    for color, coord in prefix_moves:
        c = SGF_COLS.find(coord[0])
        r = SGF_COLS.find(coord[1])
        if c >= 0 and r >= 0: board[(c, r)] = color

    cx = SGF_COLS.find(candidate_move_sgf[0])
    cy = SGF_COLS.find(candidate_move_sgf[1])
    if cx < 0 or cy < 0: return None

    mc = 'B' if len(prefix_moves) % 2 == 0 else 'W'
    board[(cx, cy)] = mc
    oc = 'W' if mc == 'B' else 'B'

    adj_opp = adj_own = 0
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = cx+dx, cy+dy
        if 0 <= nx < 19 and 0 <= ny < 19:
            s = board.get((nx, ny))
            if s == oc: adj_opp += 1
            elif s == mc: adj_own += 1

    own_cnt = opp_cnt = 0
    for (sx, sy), clr in board.items():
        if (sx, sy) == (cx, cy): continue
        if math.sqrt((cx-sx)**2 + (cy-sy)**2) <= 3:
            if clr == oc: opp_cnt += 1
            elif clr == mc: own_cnt += 1

    return {
        'adj_opp': adj_opp/4.0,
        'adj_own': adj_own/4.0,
        'dens_delta': (own_cnt - opp_cnt)/10.0,
    }

# ═══ Load KataGo AI Codex ═══
# Pre-computed from Phase 2: position -> KataGo top move
ai_codex = {}
kg_file = 'G:/GameCodex/results/phase2/katago_alignment.csv'
kg_count = 0
try:
    with open(kg_file) as f:
        for row in csv.DictReader(f):
            # We only have 200 positions with KataGo analysis
            # Use these as a reference: for similar positions, use KataGo top-1
            kg_count += 1
except: pass

# For now: build a simple AI proxy.
# KataGo top-1 across our 200 analyzed positions gives a "global AI preference"
# For held-out test: use KataGo's rhythm signature as the AI prediction target

# ═══ Held-out evaluation: year-by-year ═══

YEARS = sorted(games_by_year.keys())
MIN_TRAIN = 5  # minimum training years

print(f"\n{'='*60}")
print(f"PHASE 3: CODEX OPERATION — YEARLY HELD-OUT")
print(f"{'='*60}")

results = []

for test_idx in range(MIN_TRAIN, len(YEARS)):
    test_year = YEARS[test_idx]
    train_years = YEARS[:test_idx]

    # Build Codex from training years
    train_games = [g for y in train_years for g in games_by_year[y]]
    codex = build_position_codex(train_games, prefix_len=15)

    # Global frequency (no position context)
    global_freq = Counter()
    for g in train_games:
        for _, coord in g:
            global_freq[coord] += 1
    freq_total = sum(global_freq.values())

    # Test games (sample to keep runtime manageable)
    test_games_all = games_by_year[test_year]
    n_test = min(500, len(test_games_all))
    test_games = random.sample(test_games_all, n_test)

    # Evaluate
    freq_bits = []
    codex_bits = []
    n_pred = 0
    codex_hit = 0
    freq_hit = 0

    # Feature-wise tracking
    align_feat_bits = []     # adj_opp, adj_own, dens_delta
    nonalign_feat_bits = []  # dist_last, is_corner_open equivalent

    for moves in test_games:
        for n in range(15, min(len(moves)-1, 40)):
            prefix = moves[:n]
            actual = moves[n][1]

            # Frequency baseline
            p_freq = global_freq.get(actual, 1) / max(1, freq_total)
            p_freq = max(0.001, min(0.999, p_freq))
            freq_bits.append(-math.log2(p_freq))

            # Codex prediction
            pred = predict_codex(codex, prefix)
            if pred:
                p_codex = sum(prob for move, prob in pred if move == actual)
                p_codex = max(0.001, min(0.999, p_codex if p_codex > 0 else 0.001))
                codex_bits.append(-math.log2(p_codex))
                if p_codex > 0.1: codex_hit += 1
            else:
                # Codex unseen: use frequency fallback
                codex_bits.append(-math.log2(p_freq))

            if p_freq > 0.01: freq_hit += 1
            n_pred += 1

    if not freq_bits or not codex_bits: continue

    delta = statistics.mean(freq_bits) - statistics.mean(codex_bits)
    era = 'E0' if test_year <= 2015 else ('E1' if test_year <= 2017 else
           ('E2' if test_year <= 2021 else 'E3'))

    results.append({
        'test_year': test_year, 'era': era,
        'n_train_years': len(train_years), 'n_test_games': n_test,
        'n_predictions': n_pred,
        'freq_bits': statistics.mean(freq_bits),
        'codex_bits': statistics.mean(codex_bits),
        'delta': delta,
        'codex_hit_rate': codex_hit / max(1, n_pred),
        'freq_hit_rate': freq_hit / max(1, n_pred),
    })

# ═══ Report ═══

print(f"\n  {'Year':<6} {'Era':<4} {'N_pred':>7} {'Freq_bits':>10} {'Codex_bits':>10} {'Δ':>8}")
print(f"  {'-'*6} {'-'*4} {'-'*7} {'-'*10} {'-'*10} {'-'*8}")

for r in results:
    print(f"  {r['test_year']:<6} {r['era']:<4} {r['n_predictions']:>7} "
          f"{r['freq_bits']:>10.3f} {r['codex_bits']:>10.3f} "
          f"{r['delta']:>+8.3f}")

# Era summary
print(f"\n{'='*60}")
print(f"ERA SUMMARY")
print(f"{'='*60}")
era_summary = defaultdict(list)
for r in results:
    era_summary[r['era']].append(r)

print(f"  {'Era':<4} {'N_years':>8} {'Mean Δ':>10} {'Codex_hit':>10}")
for era in ['E0', 'E1', 'E2', 'E3']:
    if era_summary[era]:
        rs = era_summary[era]
        mean_delta = statistics.mean(r['delta'] for r in rs)
        mean_hit = statistics.mean(r['codex_hit_rate'] for r in rs)
        print(f"  {era:<4} {len(rs):>8} {mean_delta:>+10.3f} {mean_hit:>10.3f}")

print(f"\n  Human Codex > Frequency: "
      f"{sum(1 for r in results if r['delta'] > 0)}/{len(results)} years")

# ═══ Feature-wise breakdown (Phase 3 specific addition) ═══

print(f"\n{'='*60}")
print(f"FEATURE-WISE: Does Codex gain concentrate on alignment features?")
print(f"{'='*60}")

# For test year 2024 (E3), compute per-position Codex gain
# and correlate with rhythm alignment
test_2024_games = random.sample(games_by_year[2024], min(200, len(games_by_year[2024])))
train_games_pre2024 = [g for y in YEARS if y < 2024 for g in games_by_year[y]]
codex_2024 = build_position_codex(train_games_pre2024, prefix_len=15)

feat_results = []
for moves in test_2024_games:
    for n in range(15, min(len(moves)-1, 40)):
        prefix = moves[:n]
        actual = moves[n][1]

        pred = predict_codex(codex_2024, prefix)
        p_codex = 0.001
        if pred:
            for move, prob in pred:
                if move == actual:
                    p_codex = prob
                    break
        p_codex = max(0.001, min(0.999, p_codex))
        codex_gain = -math.log2(p_codex)

        rhythm = compute_rhythm_simple([(c, coord) for c, coord in prefix], actual)
        if rhythm is None: continue

        # Alignment score: average of adj_opp, adj_own, dens_delta (normalized)
        align_score = (rhythm['adj_opp'] + rhythm['adj_own'] + abs(rhythm['dens_delta'])) / 3.0

        feat_results.append({
            'codex_gain': codex_gain,
            'align_score': align_score,
            'adj_opp': rhythm['adj_opp'],
            'adj_own': rhythm['adj_own'],
            'dens_delta': rhythm['dens_delta'],
        })

if feat_results:
    # Split by alignment score median
    median_align = statistics.median(r['align_score'] for r in feat_results)
    high_align = [r for r in feat_results if r['align_score'] >= median_align]
    low_align = [r for r in feat_results if r['align_score'] < median_align]

    print(f"  N positions: {len(feat_results)}")
    print(f"  Median alignment score: {median_align:.3f}")
    print(f"  High align (N={len(high_align)}): Codex bits = "
          f"{statistics.mean(r['codex_gain'] for r in high_align):.3f}")
    print(f"  Low align  (N={len(low_align)}):  Codex bits = "
          f"{statistics.mean(r['codex_gain'] for r in low_align):.3f}")

    # Correlation: codex gain vs alignment features
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
        return sum((rx[i]-mx)*(ry[i]-my) for i in range(n))/max(.001,
            math.sqrt(sum((rx[i]-mx)**2 for i in range(n))*sum((ry[i]-my)**2 for i in range(n))))

    gains = [r['codex_gain'] for r in feat_results]
    for feat in ['adj_opp', 'adj_own', 'dens_delta', 'align_score']:
        vals = [r[feat] for r in feat_results]
        rho = spearman(gains, vals)
        print(f"  ρ(codex_gain, {feat:>12}) = {rho:+.3f}")
