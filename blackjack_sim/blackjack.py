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

class Shoe :
    def __init__(self, num_decks=6):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS] * num_decks
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    

    # TEST
if __name__ == "__main__":
    # test shoe
    shoe = Shoe(6)
    print("Dealing 5 cards from a 6-deck shoe:")
    for i in range(5):
        print(f"  {shoe.deal_card()}")
    print(f"Cards remaining: {len(shoe.cards)}")

    # test hand values
    print("\nHand value tests:")

    hand1 = [Card('Hearts', '10'), Card('Spades', 'K')]
    print(f"  10 + K = {hand_value(hand1)} (expected 20)")

    hand2 = [Card('Hearts', 'A'), Card('Diamonds', '9')]
    print(f"  A + 9 = {hand_value(hand2)} (expected 20)")

    hand3 = [Card('Hearts', 'A'), Card('Clubs', '6'), Card('Diamonds', '8')]
    print(f"  A + 6 + 8 = {hand_value(hand3)} (expected 15)")

    hand4 = [Card('Hearts', 'A'), Card('Spades', 'A'), Card('Diamonds', '9')]
    print(f"  A + A + 9 = {hand_value(hand4)} (expected 21)")