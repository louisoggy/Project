# test_counter.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from blackjack import Shoe, Counter, Card, COUNT_SYSTEMS

# CHECK 1: Hi-Lo is balanced, so a complete shoe must count to exactly 0.
# Observe every card in a fresh shoe and the running count must end at 0.
for decks in (1, 2, 6, 8):
    shoe = Shoe(decks)
    counter = Counter("hi_lo")
    while shoe.cards:
        counter.observe(shoe.deal_card())
    print(f"{decks}-deck shoe fully counted: running_count = {counter.running_count}  (must be 0)")
print()

# CHECK 2: value mapping is exactly right for Hi-Lo.
# low cards 2 to 6 = +1, neutral 7 to 9 = 0, high 10/J/Q/K/A = -1
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
    print(f"  [{mark}] {rank:<2} -> {got}  (expected {exp})")
print(f"  value mapping: {'all correct' if all_ok else 'HAS ERRORS'}")
print()

# CHECK 3: true count divides running count by decks remaining.
# Feed a known running count, check the division.
counter = Counter("hi_lo")
counter.running_count = 10
# with 5 decks left, true count should be 10 / 5 = 2.0
tc = counter.true_count(5.0)
print(f"running 10, 5 decks left -> true count {tc:.2f}  (expect 2.00)")
# with 2 decks left, 10 / 2 = 5.0
tc = counter.true_count(2.0)
print(f"running 10, 2 decks left -> true count {tc:.2f}  (expect 5.00)")
# guard: tiny decks remaining should be clamped to 0.5, so 10 / 0.5 = 20
tc = counter.true_count(0.1)
print(f"running 10, 0.1 decks left -> true count {tc:.2f}  (expect 20.00, clamped)")
print()

# CHECK 4: reset zeroes the running count.
counter = Counter("hi_lo")
counter.observe(Card('Spades', '5'))
counter.observe(Card('Spades', '6'))
before = counter.running_count
counter.reset()
after = counter.running_count
print(f"reset: {before} -> {after}  (expect 2 -> 0)")
print()

# CHECK 5: unknown system raises immediately.
try:
    Counter("nonsense_system")
    print("unknown system: FAIL (should have raised)")
except KeyError:
    print("unknown system: OK (raised KeyError as expected)")