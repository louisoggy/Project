import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from blackjack import Counter, Card, RANKS, SUITS

c = Counter("zen")
print("balanced flag:", c.balanced)

# zen is balanced so a full deck must sum to 0
for suit in SUITS:
    for rank in RANKS:
        c.observe(Card(suit, rank))
print("running count after full deck:", c.running_count, "(must be 0)")

# spot check a few values
c2 = Counter("zen")
for rank, exp in [('4', 2), ('6', 2), ('7', 1), ('10', -2), ('A', -1), ('8', 0)]:
    c2.running_count = 0
    c2.observe(Card('Spades', rank))
    mark = "OK" if c2.running_count == exp else "FAIL"
    print(f"  {rank:<2} -> {c2.running_count}  (expect {exp})  {mark}")