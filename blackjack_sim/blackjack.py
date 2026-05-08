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

def basic_strategy(player_hand, dealer_upcard):
    total = hand_value(player_hand)
    d = _card_rank_value(dealer_upcard)

    if _is_soft(player_hand):
        if total <= 17:
            return "hit"
        elif total == 18:
            return "hit" if d >= 9 else "stand"
        else:
            return "stand"
    else:
        if total <= 11:
            return "hit"
        elif total == 12:
            return "stand" if 4 <= d <= 6 else "hit"
        elif total <= 16:
            return "stand" if d <= 6 else "hit"
        else:
            return "stand"

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