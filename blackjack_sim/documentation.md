# Code Documentation

## `blackjack.py`

### Module Comments
Core Blackjack simulation engine.

This module provides the logic, classes, and functions required to simulate Blackjack games, apply basic strategy, implement card counting systems, and run statistical simulations to evaluate edge, ruin, and counting methods.

### Classes

#### `Card`
**Description:** Represents a standard playing card with a suit and a rank.

- `__init__(self, suit, rank)`
  - *Comment:* Initialize a card with the given suit and rank.
- `__str__(self)`
  - *Comment:* Return a string representation of the card.

#### `Shoe`
**Description:** Represents a multi-deck shoe of cards to draw from.

- `__init__(self, num_decks=6, penetration=0.75)`
  - *Comment:* Initialize the shoe with multiple standard decks and set penetration. Ensures penetration is kept within sensible limits (1% to 99%). Generates the total cards in the shoe and stores the starting size to accurately track penetration.
- `shuffle(self)`
  - *Comment:* Randomize the order of the cards currently in the shoe.
- `deal_card(self)`
  - *Comment:* Remove and return the top card from the shoe.
- `needs_reshuffle(self)`
  - *Comment:* Check if the shoe has reached its reshuffle point based on penetration. Returns True if the shoe should be reshuffled, False otherwise.
- `decks_remaining(self)`
  - *Comment:* Calculate the exact number of decks left in the shoe. Returns number of decks remaining (e.g., 2.5).

#### `Counter`
**Description:** Tracks the card counting values during the game to guide bet sizing.

- `__init__(self, system="hi_lo", num_decks=1)`
  - *Comment:* Initialize the counter based on a specific counting system. Unbalanced systems like KO start at a negative offset rather than zero.
- `observe(self, card)`
  - *Comment:* Update the running count based on the observed card's value in the system.
- `true_count(self, decks_remaining)`
  - *Comment:* Calculate the 'true count' (running count normalized by remaining decks). Clamps decks remaining to at least 0.5 to prevent dividing by tiny fractions near the very end of a shoe which would blow up the true count.
- `betting_count(self, decks_remaining)`
  - *Comment:* Determine the metric used for betting (true count for balanced, running count for unbalanced).
- `reset(self)`
  - *Comment:* Reset the running count back to its initial state for a new shoe.

### Functions

#### `hand_value(hand)`
- *Comment:* Calculate the optimal Blackjack value of a hand. Accumulates standard values and counts aces. Demotes aces from 11 to 1 if the total is over 21 (bust).

#### `_card_rank_value(card)`
- *Comment:* Get the integer value of a single card's rank for basic strategy logic. Returns 11 for Aces, 10 for face cards, and face value for others.

#### `_is_soft(hand)`
- *Comment:* Determine whether a hand is 'soft' (contains an Ace counted as 11). If there are no aces, it cannot be a soft hand. Compares the optimal hand value with the minimum "hard" total. If they differ, an Ace is currently being counted as 11, making it soft.

#### `basic_strategy(player_hand, dealer_upcard, can_double=True, can_split=True)`
- *Comment:* Determine the mathematically optimal action using S17/DAS basic strategy. Evaluates in layers: Layer 1 checks for pair splitting opportunities; Layer 2 checks for soft hand totals; Layer 3 checks for hard hand totals.

#### `play_hand(shoe)`
- *Comment:* Play out a single round of Blackjack (one dealer hand vs. one initial player hand). Returns a list of outcomes (one for each player hand created, e.g., via splits). Handles initial deals, natural blackjacks, non-splitting path (hitting, standing, doubling down), and a splitting path (queuing multiple hands, resplitting limits, playing them out, and evaluating against the dealer).

#### `bet_ramp(true_count)`
- *Comment:* Determine the bet size (in units) based on the true count (for balanced systems). Floors the true count to match strategy tables.

#### `ko_bet_ramp(running_count, _num_decks=6)`
- *Comment:* Determine the bet size for the KO (Knock-Out) unbalanced system. Thresholds anchored to KO's key count (-4) and pivot (+4) per Vancura & Fuchs, Knock-Out Blackjack.

#### `run_counter(num_hands=100000, num_decks=6, system="hi_lo", penetration=0.75, betting_policy=None, error_rate=0.0)`
- *Comment:* Simulate a series of hands while tracking counting, betting, and net profit. Initializes the required objects, reshuffles if the shoe is past the penetration limit, evaluates the count to use for betting, introduces transient misreads, and accumulates metrics based on the hand outcomes.

#### `run_ruin(bankroll=200, max_hands=10000, num_decks=6, system="hi_lo", error_rate=0.0)`
- *Comment:* Simulate risk of ruin (chances of going completely broke) with a finite bankroll. Stops if the bankroll is wiped out, goes all-in if bankroll is smaller than the desired bet, and settles the bankroll with standard payout rules.

#### `run_simulation(num_hands=10000, num_decks=6, penetration=0.75)`
- *Comment:* Run a barebones Blackjack simulation to test basic strategy outcomes without counting. Runs an isolated simulation loop without counters or bet spreading logic.

## `test_counter.py`

### Module Comments
Unit tests specifically for validating the Counter class logic. Ensures the math of the true counts, value mappings, and balanced property is behaving precisely as intended for the simulation to be valid.

### Test Checks Comments
- Verify the exact card value mappings for the Hi-Lo system. Low cards (2-6) = +1, neutral cards (7-9) = 0, high cards (10-A) = -1. Marks success or failure clearly in the console output.
- Verify the true count accurately divides running count by decks remaining. Forcibly feeds a known running count to test the arithmetic logic directly. Guard logic: tiny fractions of decks left should be clamped to 0.5.
- Ensure the reset function correctly zeroes out the running count.
- Attempting to instantiate an unknown system should immediately raise an error.

## `test_split.py`

### Module Comments
Validation script for complex hand splitting logic. Ensures the game correctly branches outcomes, caps the maximum split hands, and accurately calculates expected values when bets are multiplied by splits.

### Test Checks Comments
- Verify split hands produce multiple expected outcomes, that the hand cap (e.g. max 4 hands) is properly respected, and that no split ace 21 is improperly counted as a natural 3:2 blackjack. Manually reshuffles the shoe if running dangerously low on cards.
- Validate the cumulative house edge over a large data set. Standard rules: win pays +bet, lose loses -bet, blackjack pays +1.5x (3:2), push pays 0. Accurately utilizing the 'bet' field is critical so that doubles/splits are weighted correctly.