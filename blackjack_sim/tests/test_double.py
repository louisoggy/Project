import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from blackjack import Shoe, play_hand

shoe = Shoe(6)
doubled = 0
naturals = 0
total_played = 0

for _ in range(10000):
    if len(shoe.cards) < 20:
        shoe = Shoe(6)
    outcomes = play_hand(shoe)
    total_played += 1
    if any(o["bet"] == 2.0 for o in outcomes):
        doubled += 1
    if any(o["result"] == "blackjack" for o in outcomes):
        naturals += 1

print(f"Played:   {total_played}")
print(f"Doubled:  {doubled}  ({doubled/total_played*100:.2f}%)")
print(f"Naturals: {naturals}  ({naturals/total_played*100:.2f}%)")