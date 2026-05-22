import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from blackjack import Counter, Card, RANKS, SUITS

# KO is unbalanced, one full deck adds +4 to the running count
c = Counter("ko", num_decks=1)
print("balanced flag:", c.balanced)
print("initial count, 1 deck:", c.running_count)
for suit in SUITS:
    for rank in RANKS:
        c.observe(Card(suit, rank))
print("after one full deck:", c.running_count)
print()

# 6 deck KO starts at the offset -4*(6-1) = -20
c6 = Counter("ko", num_decks=6)
print("initial count, 6 decks:", c6.running_count)

# dealing all 6 decks brings it back up: -20 + 6*4 = +4
for _ in range(6):
    for suit in SUITS:
        for rank in RANKS:
            c6.observe(Card(suit, rank))
print("after all 6 decks:", c6.running_count)
print()

# reset goes back to the offset, not 0
c6.reset()
print("after reset, 6 decks:", c6.running_count)

# 7 is +1 in KO, the card that makes it un