"""
Grey everything, colour the point.

Colour is the strongest signal you have. Spending it on all ten series means
spending it on none of them. Spend it on the one you are talking about.

What it shows:
    * the same chart told three different ways, by changing only what is grey
    * highlighting a region of the x axis with axvspan
    * marking and labelling a single important point

Run it:
    python viz/basics/annotation/highlight.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, sales                       # noqa: E402

wide = sales().pivot(index="month", columns="region", values="sales")

# --- 1. one chart, three stories -------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

for ax in axes:
    for region in wide.columns:
        ax.plot(wide.index, wide[region], color="#D9D9D9", lw=1.5)
    ax.tick_params(axis="x", rotation=30, labelsize=7)
    ax.set_ylim(wide.to_numpy().min() - 10, wide.to_numpy().max() + 10)

axes[0].plot(wide.index, wide["West"], color="#0072B2", lw=2.5)
axes[0].set_title("'West is growing fastest'", fontsize=11)

axes[1].plot(wide.index, wide["East"], color="#D55E00", lw=2.5)
axes[1].set_title("'East has stalled'", fontsize=11)

axes[2].plot(wide.index, wide["North"], color="#009E73", lw=2.5)
axes[2].plot(wide.index, wide["West"], color="#0072B2", lw=2.5)
axes[2].set_title("'West is catching North'", fontsize=11)

fig.suptitle("Same data, same axes. Only the greying changed.", fontsize=12)
fig.tight_layout()
save(fig, __file__, "three-stories")

# --- 2. highlight a period, and mark the moment ----------------------------
fig, ax = plt.subplots(figsize=(9, 4.2))

for region in wide.columns:
    ax.plot(wide.index, wide[region], color="#D9D9D9", lw=1.5)
ax.plot(wide.index, wide["South"], color="#0072B2", lw=2.5)

# A shaded band is quieter than a vertical line and reads as "this period".
ax.axvspan(wide.index[11], wide.index[17], color="#FFF3CD", zorder=0)
ax.annotate("campaign ran here", xy=(wide.index[14], wide.to_numpy().max()),
            ha="center", fontsize=9, color="#8A6D3B")

peak_month = wide["South"].idxmax()
peak_value = wide["South"].max()
ax.plot([peak_month], [peak_value], "o", color="#0072B2", markersize=9)
ax.annotate(f"peak: {peak_value:.0f}",
            xy=(peak_month, peak_value), xytext=(-70, 18),
            textcoords="offset points", fontsize=9, color="#0072B2",
            arrowprops=dict(arrowstyle="->", color="#0072B2"))

ax.set_title("South, with the period and the peak called out")
ax.set_ylabel("sales")
fig.tight_layout()
save(fig, __file__, "highlight-period")

print("""
  Ask "what is the one thing I want them to see?" -- then grey the rest.
  axvspan for a period, a marker + annotate for a moment.
""")
