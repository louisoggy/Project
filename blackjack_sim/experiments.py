import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import csv
import math
import statistics
from blackjack import run_counter

def save_csv(rows, filename):
    if not rows:
        print(f"save_csv: nothing to write for {filename}")
        return

    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    path = os.path.join(results_dir, filename)

    # column order comes from the first row's insertion order
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"saved {len(rows)} row(s) -> {path}")


def run_trials(trials=10, num_hands=500000, num_decks=6, system="hi_lo",
               error_rate=0.0):
    edges = []
    evs = []

    for _ in range(trials):
        r = run_counter(num_hands=num_hands, num_decks=num_decks,
                        system=system, error_rate=error_rate)
        edges.append(r["edge_pct"])
        evs.append(r["ev_per_hand"])

    stderr = statistics.stdev(edges) / math.sqrt(trials) if trials >= 2 else 0.0

    return {
        "system": system,
        "error_rate": error_rate,
        "num_hands": num_hands,
        "num_decks": num_decks,
        "trials": trials,
        "mean_edge": statistics.mean(edges),
        "stderr_edge": stderr,
        "mean_ev": statistics.mean(evs),
        "edges": edges,
    }

if __name__ == "__main__":
    result = run_trials(trials=5, num_hands=200000, system="hi_lo", error_rate=0.0)
    print(f"system:     {result['system']}")
    print(f"mean_edge:  {result['mean_edge']:+.3f}%")
    print(f"stderr:     {result['stderr_edge']:.3f}%")
    print(f"raw edges:  {[f'{e:+.3f}' for e in result['edges']]}")

    test_rows = [
        {"system": "hi_lo", "mean_edge": 0.612, "trials": 5},
        {"system": "ko",    "mean_edge": 0.588, "trials": 5},
    ]
    save_csv(test_rows, "test.csv")
