import random
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

COUNT_SYSTEMS = {
    "hi_lo": {
        "values": {
            '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
            '7': 0, '8': 0, '9': 0,
            '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1,
        },
        "balanced": True,
    },
    "zen": {
        "values": {
            '2': 1, '3': 1, '4': 2, '5': 2, '6': 2, '7': 1,
            '8': 0, '9': 0,
            '10': -2, 'J': -2, 'Q': -2, 'K': -2, 'A': -1,
        },
        "balanced": True,
    },
}

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
    """Returns 'hit', 'stand', 'double', or 'split' using S17/DAS basic strategy."""
    total = hand_value(player_hand)
    d = _card_rank_value(dealer_upcard)

    if can_split and len(player_hand) == 2:
        r0 = _card_rank_value(player_hand[0])
        r1 = _card_rank_value(player_hand[1])
        if r0 == r1:
            pv = r0

            if pv == 11:
                return "split"
            if pv == 10:
                return "stand"
            if pv == 9:                    # stand vs 7, 10, A; split otherwise
                return "stand" if d in (7, 10, 11) else "split"
            if pv == 8:
                return "split"
            if pv == 7:
                return "split" if 2 <= d <= 7 else "hit"
            if pv == 6:
                return "split" if 2 <= d <= 6 else "hit"
            if pv == 5:                    # never split fives; fall through to hard-10
                pass
            elif pv == 4:
                return "split" if d in (5, 6) else "hit"
            elif pv in (2, 3):
                return "split" if 2 <= d <= 7 else "hit"
            # pv == 5 falls through to hard-total logic below

    if _is_soft(player_hand):
        if total >= 19:
            return "stand"
        if total == 18:
            if 3 <= d <= 6:
                return "double" if can_double else "stand"  # fallback is stand, not hit
            if d in (2, 7, 8):
                return "stand"
            return "hit"
        if total == 17:
            return "double" if (3 <= d <= 6 and can_double) else "hit"
        if total in (15, 16):
            return "double" if (4 <= d <= 6 and can_double) else "hit"
        if total in (13, 14):
            return "double" if (5 <= d <= 6 and can_double) else "hit"
        return "hit"  # soft 12 or lower, shouldn't normally occur

    if total <= 8:
        return "hit"
    if total == 9:
        return "double" if (3 <= d <= 6 and can_double) else "hit"
    if total == 10:
        return "double" if (2 <= d <= 9 and can_double) else "hit"
    if total == 11:                        # not vs A under S17
        return "double" if (2 <= d <= 10 and can_double) else "hit"
    if total == 12:
        return "stand" if 4 <= d <= 6 else "hit"
    if total <= 16:
        return "stand" if 2 <= d <= 6 else "hit"
    return "stand"

class Shoe :
    def __init__(self, num_decks=6, penetration=0.75):
        self.penetration = max(0.01, min(0.99, penetration))
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS] * num_decks
        self.shuffle()
        self.start_size = len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def needs_reshuffle(self):
        dealt = self.start_size - len(self.cards)
        return dealt / self.start_size >= self.penetration

    @property
    def decks_remaining(self):
        return len(self.cards) / 52.0

class Counter:
    def __init__(self, system="hi_lo"):
        _system = COUNT_SYSTEMS[system]
        self._values = _system["values"]
        self.balanced = _system["balanced"]
        self.running_count = 0

    def observe(self, card):
        self.running_count += self._values[card.rank]

    def true_count(self, decks_remaining):
        dr = max(decks_remaining, 0.5)
        return self.running_count / dr

    def reset(self):
        self.running_count = 0

def play_hand(shoe):
    player_hand = [shoe.deal_card()]
    dealer_hand = [shoe.deal_card()]
    player_hand.append(shoe.deal_card())
    dealer_hand.append(shoe.deal_card())

    bet = 1.0

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
        return [{
            "result": result,
            "bet": bet,
            "player_hand": player_hand,
            "dealer_hand": dealer_hand,
            "player_total": hand_value(player_hand),
            "dealer_total": hand_value(dealer_hand)
        }]

    dealer_upcard = dealer_hand[0]

    is_pair = _card_rank_value(player_hand[0]) == _card_rank_value(player_hand[1])
    first_action = basic_strategy(player_hand, dealer_upcard, can_double=True, can_split=is_pair)

    if first_action != "split":
        doubled = False
        while True:
            can_double = len(player_hand) == 2 and not doubled
            action = basic_strategy(player_hand, dealer_upcard, can_double=can_double, can_split=False)
            if action == "hit":
                player_hand.append(shoe.deal_card())
            elif action == "double":
                bet = 2.0
                doubled = True
                player_hand.append(shoe.deal_card())
                break
            else:
                break

        if hand_value(player_hand) > 21:
            return [{
                "result": "lose",
                "bet": bet,
                "player_hand": player_hand,
                "dealer_hand": dealer_hand,
                "player_total": hand_value(player_hand),
                "dealer_total": hand_value(dealer_hand)
            }]

        while hand_value(dealer_hand) < 17:
            dealer_hand.append(shoe.deal_card())

        if hand_value(dealer_hand) > 21:
            return [{
                "result": "win",
                "bet": bet,
                "player_hand": player_hand,
                "dealer_hand": dealer_hand,
                "player_total": hand_value(player_hand),
                "dealer_total": hand_value(dealer_hand)
            }]

        player_total = hand_value(player_hand)
        dealer_total = hand_value(dealer_hand)

        if player_total > dealer_total:
            result = "win"
        elif player_total < dealer_total:
            result = "lose"
        else:
            result = "push"

        return [{
            "result": result,
            "bet": bet,
            "player_hand": player_hand,
            "dealer_hand": dealer_hand,
            "player_total": player_total,
            "dealer_total": dealer_total
        }]

    # Splitting path
    is_ace_split = player_hand[0].rank == 'A'
    total_hands = 2  # tracks running count; cap is 4 hands

    # Each entry: (cards, bet, is_split_ace)
    pending = [
        ([player_hand[0], shoe.deal_card()], 1.0, is_ace_split),
        ([player_hand[1], shoe.deal_card()], 1.0, is_ace_split),
    ]
    finished = []

    while pending:
        hand, hand_bet, split_ace = pending.pop(0)

        if split_ace:
            # split aces receive exactly one card and are done; no hit, double, or resplit
            finished.append((hand, hand_bet))
            continue

        if total_hands < 4:
            act = basic_strategy(hand, dealer_upcard, can_double=True, can_split=True)
            if act == "split":
                is_new_ace = hand[0].rank == 'A'
                total_hands += 1
                pending.append(([hand[0], shoe.deal_card()], hand_bet, is_new_ace))
                pending.append(([hand[1], shoe.deal_card()], hand_bet, is_new_ace))
                continue

        doubled = False
        while True:
            can_double = len(hand) == 2 and not doubled
            act = basic_strategy(hand, dealer_upcard, can_double=can_double, can_split=False)
            if act == "hit":
                hand.append(shoe.deal_card())
            elif act == "double":
                hand_bet = 2.0
                doubled = True
                hand.append(shoe.deal_card())
                break
            else:
                break

        finished.append((hand, hand_bet))

    # Dealer plays once against all finished player hands
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(shoe.deal_card())

    dealer_total = hand_value(dealer_hand)
    outcomes = []

    for hand, hand_bet in finished:
        player_total = hand_value(hand)
        if player_total > 21:
            result = "lose"
        elif dealer_total > 21:
            result = "win"
        elif player_total > dealer_total:
            result = "win"
        elif player_total < dealer_total:
            result = "lose"
        else:
            result = "push"

        outcomes.append({
            "result": result,
            "bet": hand_bet,
            "player_hand": hand,
            "dealer_hand": dealer_hand,
            "player_total": player_total,
            "dealer_total": dealer_total
        })

    return outcomes

def bet_ramp(true_count):
    tc = max(int(true_count), 0)
    if tc <= 1:
        return 1
    elif tc == 2:
        return 2
    elif tc == 3:
        return 4
    elif tc == 4:
        return 6
    else:
        return 8

def run_counter(num_hands=100000, num_decks=6, system="hi_lo", penetration=0.75,
                betting_policy=None):
    if betting_policy is None:
        betting_policy = bet_ramp

    shoe = Shoe(num_decks, penetration)
    counter = Counter(system)
    results = {"win": 0, "lose": 0, "push": 0, "blackjack": 0}
    true_counts = []
    total_net = 0.0
    total_wagered = 0.0

    for _ in range(num_hands):
        if shoe.needs_reshuffle():
            shoe = Shoe(num_decks, penetration)
            counter.reset()

        tc = counter.true_count(shoe.decks_remaining)
        true_counts.append(tc)
        base_bet = betting_policy(tc)

        outcomes = play_hand(shoe)

        for card in outcomes[0]["dealer_hand"]:
            counter.observe(card)
        for outcome in outcomes:
            for card in outcome["player_hand"]:
                counter.observe(card)

        for outcome in outcomes:
            results[outcome["result"]] += 1
            r = outcome["result"]
            if r == "blackjack":
                total_wagered += base_bet
                total_net += 1.5 * base_bet
            else:
                wagered = base_bet * outcome["bet"]
                total_wagered += wagered
                if r == "win":
                    total_net += wagered
                elif r == "lose":
                    total_net -= wagered

    ev_per_hand = total_net / num_hands
    edge_pct = (total_net / total_wagered * 100) if total_wagered else 0.0

    return {
        "results": results,
        "true_counts": true_counts,
        "total_net": total_net,
        "total_wagered": total_wagered,
        "ev_per_hand": ev_per_hand,
        "edge_pct": edge_pct,
    }

def run_simulation(num_hands=10000, num_decks=6, penetration=0.75):
    shoe = Shoe(num_decks, penetration)
    results = {"win": 0, "lose": 0, "push": 0, "blackjack": 0}

    for _ in range(num_hands):
        if shoe.needs_reshuffle():
            shoe = Shoe(num_decks, penetration)
        for outcome in play_hand(shoe):
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
