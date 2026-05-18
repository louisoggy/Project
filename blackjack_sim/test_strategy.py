import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from blackjack import Card, basic_strategy

def C(rank, suit='Spades'):
    return Card(suit, rank)

cases = [
    # (description, hand, dealer_upcard, expected_action, can_double, can_split)

    # --- PAIRS ---
    ("A,A vs 5",        [C('A'), C('A')],  C('5'),  "split",   True, True),
    ("A,A vs 10",       [C('A'), C('A')],  C('10'), "split",   True, True),
    ("10,10 vs 6",      [C('10'), C('K')], C('6'),  "stand",   True, True),
    ("9,9 vs 7",        [C('9'), C('9')],  C('7'),  "stand",   True, True),
    ("9,9 vs 9",        [C('9'), C('9')],  C('9'),  "split",   True, True),
    ("9,9 vs 10",       [C('9'), C('9')],  C('10'), "stand",   True, True),
    ("9,9 vs A",        [C('9'), C('9')],  C('A'),  "stand",   True, True),
    ("8,8 vs A",        [C('8'), C('8')],  C('A'),  "split",   True, True),
    ("8,8 vs 10",       [C('8'), C('8')],  C('10'), "split",   True, True),
    ("7,7 vs 7",        [C('7'), C('7')],  C('7'),  "split",   True, True),
    ("7,7 vs 8",        [C('7'), C('7')],  C('8'),  "hit",     True, True),
    ("6,6 vs 2",        [C('6'), C('6')],  C('2'),  "split",   True, True),
    ("6,6 vs 7",        [C('6'), C('6')],  C('7'),  "hit",     True, True),
    ("5,5 vs 5",        [C('5'), C('5')],  C('5'),  "double",  True, True),
    ("5,5 vs 10",       [C('5'), C('5')],  C('10'), "hit",     True, True),
    ("4,4 vs 5",        [C('4'), C('4')],  C('5'),  "split",   True, True),
    ("4,4 vs 4",        [C('4'), C('4')],  C('4'),  "hit",     True, True),
    ("3,3 vs 4",        [C('3'), C('3')],  C('4'),  "split",   True, True),
    ("2,2 vs 8",        [C('2'), C('2')],  C('8'),  "hit",     True, True),
    ("J,Q vs 6",        [C('J'), C('Q')],  C('6'),  "stand",   True, True),

    # --- SOFT ---
    ("A,2 vs 5",        [C('A'), C('2')],  C('5'),  "double",  True, True),
    ("A,2 vs 4",        [C('A'), C('2')],  C('4'),  "hit",     True, True),
    ("A,4 vs 4",        [C('A'), C('4')],  C('4'),  "double",  True, True),
    ("A,4 vs 3",        [C('A'), C('4')],  C('3'),  "hit",     True, True),
    ("A,6 vs 3",        [C('A'), C('6')],  C('3'),  "double",  True, True),
    ("A,6 vs 7",        [C('A'), C('6')],  C('7'),  "hit",     True, True),
    ("A,7 vs 2",        [C('A'), C('7')],  C('2'),  "stand",   True, True),
    ("A,7 vs 3",        [C('A'), C('7')],  C('3'),  "double",  True, True),
    ("A,7 vs 8",        [C('A'), C('7')],  C('8'),  "stand",   True, True),
    ("A,7 vs 9",        [C('A'), C('7')],  C('9'),  "hit",     True, True),
    ("A,7 vs A",        [C('A'), C('7')],  C('A'),  "hit",     True, True),
    ("A,8 vs 6",        [C('A'), C('8')],  C('6'),  "stand",   True, True),
    ("A,9 vs 6",        [C('A'), C('9')],  C('6'),  "stand",   True, True),

    # --- HARD ---
    ("5+2 vs 6",        [C('5'), C('2')],  C('6'),  "hit",     True, True),
    ("4+5 vs 3",        [C('4'), C('5')],  C('3'),  "double",  True, True),
    ("4+5 vs 2",        [C('4'), C('5')],  C('2'),  "hit",     True, True),
    ("6+4 vs 9",        [C('6'), C('4')],  C('9'),  "double",  True, True),
    ("6+4 vs 10",       [C('6'), C('4')],  C('10'), "hit",     True, True),
    ("7+4 vs 10",       [C('7'), C('4')],  C('10'), "double",  True, True),
    ("7+4 vs A",        [C('7'), C('4')],  C('A'),  "hit",     True, True),
    ("10+2 vs 3",       [C('10'), C('2')], C('3'),  "hit",     True, True),
    ("10+2 vs 4",       [C('10'), C('2')], C('4'),  "stand",   True, True),
    ("10+3 vs 2",       [C('10'), C('3')], C('2'),  "stand",   True, True),
    ("10+6 vs 6",       [C('10'), C('6')], C('6'),  "stand",   True, True),
    ("10+6 vs 7",       [C('10'), C('6')], C('7'),  "hit",     True, True),
    ("10+6 vs 10",      [C('10'), C('6')], C('10'), "hit",     True, True),
    ("10+7 vs A",       [C('10'), C('7')], C('A'),  "stand",   True, True),

    # --- FLAG BEHAVIOUR ---
    ("A,A vs 5 no-split",  [C('A'), C('A')], C('5'),  "hit",   True, False),
    ("8,8 vs 5 no-split",  [C('8'), C('8')], C('5'),  "stand", True, False),
    ("9 vs 3 no-double",   [C('4'), C('5')], C('3'),  "hit",   False, True),
    ("11 vs 10 no-double", [C('7'), C('4')], C('10'), "hit",   False, True),
    ("A,7 vs 3 no-double", [C('A'), C('7')], C('3'),  "stand", False, True),
]

print("Basic strategy tests:")
print("-" * 60)
passed = 0
failed = 0
for desc, hand, upcard, expected, cd, cs in cases:
    actual = basic_strategy(hand, upcard, can_double=cd, can_split=cs)
    ok = actual == expected
    marker = "OK " if ok else "FAIL"
    print(f"  [{marker}] {desc:<25} expected={expected:<6} actual={actual}")
    if ok:
        passed += 1
    else:
        failed += 1
print("-" * 60)
print(f"  {passed} passed, {failed} failed")