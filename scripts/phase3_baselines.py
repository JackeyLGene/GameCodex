"""Phase 3+: Stronger baselines, statistical tests, historical drift envelope.

Adds:
  1. Recency baseline (last-3-years frequency per position)
  2. Sign test on Human Codex > Frequency (21/21)
  3. Bootstrap CI on era Δ
  4. Historical drift envelope (pre-2000 vs post-2000)
"""
import csv, json, statistics, math, random
from collections import defaultdict, Counter

random.seed(42)

# ═══ Load ═══
parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'
games_by_year = defaultdict(list)
with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','');
        if not y or y == 'None': continue
        year = int(y)
        moves = json.loads(row.get('moves','[]'))
        if len(moves) < 30: continue
        games_by_year[year].append(moves)

YEARS = sorted(y for y in games_by_year.keys() if y >= 2000)
print(f"Years: {min(YEARS)}-{max(YEARS)}, total games: {sum(len(v) for y,v in games_by_year.items() if y>=2000)}")

# ═══ Codex builders ═══
def build_position_codex(games, prefix_len=15):
    codex = defaultdict(Counter)
    for moves in games:
        for n in range(prefix_len, min(len(moves)-1, 50)):
            prefix = ','.join(f"{c}{coord}" for c, coord in moves[:n])
            codex[prefix][moves[n][1]] += 1
    return dict(codex)

def build_recency_codex(year_range, prefix_len=15):
    """Build Codex from a specific range of years."""
    games = [g for y in year_range for g in games_by_year.get(y, [])]
    return build_position_codex(games, prefix_len)

def predict(codex, prefix_moves):
    prefix = ','.join(f"{c}{coord}" for c, coord in prefix_moves)
    if prefix not in codex: return None
    counts = codex[prefix]
    top = counts.most_common(1)
    total = sum(c for _, c in top)
    return [(move, count/total) for move, count in top]

def encode_move(codex, prefix_moves, actual_move, global_freq=None, freq_total=None):
    """Bits to encode actual move under Codex."""
    pred = predict(codex, prefix_moves)
    if pred:
        p = sum(prob for move, prob in pred if move == actual_move)
        if p > 0:
            p = max(0.001, min(0.999, p))
        elif global_freq:
            p = global_freq.get(actual_move, 1) / max(1, freq_total)
            p = max(0.001, min(0.999, p))
        else:
            p = 0.001
    elif global_freq:
        p = global_freq.get(actual_move, 1) / max(1, freq_total)
        p = max(0.001, min(0.999, p))
    else:
        p = 0.001
    return -math.log2(p)

# ═══ Held-out with multiple baselines ═══
MIN_TRAIN = 5
RECENCY_WINDOW = 3  # years

print(f"\n{'='*60}")
print(f"PHASE 3+: STRONGER BASELINES + STATISTICAL TESTS")
print(f"{'='*60}")

results = []
for test_idx in range(MIN_TRAIN, len(YEARS)):
    test_year = YEARS[test_idx]
    train_years = [y for y in YEARS[:test_idx]]

    # Full historical Codex
    train_games = [g for y in train_years for g in games_by_year[y]]
    hist_codex = build_position_codex(train_games, prefix_len=15)

    # Recency Codex (last 3 years before test)
    recency_years = [y for y in train_years if y >= test_year - RECENCY_WINDOW]
    if not recency_years: recency_years = train_years[-RECENCY_WINDOW:]
    recency_codex = build_position_codex(
        [g for y in recency_years for g in games_by_year[y]], prefix_len=15)

    # Global frequency
    global_freq = Counter()
    for g in train_games:
        for _, coord in g:
            global_freq[coord] += 1
    freq_total = sum(global_freq.values())

    # Test
    test_games = random.sample(games_by_year[test_year],
                                min(500, len(games_by_year[test_year])))

    freq_bits = []
    hist_bits = []
    recency_bits = []
    n_pred = 0

    for moves in test_games:
        for n_pos in range(15, min(len(moves)-1, 40)):
            prefix = moves[:n_pos]
            actual = moves[n_pos][1]

            p_freq = global_freq.get(actual, 1) / max(1, freq_total)
            p_freq = max(0.001, min(0.999, p_freq))
            freq_bits.append(-math.log2(p_freq))

            hist_bits.append(encode_move(hist_codex, prefix, actual, global_freq, freq_total))
            recency_bits.append(encode_move(recency_codex, prefix, actual, global_freq, freq_total))
            n_pred += 1

    era = 'E0' if test_year <= 2015 else ('E1' if test_year <= 2017 else
           ('E2' if test_year <= 2021 else 'E3'))

    results.append({
        'test_year': test_year, 'era': era,
        'freq_bits': statistics.mean(freq_bits),
        'hist_bits': statistics.mean(hist_bits),
        'recency_bits': statistics.mean(recency_bits),
        'delta_hist': statistics.mean(freq_bits) - statistics.mean(hist_bits),
        'delta_recency': statistics.mean(freq_bits) - statistics.mean(recency_bits),
        'hist_vs_recency': statistics.mean(hist_bits) - statistics.mean(recency_bits),
        'n_pred': n_pred,
    })

# ═══ Report ═══
print(f"\n  {'Year':<6} {'Δ(Hist)':>10} {'Δ(Recency)':>12} {'Hist vs Rec':>12}")
for r in results:
    print(f"  {r['test_year']:<6} {r['delta_hist']:>+10.3f} "
          f"{r['delta_recency']:>+12.3f} {r['hist_vs_recency']:>+12.3f}")

# ═══ Statistical tests ═══

# Sign test: is 21/21 significant?
n_years = len(results)
n_hist_win = sum(1 for r in results if r['delta_hist'] > 0)
# Under H0 (no effect), P(win) = 0.5 per year
# Binomial test: P(X >= n_hist_win) with n=n_years, p=0.5
from math import comb
p_binom = sum(comb(n_years, k) * (0.5**n_years) for k in range(n_hist_win, n_years+1))

print(f"\n{'='*60}")
print(f"STATISTICAL TESTS")
print(f"{'='*60}")
print(f"\n  Sign test (Human Codex > Frequency):")
print(f"    {n_hist_win}/{n_years} years, p = {p_binom:.6f}")
print(f"    → {'SIGNIFICANT' if p_binom < 0.01 else ('marginal' if p_binom < 0.05 else 'not significant')}")

# Recency sign test
n_recency_win = sum(1 for r in results if r['delta_recency'] > 0)
p_recency = sum(comb(n_years, k) * (0.5**n_years) for k in range(n_recency_win, n_years+1))
print(f"\n  Sign test (Recency Codex > Frequency):")
print(f"    {n_recency_win}/{n_years} years, p = {p_recency:.6f}")

# Hist vs Recency
n_hist_better = sum(1 for r in results if r['hist_vs_recency'] < 0)
p_hvr = sum(comb(n_years, k) * (0.5**n_years) for k in range(n_hist_better, n_years+1))
print(f"\n  Sign test (Hist < Recency):")
print(f"    {n_hist_better}/{n_years} years, p = {p_hvr:.6f}")
print(f"    Hist better than Recency in {n_years - n_hist_better}/{n_years} years")

# ═══ Bootstrap CI on era Δ ═══
print(f"\n{'='*60}")
print(f"BOOTSTRAP CI — ERA Δ VALUES")
print(f"{'='*60}")

era_deltas = defaultdict(list)
for r in results:
    era_deltas[r['era']].append(r['delta_hist'])

for era in ['E0','E1','E2','E3']:
    if era not in era_deltas or len(era_deltas[era]) < 2: continue
    vals = era_deltas[era]
    mean_obs = statistics.mean(vals)

    # Bootstrap
    n_boot = 10000
    boot_means = []
    for _ in range(n_boot):
        sample = [random.choice(vals) for _ in range(len(vals))]
        boot_means.append(statistics.mean(sample))
    boot_means.sort()
    ci_lo = boot_means[250]   # 2.5%
    ci_hi = boot_means[9750]  # 97.5%

    print(f"  {era}: Δ={mean_obs:+.4f}  [95% CI: {ci_lo:+.4f}, {ci_hi:+.4f}]")

# ═══ E2 dip significance ═══
if 'E2' in era_deltas and 'E3' in era_deltas:
    d_e2e3 = statistics.mean(era_deltas['E3']) - statistics.mean(era_deltas['E2'])
    print(f"\n  E2→E3 recovery: ΔΔ = {d_e2e3:+.4f}")

# ═══ Historical drift envelope (pre-2000 baseline) ═══
print(f"\n{'='*60}")
print(f"HISTORICAL DRIFT ENVELOPE (pre-2000)")
print(f"{'='*60}")

pre2000_years = [y for y in YEARS if y < 2000]
post2000_years = [y for y in YEARS if y >= 2000]

if pre2000_years:
    pre_games = [g for y in pre2000_years[:10] for g in games_by_year[y]]
    pre_codex = build_position_codex(pre_games, prefix_len=15)

    # Test on post-2000: does pre-2000 Codex still work?
    test_post = [g for y in post2000_years[:3] for g in games_by_year[y]]
    test_sample = random.sample(test_post, min(200, len(test_post)))

    pre_freq = Counter()
    for g in pre_games:
        for _, coord in g:
            pre_freq[coord] += 1
    pre_total = sum(pre_freq.values())

    pre_bits = []
    pre_freq_bits = []
    for moves in test_sample:
        for n in range(15, min(len(moves)-1, 40)):
            prefix = moves[:n]
            actual = moves[n][1]
            p = pre_freq.get(actual, 1) / max(1, pre_total)
            p = max(0.001, min(0.999, p))
            pre_freq_bits.append(-math.log2(p))
            pre_bits.append(encode_move(pre_codex, prefix, actual, pre_freq, pre_total))

    print(f"  Pre-2000 Codex → Post-2000 test:")
    print(f"    Freq bits:  {statistics.mean(pre_freq_bits):.3f}")
    print(f"    Codex bits: {statistics.mean(pre_bits):.3f}")
    print(f"    Δ:          {statistics.mean(pre_freq_bits) - statistics.mean(pre_bits):+.4f}")
    print(f"  → Pre-2000 Codex still beats frequency cross-era: "
          f"{'YES' if statistics.mean(pre_bits) < statistics.mean(pre_freq_bits) else 'NO'}")
else:
    print("  No pre-2000 data available")

print(f"\n{'='*60}")
print(f"SUMMARY")
print(f"{'='*60}")
print(f"  Human Codex > Frequency:  {n_hist_win}/{n_years} years (p={p_binom:.6f})")
print(f"  Recency Codex > Frequency: {n_recency_win}/{n_years} years (p={p_recency:.6f})")

# Fix the syntax for the final print
hist_mean = statistics.mean(r['delta_hist'] for r in results)
recency_mean = statistics.mean(r['delta_recency'] for r in results)
print(f"  Mean Δ Hist:    {hist_mean:+.4f} bits/move")
print(f"  Mean Δ Recency: {recency_mean:+.4f} bits/move")

# Write detailed results
out_csv = 'G:/GameCodex/results/phase3/baselines_plus.csv'
import os
os.makedirs('G:/GameCodex/results/phase3', exist_ok=True)
with open(out_csv, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['test_year','era','freq_bits','hist_bits',
                                       'recency_bits','delta_hist','delta_recency',
                                       'hist_vs_recency','n_pred'])
    w.writeheader()
    for r in results:
        w.writerow(r)
print(f"\nSaved: {out_csv}")
