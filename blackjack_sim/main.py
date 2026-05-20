import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from blackjack import run_simulation, play_hand, Shoe

DEFAULT_HANDS = 100000
DEFAULT_DECKS = 6

def sep():
    print("-" * 35)

def main_menu():
    print("\n=== BLACKJACK SIMULATOR ===")
    sep()
    print("  1. Run simulation")
    print("  2. Watch a hand")
    print("  3. Configure")
    print("  4. Quit")
    sep()

def show_results(results, num_hands):
    print(f"\nResults ({num_hands:,} hands):")
    sep()
    for outcome, count in results.items():
        print(f"  {outcome:<10} {count:>7,}  ({count / num_hands * 100:.2f}%)")
    sep()
    wins = results["win"] + results["blackjack"]
    losses = results["lose"]
    print(f"  Win rate:  {wins / num_hands * 100:.2f}%")
    print(f"  Lose rate: {losses / num_hands * 100:.2f}%")

def watch_hand(num_decks):
    shoe = Shoe(num_decks)
    outcomes = play_hand(shoe)
    print("\n--- Hand ---")
    first = outcomes[0]
    print(f"  Dealer: {', '.join(str(c) for c in first['dealer_hand'])} = {first['dealer_total']}")
    sep()
    for i, o in enumerate(outcomes):
        label = f"  Hand {i + 1}: " if len(outcomes) > 1 else "  Player: "
        bet_note = f"  (bet: {o['bet']:.0f})" if o['bet'] != 1.0 else ""
        print(f"{label}{', '.join(str(c) for c in o['player_hand'])} = {o['player_total']}{bet_note}")
        print(f"  Result: {o['result'].upper()}")

def configure_menu(num_hands, num_decks):
    print(f"\nCurrent settings:")
    print(f"  Hands : {num_hands:,}")
    print(f"  Decks : {num_decks}")
    sep()
    val = input(f"  Hands [{num_hands}]: ").strip()
    if val:
        try:
            num_hands = int(val)
        except ValueError:
            print("  Invalid, keeping current.")
    val = input(f"  Decks [{num_decks}]: ").strip()
    if val:
        try:
            num_decks = int(val)
        except ValueError:
            print("  Invalid, keeping current.")
    return num_hands, num_decks

def main():
    num_hands = DEFAULT_HANDS
    num_decks = DEFAULT_DECKS

    while True:
        main_menu()
        choice = input("  > ").strip()

        if choice == "1":
            print(f"\nSimulating {num_hands:,} hands:")
            results = run_simulation(num_hands, num_decks)
            show_results(results, num_hands)
        elif choice == "2":
            watch_hand(num_decks)
        elif choice == "3":
            num_hands, num_decks = configure_menu(num_hands, num_decks)
            print("  Settings updated.")
        elif choice == "4":
            print("Quit simulator")
            break
        else:
            print("  Invalid option.")

if __name__ == "__main__":
    main()