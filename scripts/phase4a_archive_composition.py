"""Phase 4A: Archive Composition Matrix.

CWI is not a transparent window — it's a Codex deposit.
This script maps: decade × region × player × event × source.

Outputs:
  - archive_composition_by_decade.csv
  - region_share_timeline.csv
  - coverage_breaks.md
"""
import csv, json, math, os
from collections import defaultdict, Counter

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
INTL_KW = ['ing cup','chunlan','fujitsu','tongyang','tong yang','world',
           'international','asian','intercontinental','sponsorship']

def classify(event):
    if not event: return 'unknown'
    e = event.lower().strip()
    for kw in JPN_KW:
        if kw in e: return 'JPN'
    for kw in KOR_KW:
        if kw in e: return 'KOR'
    for kw in CHN_KW:
        if kw in e: return 'CHN'
    for kw in INTL_KW:
        if kw in e: return 'INTL'
    return 'JPN'  # CWI is Japan-centric

# ═══ Load ═══
parsed_csv = 'G:/GameCodex/data/parsed/go_games_parsed.csv'
rows_by_decade = defaultdict(list)

with open(parsed_csv, encoding='utf-8') as f:
    for row in csv.DictReader(f):
        y = row.get('year','')
        if not y or y=='None': continue
        year = int(y)
        decade = (year//10)*10
        dkey = (decade, decade+9)

        event = row.get('event','')
        region = classify(event)

        rows_by_decade[dkey].append({
            'year': year,
            'region': region,
            'event': event,
            'black': row.get('black_player','?'),
            'white': row.get('white_player','?'),
            'black_rank': row.get('black_rank','?'),
            'white_rank': row.get('white_rank','?'),
            'result': row.get('result','?'),
            'source': row.get('source_file','?'),
        })

print(f"Loaded {sum(len(v) for v in rows_by_decade.values()):,} games across "
      f"{len(rows_by_decade)} decades")

# ═══ 4A.1: Decade × Region composition ═══
print(f"\n{'='*60}")
print(f"4A.1: REGION COMPOSITION BY DECADE")
print(f"{'='*60}")
print(f"  {'Decade':<12} {'JPN':>8} {'KOR':>8} {'CHN':>8} {'INTL':>8} {'unknown':>8} {'total':>8} {'region_entropy':>10}")
print(f"  {'-'*12} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*10}")

comp_data = []
for dkey in sorted(rows_by_decade.keys()):
    rows = rows_by_decade[dkey]
    rc = Counter(r['region'] for r in rows)
    total = len(rows)
    # Shannon entropy of region distribution
    entropy = -sum((c/total)*math.log2(c/total) for c in rc.values() if c>0)
    comp_data.append({
        'decade': dkey[0],
        'label': f"{dkey[0]}s",
        'total': total,
        'JPN': rc.get('JPN',0), 'KOR': rc.get('KOR',0),
        'CHN': rc.get('CHN',0), 'INTL': rc.get('INTL',0),
        'unknown': rc.get('unknown',0),
        'region_entropy': entropy,
    })
    print(f"  {dkey[0]}s{' '*7} {rc.get('JPN',0):>8} {rc.get('KOR',0):>8} "
          f"{rc.get('CHN',0):>8} {rc.get('INTL',0):>8} {rc.get('unknown',0):>8} "
          f"{total:>8} {entropy:>10.4f}")

# ═══ 4A.2: Player diversity ═══
print(f"\n{'='*60}")
print(f"4A.2: PLAYER DIVERSITY BY DECADE")
print(f"{'='*60}")
print(f"  {'Decade':<12} {'Unique players':>14} {'Games/player':>14} {'Top5 share':>10}")

for dkey in sorted(rows_by_decade.keys()):
    rows = rows_by_decade[dkey]
    players = set()
    for r in rows:
        players.add(r['black'])
        players.add(r['white'])
    n_players = len(players)
    n_games = len(rows)
    gpp = n_games / max(1, n_players)
    # Herfindahl: concentration of games among top players
    pc = Counter()
    for r in rows:
        pc[r['black']] += 1; pc[r['white']] += 1
    top5_share = sum(c for _,c in pc.most_common(5)) / sum(pc.values()) if pc else 0
    print(f"  {dkey[0]}s{' '*7} {n_players:>14} {gpp:>14.1f} {top5_share:>10.3f}")

# ═══ 4A.3: Event diversity ═══
print(f"\n{'='*60}")
print(f"4A.3: EVENT DIVERSITY BY DECADE")
print(f"{'='*60}")
print(f"  {'Decade':<12} {'Unique events':>14} {'Games/event':>14} {'Top event':>25}")

for dkey in sorted(rows_by_decade.keys()):
    rows = rows_by_decade[dkey]
    events = Counter(r['event'] for r in rows if r['event'])
    top_ev = events.most_common(1)[0] if events else ('?',0)
    print(f"  {dkey[0]}s{' '*7} {len(events):>14} {len(rows)/max(1,len(events)):>14.1f} "
          f"{top_ev[0][:25]:>25}")

# ═══ 4A.4: Coverage breaks ═══
print(f"\n{'='*60}")
print(f"4A.4: COVERAGE BREAKS (year-to-year game count changes)")
print(f"{'='*60}")

# Year-level counts for break detection
year_counts = defaultdict(int)
for dkey, rows in rows_by_decade.items():
    for r in rows:
        year_counts[r['year']] += 1

years = sorted(year_counts.keys())
breaks = []
for i in range(1, len(years)):
    y0, c0 = years[i-1], year_counts[years[i-1]]
    y1, c1 = years[i], year_counts[years[i]]
    if c0 > 0:
        ratio = c1 / c0
        if ratio > 3 or ratio < 0.33:
            breaks.append((y0, y1, c0, c1, ratio))

print(f"  Year-to-year breaks (>3× or <0.33×):")
for y0, y1, c0, c1, ratio in breaks[-20:]:
    direction = '↑' if ratio > 1 else '↓'
    print(f"  {y0}→{y1}: {c0:>6} → {c1:>6} ({ratio:.1f}×) {direction}")

# ═══ Save ═══
out_dir = 'G:/GameCodex/results/phase4'
os.makedirs(out_dir, exist_ok=True)

# Composition
comp_csv = os.path.join(out_dir, 'archive_composition_by_decade.csv')
with open(comp_csv, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['decade','label','total','JPN','KOR','CHN',
                                       'INTL','unknown','region_entropy'])
    w.writeheader()
    for row in comp_data:
        w.writerow(row)

# Region share timeline (year level)
region_csv = os.path.join(out_dir, 'region_share_timeline.csv')
with open(region_csv, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['year','JPN','KOR','CHN','INTL','unknown','total','region_entropy'])
    for year in sorted(year_counts.keys()):
        dkey = ((year//10)*10, (year//10)*10+9)
        rows = rows_by_decade.get(dkey, [])
        yr_rows = [r for r in rows if r['year']==year]
        if not yr_rows: continue
        rc = Counter(r['region'] for r in yr_rows)
        total = len(yr_rows)
        entropy = -sum((c/total)*math.log2(c/total) for c in rc.values() if c>0)
        w.writerow([year, rc.get('JPN',0), rc.get('KOR',0),
                     rc.get('CHN',0), rc.get('INTL',0),
                     rc.get('unknown',0), total, entropy])

# Coverage breaks
breaks_md = os.path.join(out_dir, 'coverage_breaks.md')
with open(breaks_md, 'w') as f:
    f.write("# CWI Coverage Breaks\n\n")
    f.write("Year-to-year game count changes exceeding 3× or below 0.33×.\n\n")
    f.write("| From | To | Count0 | Count1 | Ratio | Direction |\n")
    f.write("|------|----|--------|--------|-------|----------|\n")
    for y0, y1, c0, c1, ratio in breaks:
        d = '↑' if ratio > 1 else '↓'
        f.write(f"| {y0} | {y1} | {c0:,} | {c1:,} | {ratio:.1f}× | {d} |\n")

print(f"\nSaved:")
print(f"  {comp_csv}")
print(f"  {region_csv}")
print(f"  {breaks_md}")
print(f"\nPhase 4A complete. Ready for 4B (region-controlled replication).")
