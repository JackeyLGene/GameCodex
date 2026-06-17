"""KataGo analysis wrapper: send JSON queries, parse policy output.

Usage: python scripts/run_katago.py
  Reads positions from phase2 sampled data, runs KataGo, saves policy results.
"""
import subprocess, json, os, csv

KATAGO_EXE = 'G:/GameCodex/data/katago/katago.exe'
KATAGO_CFG = 'G:/GameCodex/data/katago/analysis.cfg'
KATAGO_MODEL = 'G:/GameCodex/data/katago/model.bin.gz'

def start_katago():
    """Start KataGo analysis engine process."""
    proc = subprocess.Popen(
        [KATAGO_EXE, 'analysis', '-config', KATAGO_CFG, '-model', KATAGO_MODEL],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, bufsize=1
    )
    # Read until ready
    for line in proc.stderr:
        if 'Started, ready to begin handling requests' in line:
            break
    return proc

def query_position(proc, moves_list, max_visits=200):
    """Send a position query, return policy data."""
    query = {
        'id': 'pos1',
        'moves': moves_list,
        'rules': 'japanese',
        'komi': 6.5,
        'boardXSize': 19,
        'boardYSize': 19,
        'maxVisits': max_visits,
        'includePolicy': True,
    }
    proc.stdin.write(json.dumps(query) + '\n')
    proc.stdin.flush()

    # Read response
    for line in proc.stdout:
        line = line.strip()
        if not line: continue
        try:
            data = json.loads(line)
            if data.get('id') == 'pos1':
                return data
        except:
            continue
    return None

def test_katago():
    """Quick test of KataGo analysis."""
    print("Starting KataGo...")
    proc = start_katago()
    print("KataGo ready. Testing position...")

    # Simple opening: hoshi (Q16), hoshi (D4), komoku (Q4)
    # GTP format: letter+number, letter=A-T (skip I)
    moves = [['B', 'Q16'], ['W', 'D4'], ['B', 'Q4']]
    result = query_position(proc, moves, max_visits=100)

    proc.stdin.close()
    proc.terminate()

    if result and 'moveInfos' in result:
        print(f"\nAnalysis result:")
        print(f"  Root winrate: {result.get('rootInfo', {}).get('winrate', '?')}")
        print(f"  Top 5 moves:")
        for mi in result['moveInfos'][:5]:
            print(f"    {mi.get('move', '?'):>6}  "
                  f"winrate={mi.get('winrate', 0):.4f}  "
                  f"prior={mi.get('prior', 0):.4f}  "
                  f"order={mi.get('order', '?')}")
        print("\nKataGo working correctly!")
        return True
    else:
        print(f"Error: unexpected response")
        print(result)
        return False

if __name__ == '__main__':
    test_katago()
