import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from blackjack import run_counter

r = run_counter(num_hands=1000000, num_decks=6, system="hi_lo")

print(f"  total_net:     {r['total_net']:.1f} units")
print(f"  total_wagered: {r['total_wagered']:.1f} units")
print(f"  ev_per_hand:   {r['ev_per_hand']:.4f} units/hand")
print(f"  edge_pct:      {r['edge_pct']:.3f}%")

avg_bet = r['total_wagered'] / 1000000
print(f"  avg wagered per hand: {avg_bet:.3f} units")

r2 = run_counter(num_hands=1000000, num_decks=6, system="hi_lo")
print(f"  run 1 edge: {r['edge_pct']:.3f}%")
print(f"  run 2 edge: {r2['edge_pct']:.3f}%")
