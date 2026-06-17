"""SGF Parser: professional Go game records -> standardized CSV/JSONL.

Extracts: date, players, ranks, result, komi, moves.
Maps date -> year -> era.

Usage: python parse_sgf.py <sgf_dir_or_file> --out results/parsed/
"""
import os, sys, re, json, csv, argparse
from collections import Counter

ERA_MAP = [
    (2022, "E3"),
    (2018, "E2"),
    (2016, "E1"),
    (2000, "E0"),
    (0, "pre2000"),
]

def parse_sgf_text(text):
    """Parse SGF text into structured dict. Extracts:
    - date (YYYY-MM-DD or YYYY-MM or YYYY)
    - black_player, white_player
    - black_rank, white_rank
    - result (B+R, W+2.5, etc.)
    - komi
    - moves: list of (color, coord) e.g. ('B', 'pd'), ('W', 'dp')
    """
    record = {
        'date': None, 'year': None, 'era': None,
        'black_player': None, 'white_player': None,
        'black_rank': None, 'white_rank': None,
        'result': None, 'komi': None,
        'moves': [], 'n_moves': 0,
        'event': None, 'source_file': None,
    }

    # Extract header fields using SGF property syntax
    props = {
        'DT': 'date', 'PB': 'black_player', 'PW': 'white_player',
        'BR': 'black_rank', 'WR': 'white_rank',
        'RE': 'result', 'KM': 'komi', 'EV': 'event',
    }
    for prop, field in props.items():
        m = re.search(rf'{prop}\[([^\]]*)\]', text)
        if m:
            record[field] = m.group(1).strip()

    # Parse date
    if record['date']:
        parts = record['date'].split('-')
        if len(parts) >= 1 and parts[0].isdigit():
            record['year'] = int(parts[0])
            for year_thresh, era_label in ERA_MAP:
                if record['year'] >= year_thresh:
                    record['era'] = era_label
                    break

    # Parse moves: SGF uses ;B[coord] ;W[coord] format
    move_pattern = re.findall(r';(B|W)\[([a-z]{2})\]', text)
    record['moves'] = [(color, coord) for color, coord in move_pattern]
    record['n_moves'] = len(record['moves'])

    # Parse result to winner
    if record['result']:
        r = record['result']
        if r.startswith('B+') or r.startswith('W+'):
            record['winner'] = 'B' if r.startswith('B+') else 'W'
        elif 'Resign' in r or 'resign' in r.lower():
            record['winner'] = 'B' if r.startswith('W') else ('W' if r.startswith('B') else None)
        else:
            record['winner'] = None

    return record

def parse_file(filepath):
    """Parse a single SGF file. Returns list of records (usually 1 per file)."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()

    # Some SGF files contain multiple games (separate trees)
    games = []
    # Find all game trees: (; ... )
    # Simple approach: split on '(;' and rejoin
    chunks = text.split('(;')
    for chunk in chunks:
        if not chunk.strip():
            continue
        chunk = '(;' + chunk
        record = parse_sgf_text(chunk)
        record['source_file'] = os.path.basename(filepath)
        if record['n_moves'] > 0:
            games.append(record)
    return games

def parse_directory(dirpath, extensions=('.sgf',)):
    """Parse all SGF files in directory recursively."""
    all_games = []
    n_files = 0
    for root, dirs, files in os.walk(dirpath):
        for fname in files:
            if fname.lower().endswith(extensions):
                filepath = os.path.join(root, fname)
                try:
                    games = parse_file(filepath)
                    all_games.extend(games)
                    n_files += 1
                except Exception as e:
                    print(f"  Error parsing {fname}: {e}")
    return all_games, n_files

def main():
    parser = argparse.ArgumentParser(description='Parse SGF Go game records')
    parser.add_argument('input', help='SGF file or directory')
    parser.add_argument('--out', default='G:/GameCodex/data/parsed',
                        help='Output directory')
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    if os.path.isfile(args.input):
        games = parse_file(args.input)
        n_files = 1
    else:
        games, n_files = parse_directory(args.input)

    print(f"Parsed {n_files} files -> {len(games)} games")

    if not games:
        print("No games found.")
        return

    # Year distribution
    years = Counter(g['year'] for g in games if g['year'])
    eras = Counter(g['era'] for g in games if g['era'])

    print(f"\nYear range: {min(years.keys())} - {max(years.keys())}")
    print(f"Games with year: {sum(years.values())}")
    print(f"\nBy era:")
    for era in ['E0', 'E1', 'E2', 'E3', 'pre2000']:
        if eras[era] > 0:
            print(f"  {era}: {eras[era]}")

    print(f"\nBy year (top 20):")
    for year in sorted(years.keys(), reverse=True)[:20]:
        print(f"  {year}: {years[year]}")

    # Save parsed data
    # CSV: one row per game with summary + moves as JSON
    csv_path = os.path.join(args.out, 'go_games_parsed.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['source_file', 'year', 'era', 'date',
                      'black_player', 'white_player',
                      'black_rank', 'white_rank',
                      'result', 'winner', 'komi', 'event',
                      'n_moves', 'moves']
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader()
        for g in games:
            g['moves'] = json.dumps(g['moves'])
            w.writerow(g)

    print(f"\nSaved: {csv_path}")
    print(f"  Total games: {len(games)}")

if __name__ == '__main__':
    main()
