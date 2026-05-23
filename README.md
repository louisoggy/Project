# Investigation and Simulation of Card Counting Methods in Blackjack

A Monte Carlo blackjack simulator used to compare three card counting systems (Hi-Lo, KO, Zen) on profitability, robustness to player error, and risk of ruin.


## Requirements

- Python 3 (developed on 3.14)
- `matplotlib` and `pandas` — only needed for generating plots

```
python -m pip install matplotlib pandas
```

## How to run

The main entry point is `blackjack_sim/main.py`:

```
python blackjack_sim/main.py
```

This opens a numbered menu:

| Option | Description |
|--------|-------------|
| 1 | **Run simulation** — plays hands with basic strategy and a flat bet, no counting (used to validate the engine) |
| 2 | **Watch a hand** — deals and displays a single hand |
| 3 | **Configure** — set the number of hands and decks used by option 1 |
| 4 | **Perfect play simulation** — compares the three systems' edge under perfect counting, saves a CSV |
| 5 | **Error robustness simulation** — sweeps each system across a range of player count error rates, saves a CSV |
| 6 | **Risk of ruin simulation** — measures how often each system goes broke across several starting bankrolls, saves a CSV |
| 7 | **Generate plots** — reads the result CSVs and writes PNG figures |
| 8 | **Quit** |

Options 4–6 prompt for their parameters (trials, hands per trial, etc.) before running — press Enter to accept the defaults. The experiments can take several minutes.

## File structure

```
blackjack_sim/
├── blackjack.py       core simulator: cards, shoe, hand values, basic strategy,
│                      counting systems and Counter class, betting ramps, and the
│                      simulation functions (run_simulation, run_counter, run_ruin)
├── main.py            menu-driven interface — the entry point
├── experiments.py     the three experiment functions, the run_trials averaging
│                      harness, and the CSV writing helper
├── plots.py           reads result CSVs and generates figures via matplotlib
│
├── test_strategy.py   52 basic strategy cases covering splits, soft hands, and hard totals
├── test_counter.py    unit tests for the Counter class
├── test_bet.py        unit tests for bet_ramp and ko_bet_ramp
├── test_double.py     validation of double-down decisions
├── test_split.py      validation of split hand logic
├── test_ko.py         KO system counting validation
├── test_zen.py        Zen system counting validation
├── test_ruin.py       validation of run_ruin
├── check_systems.py       sanity checks on the counting system definitions
├── count_distribution.py  samples the true/running count distribution across a shoe
│
├── results/           CSV output from the experiments
├── figures/           PNG figures produced by plots.py
└── devlog.txt         development log kept throughout the project
```

## Rule set

All simulations use the following fixed rules:

- Six decks by default
- Dealer stands on all 17s (S17)
- Double after split allowed (DAS)
- Double on any two cards
- Resplit up to four hands
- Split aces receive one card only
- Blackjack pays 3:2
- Dealer peeks for blackjack
- 75% deck penetration before reshuffle

## Counting systems

- **Hi-Lo** — balanced, level 1; true count used for betting
- **KO (Knock-Out)** — unbalanced, level 1; bets off the running count with a starting offset that accounts for deck size
- **Zen** — balanced, multi-level (2,3,7 = +1; 4,5,6 = +2; 8,9 = 0; 10–K = −2; A = −1); true count used for betting
