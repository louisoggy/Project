import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from blackjack import run_counter

for system in ("hi_lo", "ko", "zen"):
    r = run_counter(num_hands=500000, num_decks=6, system=system)
    print(f"{system:6}  edge {r['edge_pct']:+.3f}%   "
          f"ev/hand {r['ev_per_hand']:+.4f}   "
          f"avg bet {r['total_wagered']/500000:.3f}")