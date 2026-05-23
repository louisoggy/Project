import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import csv
import math
import statistics
from blackjack import run_counter, run_ruin

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

def perfect_play_simulation(trials=20, num_hands=500000, num_decks=6):
    rows = []
    for system in ("hi_lo", "ko", "zen"):
        r = run_trials(trials=trials, num_hands=num_hands,
                       num_decks=num_decks, system=system, error_rate=0.0)

        edge_stdev = statistics.stdev(r["edges"]) if trials >= 2 else 0.0

        row = {
            "system":     system,
            "mean_edge":  r["mean_edge"],
            "stderr_edge": r["stderr_edge"],
            "mean_ev":    r["mean_ev"],
            "edge_stdev": edge_stdev,
            "trials":     trials,
            "num_hands":  num_hands,
            "num_decks":  num_decks,
        }
        rows.append(row)
        print(f"  {system:6s}  mean_edge={row['mean_edge']:+.3f}%  "
              f"stderr={row['stderr_edge']:.3f}%  stdev={edge_stdev:.3f}%")

    save_csv(rows, "perfect_play_simulation.csv")
    return rows


def err_robustness_simulation(trials=20, num_hands=500000, num_decks=6):
    error_rates = (0.0, 0.02, 0.10, 0.25, 0.50)
    rows = []

    for system in ("hi_lo", "ko", "zen"):
        for error_rate in error_rates:
            r = run_trials(trials=trials, num_hands=num_hands,
                           num_decks=num_decks, system=system,
                           error_rate=error_rate)

            row = {
                "system":      system,
                "error_rate":  error_rate,
                "mean_edge":   r["mean_edge"],
                "stderr_edge": r["stderr_edge"],
                "mean_ev":     r["mean_ev"],
                "trials":      trials,
                "num_hands":   num_hands,
                "num_decks":   num_decks,
            }
            rows.append(row)
            print(f"  {system:6s}  error={error_rate:.0%}  "
                  f"mean_edge={row['mean_edge']:+.3f}%  stderr={row['stderr_edge']:.3f}%")

    save_csv(rows, "err_robustness_simulation.csv")
    return rows


def ruin_simulation(trials=200, bankrolls=(100, 200, 400, 800),
                    max_hands=10000, num_decks=6):
    rows = []

    for system in ("hi_lo", "ko", "zen"):
        for bankroll in bankrolls:
            broke_count = 0
            hands_totals = []

            for _ in range(trials):
                r = run_ruin(bankroll=bankroll, max_hands=max_hands,
                             num_decks=num_decks, system=system, error_rate=0.0)
                if r["broke"]:
                    broke_count += 1
                hands_totals.append(r["hands_played"])

            row = {
                "system":           system,
                "bankroll":         bankroll,
                "broke_rate":       broke_count / trials,
                "avg_hands_played": statistics.mean(hands_totals),
                "trials":           trials,
                "max_hands":        max_hands,
                "num_decks":        num_decks,
            }
            rows.append(row)
            print(f"  {system:6s}  bankroll={bankroll:4d}  "
                  f"broke={row['broke_rate']:.1%}  "
                  f"avg_hands={row['avg_hands_played']:.0f}")

    save_csv(rows, "ruin_simulation.csv")
    return rows


if __name__ == "__main__":
    # perfect_play_simulation()
    # err_robustness_simulation()
    print("Ruin simulation: risk of ruin by system and starting bankroll")
    ruin_simulation()
