"""
Cherry-picking -- lying with entirely real numbers.

Every value in these charts is true. The distortion is in the choices: where
the time window starts, how the bins are cut, and which comparison is left out.
This is the hardest family to spot, because there is nothing false to point at.

What it shows:
    * a window chosen to reverse a trend
    * bin boundaries chosen to make a bump appear or vanish
    * a percentage change with no baseline, which can mean anything

Run it:
    python viz/basics/misleading/cherry_picking.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save                              # noqa: E402

# --- 1. the chosen window --------------------------------------------------
rng = np.random.default_rng(21)
years = np.arange(2000, 2025)
values = 100 + 3.2 * (years - 2000) + rng.normal(0, 9, len(years))
values[14:18] -= 22                      # a real, temporary dip

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

window = slice(14, 19)
left.plot(years[window], values[window], "-o", color="#C44E52", lw=2)
slope_window = np.polyfit(years[window], values[window], 1)[0]
left.set_title(f"2014-2018 only: 'a decline of {abs(slope_window):.1f}/year'",
               fontsize=10)

left_line = np.polyfit(years, values, 1)[0]
right.plot(years, values, "-o", color="#4C72B0", lw=1.5, markersize=3)
right.axvspan(years[14], years[18], color="#F8D7DA", zorder=0)
right.annotate("the window on the left", xy=(years[16], values[14:19].min() - 12),
               ha="center", fontsize=8, color="#C44E52")
right.set_title(f"All 25 years: 'a rise of {left_line:.1f}/year'", fontsize=10)

for ax in (left, right):
    ax.set_ylabel("index")

fig.suptitle("Same series. The window does all the work.", fontsize=12)
fig.tight_layout()
save(fig, __file__, "chosen-window")

# --- 2. the chosen bins ----------------------------------------------------
ages = np.concatenate([rng.normal(24, 4, 300), rng.normal(41, 6, 300)])

fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))

axes[0].hist(ages, bins=np.arange(10, 61, 5), color="#4C72B0", edgecolor="white")
axes[0].set_title("bins of 5: two clear groups", fontsize=10)

axes[1].hist(ages, bins=np.arange(10, 61, 20), color="#C44E52", edgecolor="white")
axes[1].set_title("bins of 20: one smooth hump", fontsize=10)

axes[2].hist(ages, bins=[10, 30, 35, 60], color="#8172B2", edgecolor="white")
axes[2].set_title("uneven bins: pure invention", fontsize=10)

for ax in axes:
    ax.set_xlabel("age")

fig.suptitle("Identical 600 people. Bin boundaries are an argument, so state them.",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "chosen-bins")

# --- 3. percentages with no baseline ---------------------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.8))

conditions = ["Drug A", "Drug B"]
relative = [50, 50]                       # both "cut the risk by half"
absolute_before = [0.02, 40.0]            # from very different baselines
absolute_after = [0.01, 20.0]

left.bar(conditions, relative, color="#C44E52")
left.set_ylabel("% risk reduction")
left.set_title("'Both halve your risk!'", fontsize=10)

x = np.arange(2)
left_bars = right.bar(x - 0.2, absolute_before, width=0.4, label="before",
                      color="#CCCCCC")
right_bars = right.bar(x + 0.2, absolute_after, width=0.4, label="after",
                       color="#4C72B0")
right.set_yscale("log")
right.set_xticks(x); right.set_xticklabels(conditions)
right.set_ylabel("absolute risk (%) -- log scale")
right.bar_label(left_bars, fmt="%.2f", fontsize=8)
right.bar_label(right_bars, fmt="%.2f", fontsize=8)
right.legend(fontsize=8)
right.set_title("The same two, with their baselines", fontsize=10)

fig.suptitle("A relative change with no baseline is not information",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "no-baseline")

print("""
  Three questions to ask any chart -- including your own:
    1. why does the time axis start THERE?
    2. who chose the bins/categories, and what happens if I change them?
    3. a percentage of WHAT? show me the baseline and the sample size.
""")
