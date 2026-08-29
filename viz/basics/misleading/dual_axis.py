"""
Two y axes -- where correlation is manufactured.

Put two series on two different y axes and you get to choose the scales. Any
two lines can be made to cross, touch, or move together. The reader sees a
relationship that you invented with a scaling factor.

What it shows:
    * one pair of series made to tell three different stories
    * why the crossing point is meaningless
    * three honest alternatives that keep the information

Run it:
    python viz/basics/misleading/dual_axis.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, two_series                  # noqa: E402

data = two_series()
months, revenue, headcount = data["month"], data["revenue_k"], data["headcount"]

# --- 1. the same data, three "findings" ------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

scalings = [
    ((150, 450), (10, 30), "'headcount tracks revenue'"),
    ((150, 450), (0, 60), "'revenue outgrew the team'"),
    ((0, 900), (10, 26), "'the team outgrew revenue'"),
]

for ax, (rev_lim, head_lim, story) in zip(axes, scalings):
    ax.plot(months, revenue, color="#0072B2", lw=2)
    ax.set_ylim(*rev_lim)
    ax.set_ylabel("revenue ($k)", color="#0072B2")
    ax.tick_params(axis="y", labelcolor="#0072B2")
    ax.tick_params(axis="x", rotation=30, labelsize=7)

    twin = ax.twinx()
    twin.plot(months, headcount, color="#D55E00", lw=2)
    twin.set_ylim(*head_lim)
    twin.set_ylabel("headcount", color="#D55E00")
    twin.tick_params(axis="y", labelcolor="#D55E00")

    ax.set_title(story, fontsize=11)

fig.suptitle("Identical data in all three. Only the two y ranges changed.",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "three-stories")

# --- 2. the honest alternatives --------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# (a) Two panels, stacked. Nothing is hidden and nothing is implied.
axes[0].plot(months, revenue, color="#0072B2", lw=2)
axes[0].set_title("a) separate panels", fontsize=10)
axes[0].set_ylabel("revenue ($k)")
axes[0].tick_params(axis="x", rotation=30, labelsize=7)

# (b) Index both to their starting value: now they share one honest axis.
axes[1].plot(months, 100 * revenue / revenue.iloc[0], color="#0072B2",
             lw=2, label="revenue")
axes[1].plot(months, 100 * headcount / headcount.iloc[0], color="#D55E00",
             lw=2, label="headcount")
axes[1].axhline(100, color="#999999", lw=0.8)
axes[1].set_title("b) indexed to 100 at the start", fontsize=10)
axes[1].set_ylabel("index (first month = 100)")
axes[1].legend(fontsize=8)
axes[1].tick_params(axis="x", rotation=30, labelsize=7)

# (c) Plot the thing you actually mean: the ratio.
axes[2].plot(months, revenue / headcount, color="#009E73", lw=2)
axes[2].set_title("c) the ratio -- revenue per head", fontsize=10)
axes[2].set_ylabel("$k per person")
axes[2].tick_params(axis="x", rotation=30, labelsize=7)

fig.suptitle("Three honest ways to compare two series on different scales",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "alternatives")

correlation = np.corrcoef(revenue, headcount)[0, 1]
print(f"""
  The real relationship, unchanged by any of the pictures above:
    correlation(revenue, headcount) = {correlation:.2f}

  A dual axis lets you pick where the lines cross. That crossing point means
  nothing -- it is a property of your two scale choices, not the data.

  Instead: separate panels, index both to 100, or plot the ratio.
""")
