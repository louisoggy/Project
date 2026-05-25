import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from blackjack import Shoe, play_hand, hand_value, Card

shoe = Shoe(6)
multi_hand_count = 0
total_starting_hands = 0
max_hands_seen = 0
blackjack_count = 0

for _ in range(50000):
    if len(shoe.cards) < 20:
        shoe = Shoe(6)
    outcomes = play_hand(shoe)
    total_starting_hands += 1

    if len(outcomes) > 1:
        multi_hand_count += 1
    max_hands_seen = max(max_hands_seen, len(outcomes))

    for o in outcomes:
        if o["result"] == "blackjack":
            blackjack_count += 1

print(f"Starting hands:      {total_starting_hands}")
print(f"Multi-hand (split):  {multi_hand_count}  ({multi_hand_count/total_starting_hands*100:.2f}%)")
print(f"Max hands from one split: {max_hands_seen}")
print(f"Blackjack results:   {blackjack_count}  ({blackjack_count/total_starting_hands*100:.2f}%)")
print()

shoe = Shoe(6)
net = 0.0
wagered = 0.0
n = 500000
for _ in range(n):
    if len(shoe.cards) < 20:
        shoe = Shoe(6)
    for o in play_hand(shoe):
        b = o["bet"]
        wagered += b
        if o["result"] == "win":
            net += b
        elif o["result"] == "lose":
            net -= b
        elif o["result"] == "blackjack":
            net += 1.5

edge = -net / wagered * 100
print(f"Hands played:  {n}")
print(f"Net units:     {net:.1f}")
print(f"Total wagered: {wagered:.1f}")
print(f"House edge:    {edge:.3f}%")
