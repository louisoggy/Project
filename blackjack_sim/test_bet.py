# check_betting.py
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from blackjack import run_counter

# big run so the edge actually settles. bet spreading has high variance
# need a lot of hands before the number means anything
print("Running 1,000,000 hands (this will take a bit)...")
r = run_counter(num_hands=1000000, num_decks=6, system="hi_lo")

print()
print("RESULT over 1,000,000 hands:")
print(f"  total_net:     {r['total_net']:.1f} units")
print(f"  total_wagered: {r['total_wagered']:.1f} units")
print(f"  ev_per_hand:   {r['ev_per_hand']:.4f} units/hand")
print(f"  edge_pct:      {r['edge_pct']:.3f}%")
print()

# most hands bet 1 unit, only a few ramp up at high counts, so the average
# bet should sit a bit above 1. if it's way higher the ramp is firing too often
avg_bet = r['total_wagered'] / 1000000
print(f"  avg wagered per hand: {avg_bet:.3f} units  (expect ~1.1 to 1.5)")
print()

# run it again to check it's stable. if the edge is real both runs land close.
# if they swing a lot then variance is still winning and i need more hands
print("Second run for stability check...")
r2 = run_counter(num_hands=1000000, num_decks=6, system="hi_lo")
print(f"  run 1 edge: {r['edge_pct']:.3f}%")
print(f"  run 2 edge: {r2['edge_pct']:.3f}%")