import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from blackjack import run_simulation, play_hand, Shoe
from experiments import perfect_play_simulation, err_robustness_simulation, ruin_simulation
from blackjack_sim.plots import generate_all

DEFAULT_HANDS = 100000
DEFAULT_DECKS = 6

# experiment defaults - session values are initialised from here in main()
PP_TRIALS       = 20
PP_HANDS        = 500000
ERR_TRIALS      = 20
ERR_HANDS       = 500000
ERR_RATES       = [0.0, 0.02, 0.10, 0.25, 0.50]   # note: not yet a parameter of err_robustness_simulation
RUIN_TRIALS     = 200
RUIN_BANKROLLS  = [100, 200, 400, 800]
RUIN_MAX_HANDS  = 10000


def sep():
    print("-" * 35)


# input helpers
def _prompt_int(label, current):
    val = input(f"  {label} [{current}]: ").strip()
    if val:
        try:
            return int(val)
        except ValueError:
            print("  Invalid, keeping current.")
    return current


def _prompt_intlist(label, current):
    display = ", ".join(str(x) for x in current)
    val = input(f"  {label} [{display}]: ").strip()
    if val:
        try:
            return [int(x.strip()) for x in val.split(",")]
        except ValueError:
            print("  Invalid, keeping current.")
    return current


def _prompt_floatlist(label, current):
    display = ", ".join(str(x) for x in current)
    val = input(f"  {label} [{display}]: ").strip()
    if val:
        try:
            return [float(x.strip()) for x in val.split(",")]
        except ValueError:
            print("  Invalid, keeping current.")
    return current


# menu and display

def main_menu():
    print("\n=== BLACKJACK SIMULATOR ===")
    sep()
    print("  1. Run simulation")
    print("  2. Watch a hand")
    print("  3. Configure")
    print("  4. Perfect play simulation")
    print("  5. Error robustness simulation")
    print("  6. Risk of ruin simulation")
    print("  7. Generate plots")
    print("  8. Quit")
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

    # session local experiment settings, initialised from module defaults
    pp_trials      = PP_TRIALS
    pp_hands       = PP_HANDS
    err_trials     = ERR_TRIALS
    err_hands      = ERR_HANDS
    ruin_trials    = RUIN_TRIALS
    ruin_bankrolls = list(RUIN_BANKROLLS)
    ruin_max_hands = RUIN_MAX_HANDS

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
            sep()
            pp_trials = _prompt_int("Trials", pp_trials)
            pp_hands  = _prompt_int("Hands per trial", pp_hands)
            sep()
            print("Running... this may take several minutes.")
            perfect_play_simulation(trials=pp_trials, num_hands=pp_hands, num_decks=num_decks)
            print("Saved to the results folder.")

        elif choice == "5":
            sep()
            err_trials = _prompt_int("Trials", err_trials)
            err_hands  = _prompt_int("Hands per trial", err_hands)
            sep()
            print("Running... this may take several minutes.")
            err_robustness_simulation(trials=err_trials, num_hands=err_hands, num_decks=num_decks)
            print("Saved to the results folder.")

        elif choice == "6":
            sep()
            ruin_trials    = _prompt_int("Trials", ruin_trials)
            ruin_bankrolls = _prompt_intlist("Bankrolls: ',' separated", ruin_bankrolls)
            ruin_max_hands = _prompt_int("Max hands per trial", ruin_max_hands)
            sep()
            print("Running... this may take several minutes.")
            ruin_simulation(trials=ruin_trials, bankrolls=ruin_bankrolls,
                            max_hands=ruin_max_hands, num_decks=num_decks)
            print("Saved to the results folder.")

        elif choice == "7":
            print("Generating plots...")
            generate_all()
            print("Figures saved to the figures folder.")

        elif choice == "8":
            print("Quit simulator")
            break

        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
