"""
Change over time -- lines, and the traps in them.

The question this chart answers: "what happened, and where is it going?"

What it shows:
    * time goes on the x axis, always, left to right
    * lines connect -- so only use one when the gap between points means something
    * a line chart does NOT need a zero baseline (unlike bars)
    * stacked areas hide the middle series; only the bottom one is readable

Run it:
    python viz/basics/choosing/change_over_time.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, sales                       # noqa: E402

data = sales()
wide = data.pivot(index="month", columns="region", values="sales")

# --- 1. lines do not need a zero -------------------------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

wide.plot(ax=left, legend=False)
left.set_ylim(0, wide.to_numpy().max() * 1.05)
left.set_title("Forced to zero: all the movement is squashed")
left.set_ylabel("sales")

wide.plot(ax=right)
right.set_title("Natural range: the differences are visible")
right.legend(title="region", fontsize=8)

fig.suptitle("Bars need zero because you read LENGTH. Lines you read by SLOPE.",
             fontsize=11)
fig.tight_layout()
save(fig, __file__, "zero-or-not")

# --- 2. stacked area: only the bottom band is honest -----------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

left.stackplot(wide.index, [wide[c] for c in wide.columns], labels=wide.columns)
left.set_title("Stacked: can you tell if 'East' is growing?")
left.legend(loc="upper left", fontsize=8)

wide.plot(ax=right)
right.set_title("Unstacked: now you can")
right.legend(title="region", fontsize=8)

fig.suptitle("In a stack, every band except the bottom sits on a wobbly floor.",
             fontsize=11)
fig.tight_layout()
save(fig, __file__, "stacked-area")

# --- 3. do not connect points that are not connected -----------------------
survey_years = [2016, 2017, 2018, 2022, 2023]
satisfaction = [61, 64, 66, 58, 60]

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.6))

left.plot(survey_years, satisfaction, "-o", color="#4C72B0")
left.set_title("A line implies we measured 2019-2021. We did not.")

right.plot(survey_years, satisfaction, "o", color="#4C72B0", markersize=8)
right.plot(survey_years[:3], satisfaction[:3], "-", color="#4C72B0")
right.plot(survey_years[3:], satisfaction[3:], "-", color="#4C72B0")
right.set_title("Break the line across the gap")

for ax in (left, right):
    ax.set_xticks(survey_years)
    ax.set_ylabel("% satisfied")

fig.tight_layout()
save(fig, __file__, "gaps")

print("""
  Time series rules:
    time on x, left to right, always
    lines may start anywhere -- slope is the message
    gaps in the data -> gaps in the line
    stacking hides everything above the bottom band
""")
