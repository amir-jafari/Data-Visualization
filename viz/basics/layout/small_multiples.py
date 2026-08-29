"""
Small multiples -- many small charts instead of one crowded one.

Ten lines on one chart is a plate of spaghetti. Ten small charts, drawn the
same way on the same scales, can be compared at a glance because the eye only
has to spot the difference in SHAPE.

What it shows:
    * the spaghetti chart, and the same data as a grid
    * the two rules that make it work: identical scales, and a sensible order
    * a grey "all the others" ghost behind each panel, for context

Run it:
    python viz/basics/layout/small_multiples.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save                              # noqa: E402

# Twelve series with different behaviours, so the grid has something to show.
rng = np.random.default_rng(3)
months = np.arange(24)
names = [f"store {i:02d}" for i in range(1, 13)]
trends = rng.uniform(-1.2, 2.0, 12)
series = {name: 50 + trend * months + rng.normal(0, 3, 24)
          for name, trend in zip(names, trends)}

# --- 1. spaghetti ----------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.5))
for name, values in series.items():
    ax.plot(months, values, lw=1.5, label=name)
ax.legend(fontsize=6, ncol=3)
ax.set_title("Twelve series on one chart: which store is falling?")
fig.tight_layout()
save(fig, __file__, "spaghetti")

# --- 2. small multiples, done properly -------------------------------------
# Rule 1: every panel on the SAME scale, or the shapes are not comparable.
# Rule 2: order by something meaningful -- here, by trend. Alphabetical
#         ordering throws away a free layer of information.
low = min(v.min() for v in series.values())
high = max(v.max() for v in series.values())
ordered = sorted(series.items(), key=lambda kv: kv[1][-1] - kv[1][0], reverse=True)

fig, axes = plt.subplots(3, 4, figsize=(12, 6), sharex=True, sharey=True)

for ax, (name, values) in zip(axes.flat, ordered):
    # Ghost: all the other series, very faint, for context.
    for other in series.values():
        ax.plot(months, other, color="#EAEAEA", lw=0.8, zorder=0)
    change = values[-1] - values[0]
    colour = "#0072B2" if change > 0 else "#D55E00"
    ax.plot(months, values, color=colour, lw=2)
    ax.set_title(f"{name}   {change:+.0f}", fontsize=9)
    ax.set_ylim(low - 5, high + 5)

fig.suptitle("Same scales, ordered by change, each with the others ghosted behind",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "small-multiples")

print("""
  Small multiples work only if you obey both rules:
    1. identical scales on every panel  (sharex/sharey, or set the limits)
    2. order the panels by something meaningful, not alphabetically
  A ghost of the other series behind each panel gives context for free.
""")
