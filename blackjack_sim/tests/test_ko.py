import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from blackjack import Counter, Card, RANKS, SUITS, ko_bet_ramp

c = Counter("ko", num_decks=1)
print("balanced flag:", c.balanced)
print("initial count, 1 deck:", c.running_count)
for suit in SUITS:
    for rank in RANKS:
        c.observe(Card(suit, rank))
print("after one full deck:", c.running_count)
print()

c6 = Counter("ko", num_decks=6)
print("initial count, 6 decks:", c6.running_count)

for _ in range(6):
    for suit in SUITS:
        for rank in RANKS:
            c6.observe(Card(suit, rank))
print("after all 6 decks:", c6.running_count)
print()

c6.reset()
print("after reset, 6 decks:", c6.running_count)

c7 = Counter("ko", num_decks=1)
c7.running_count = 0
c7.observe(Card('Spades', '7'))
print("7 maps to:", c7.running_count)
print()

for rc in range(-8, 9):
    print(f"running count {rc:>3} -> bet {ko_bet_ramp(rc, 6)}")