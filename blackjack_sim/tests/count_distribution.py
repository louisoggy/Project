import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import statistics
from blackjack import run_counter

data = run_counter(num_hands=200000, num_decks=6, system="hi_lo")
tcs = data["true_counts"]
results = data["results"]

print(f"  hands recorded: {len(tcs)}")
print(f"  mean true count: {statistics.mean(tcs):.4f}")
print(f"  stdev:           {statistics.pstdev(tcs):.4f}")
print(f"  min:             {min(tcs):.2f}")
print(f"  max:             {max(tcs):.2f}")
print()

buckets = {}
for tc in tcs:
    b = round(tc)
    buckets[b] = buckets.get(b, 0) + 1

for b in sorted(buckets):
    pct = buckets[b] / len(tcs) * 100
    bar = "#" * int(pct)
    print(f"  {b:>3}: {pct:5.2f}%  {bar}")
print()

total = sum(results.values())
for k, v in results.items():
    print(f"  {k:<10} {v:>8}  ({v/total*100:.2f}%)")
