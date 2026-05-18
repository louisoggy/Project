import random
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

class Card :
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
def hand_value(hand):
    value = 0
    aces = 0

    for card in hand:
        if card.rank in ['J', 'Q', 'K']:
            value += 10
        elif card.rank == 'A':
            aces += 1
            value += 11
        else:
            value += int(card.rank)

    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value

def _card_rank_value(card):
    if card.rank in ['J', 'Q', 'K']:
        return 10
    elif card.rank == 'A':
        return 11
    else:
        return int(card.rank)

def _is_soft(hand):
    if not any(c.rank == 'A' for c in hand):
        return False
    hard_total = sum(1 if c.rank == 'A' else _card_rank_value(c) for c in hand)
    return hand_value(hand) != hard_total

def basic_strategy(player_hand, dealer_upcard, can_double=True, can_split=True):
    """
    Standard S17/DAS basic strategy. Returns "hit", "stand", "double", or "split".
    Priority: pairs -> soft totals -> hard totals.
    can_double / can_split let the caller disable actions that aren't legal.
    """
    total = hand_value(player_hand)
    d = _card_rank_value(dealer_upcard)  # 2-9 face value, 10/J/Q/K=10, A=11

    # ------------------------------------------------------------------
    # 1. PAIRS
    # ------------------------------------------------------------------
    # Pair detection: exactly two cards, same 10-value rank (10/J/Q/K all count as 10)
    if can_split and len(player_hand) == 2:
        r0 = _card_rank_value(player_hand[0])
        r1 = _card_rank_value(player_hand[1])
        if r0 == r1:
            pv = r0  # pair value (2-11)

            if pv == 11:                   # A,A -> always split
                return "split"
            if pv == 10:                   # 10,10 -> never split
                return "stand"
            if pv == 9:                    # 9,9 -> stand vs 7, 10, A
                return "stand" if d in (7, 10, 11) else "split"
            if pv == 8:                    # 8,8 -> always split
                return "split"
            if pv == 7:                    # 7,7 -> split vs 2-7
                return "split" if 2 <= d <= 7 else "hit"
            if pv == 6:                    # 6,6 -> split vs 2-6
                return "split" if 2 <= d <= 6 else "hit"
            if pv == 5:                    # 5,5 -> never split; fall through to hard-10
                pass
            elif pv == 4:                  # 4,4 -> split vs 5-6 (DAS) only
                return "split" if d in (5, 6) else "hit"
            elif pv in (2, 3):             # 2,2 / 3,3 -> split vs 2-7
                return "split" if 2 <= d <= 7 else "hit"
            # pv == 5 falls through to hard-total logic below

    # ------------------------------------------------------------------
    # 2. SOFT TOTALS  (hand contains an ace counted as 11)
    # ------------------------------------------------------------------
    if _is_soft(player_hand):
        if total >= 19:                    # soft 19+ -> always stand
            return "stand"
        if total == 18:                    # soft 18 (A,7)
            if 3 <= d <= 6:
                return "double" if can_double else "stand"  # double or stand
            if d in (2, 7, 8):
                return "stand"
            return "hit"                   # vs 9, 10, A
        if total == 17:                    # soft 17 (A,6) -> double vs 3-6
            return "double" if (3 <= d <= 6 and can_double) else "hit"
        if total in (15, 16):              # soft 15-16 (A,4 / A,5) -> double vs 4-6
            return "double" if (4 <= d <= 6 and can_double) else "hit"
        if total in (13, 14):              # soft 13-14 (A,2 / A,3) -> double vs 5-6
            return "double" if (5 <= d <= 6 and can_double) else "hit"
        return "hit"                       # soft 12 or lower (shouldn't normally occur)

    # ------------------------------------------------------------------
    # 3. HARD TOTALS
    # ------------------------------------------------------------------
    if total <= 8:                         # 5-8 -> always hit
        return "hit"
    if total == 9:                         # double vs 3-6, else hit
        return "double" if (3 <= d <= 6 and can_double) else "hit"
    if total == 10:                        # double vs 2-9, else hit
        return "double" if (2 <= d <= 9 and can_double) else "hit"
    if total == 11:                        # double vs 2-10 (not vs A under S17)
        return "double" if (2 <= d <= 10 and can_double) else "hit"
    if total == 12:                        # stand vs 4-6, else hit
        return "stand" if 4 <= d <= 6 else "hit"
    if total <= 16:                        # 13-16 -> stand vs 2-6, else hit
        return "stand" if 2 <= d <= 6 else "hit"
    return "stand"                         # 17+ -> always stand

class Shoe :
    def __init__(self, num_decks=6):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS] * num_decks
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

def play_hand(shoe):
    player_hand = [shoe.deal_card()]
    dealer_hand = [shoe.deal_card()]
    player_hand.append(shoe.deal_card())
    dealer_hand.append(shoe.deal_card())

    player_total = hand_value(player_hand)
    dealer_total = hand_value(dealer_hand)

    player_blackjack = player_total == 21
    dealer_blackjack = dealer_total == 21

    if player_blackjack or dealer_blackjack:
        if player_blackjack and dealer_blackjack:
            result = "push"
        elif player_blackjack:
            result = "blackjack"
        else:
            result = "lose"
        return {
            "result": result,
            "player_hand": player_hand,
            "dealer_hand": dealer_hand,
            "player_total": hand_value(player_hand),
            "dealer_total": hand_value(dealer_hand)
        }

    dealer_upcard = dealer_hand[0]
    while basic_strategy(player_hand, dealer_upcard) == "hit":
        player_hand.append(shoe.deal_card())

    if hand_value(player_hand) > 21:
        return {
            "result": "lose",
            "player_hand": player_hand,
            "dealer_hand": dealer_hand,
            "player_total": hand_value(player_hand),
            "dealer_total": hand_value(dealer_hand)
        }

    while hand_value(dealer_hand) < 17:
        dealer_hand.append(shoe.deal_card())

    if hand_value(dealer_hand) > 21:
        return {
            "result": "win",
            "player_hand": player_hand,
            "dealer_hand": dealer_hand,
            "player_total": hand_value(player_hand),
            "dealer_total": hand_value(dealer_hand)
        }
    
    player_total = hand_value(player_hand)
    dealer_total = hand_value(dealer_hand)

    if player_total > dealer_total:
        result = "win"
    elif player_total < dealer_total:
        result = "lose"
    else:
        result = "push"

    return {
        "result": result,
        "player_hand": player_hand,
        "dealer_hand": dealer_hand,
        "player_total": player_total,
        "dealer_total": dealer_total
    }

def run_simulation(num_hands=10000, num_decks=6):
    shoe = Shoe(num_decks)
    results = {"win": 0, "lose": 0, "push": 0, "blackjack": 0}

    for i in range(num_hands):
        if len(shoe.cards) < 20:
            shoe = Shoe(num_decks)
        outcome = play_hand(shoe)
        results[outcome["result"]] += 1

    return results

if __name__ == "__main__":
    num_hands = 100000
    print(f"Simulating {num_hands} hands...\n")
    results = run_simulation(num_hands)

    for result, count in results.items():
        print(f"  {result}: {count} ({count/num_hands*100:.2f}%)")

    wins = results["win"] + results["blackjack"]
    losses = results["lose"]
    print(f"\n  Overall win rate: {wins/num_hands*100:.2f}%")
    print(f"  Overall lose rate: {losses/num_hands*100:.2f}%")