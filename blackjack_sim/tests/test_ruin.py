import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from blackjack import run_ruin

# small bankroll should go broke often, large bankroll rarely.
# run a batch of trials for each and report the broke rate.
for bankroll in (50, 100, 200, 500):
    trials = 200
    broke = 0
    survived_hands = []
    for _ in range(trials):
        r = run_ruin(bankroll=bankroll, max_hands=10000, system="hi_lo")
        if r["broke"]:
            broke += 1
        survived_hands.append(r["hands_played"])
    print(f"bankroll {bankroll:>4}u  ->  broke {broke/trials*100:5.1f}%   "
          f"avg hands played {sum(survived_hands)/trials:.0f}")