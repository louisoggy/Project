import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import statistics
from blackjack import run_counter

data = run_counter(num_hands=200000, num_decks=6, system="hi_lo")
tcs = data["true_counts"]
results = data["results"]

print("CHECK 1: true count distribution")
print(f"  hands recorded: {len(tcs)}")
print(f"  mean true count: {statistics.mean(tcs):.4f}  (expect near 0)")
print(f"  stdev:           {statistics.pstdev(tcs):.4f}  (expect roughly 1.5 to 2.5)")
print(f"  min:             {min(tcs):.2f}")
print(f"  max:             {max(tcs):.2f}")
print()

# CHECK 2: spread, not all clustered at zero. Bucket the true counts.
buckets = {}
for tc in tcs:
    b = round(tc)  # nearest integer bucket
    buckets[b] = buckets.get(b, 0) + 1

print("CHECK 2: true count buckets (rounded to nearest int)")
for b in sorted(buckets):
    pct = buckets[b] / len(tcs) * 100
    bar = "#" * int(pct)
    print(f"  {b:>3}: {pct:5.2f}%  {bar}")
print()

# CHECK 3: results still look like a normal game
total = sum(results.values())
print("CHECK 3: outcome breakdown (sanity)")
for k, v in results.items():
    print(f"  {k:<10} {v:>8}  ({v/total*100:.2f}%)")