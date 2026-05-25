import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from blackjack import Shoe, Counter, Card, COUNT_SYSTEMS

for decks in (1, 2, 6, 8):
    shoe = Shoe(decks)
    counter = Counter("hi_lo")
    while shoe.cards:
        counter.observe(shoe.deal_card())
    print(f"{decks}-deck shoe fully counted: running_count = {counter.running_count}")
print()

counter = Counter("hi_lo")
expected = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1,
}
all_ok = True
for rank, exp in expected.items():
    counter.running_count = 0
    counter.observe(Card('Spades', rank))
    got = counter.running_count
    mark = "OK" if got == exp else "FAIL"
    if got != exp:
        all_ok = False
    print(f"  [{mark}] {rank:<2} -> {got}")
print(f"  value mapping: {'all correct' if all_ok else 'HAS ERRORS'}")
print()

counter = Counter("hi_lo")
counter.running_count = 10
tc = counter.true_count(5.0)
print(f"running 10, 5 decks left -> true count {tc:.2f}")
tc = counter.true_count(2.0)
print(f"running 10, 2 decks left -> true count {tc:.2f}")
tc = counter.true_count(0.1)
print(f"running 10, 0.1 decks left -> true count {tc:.2f}")
print()

counter = Counter("hi_lo")
counter.observe(Card('Spades', '5'))
counter.observe(Card('Spades', '6'))
before = counter.running_count
counter.reset()
after = counter.running_count
print(f"reset: {before} -> {after}")
print()

try:
    Counter("nonsense_system")
    print("unknown system: FAIL (should have raised)")
except KeyError:
    print("unknown system: OK (raised KeyError as expected)")
