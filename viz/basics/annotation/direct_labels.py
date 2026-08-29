"""
Label the lines, not the legend.

A legend makes the reader do a matching exercise: find the colour, carry it
across the chart, find the line. Putting the name next to the line removes
that work entirely.

What it shows:
    * a legend replaced by labels at the end of each line
    * ax.annotate with data coordinates, and how to stop labels overlapping
    * why this matters more as the number of series grows

Run it:
    python viz/basics/annotation/direct_labels.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, sales                       # noqa: E402

wide = sales().pivot(index="month", columns="region", values="sales")
COLOURS = {"North": "#0072B2", "South": "#E69F00",
           "East": "#009E73", "West": "#CC79A7"}

# --- 1. legend versus direct labels ----------------------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(12, 4.2))

for region in wide.columns:
    left.plot(wide.index, wide[region], color=COLOURS[region], label=region, lw=2)
left.legend(title="region")
left.set_title("Legend: find the colour, then find the line")
left.set_ylabel("sales")

for region in wide.columns:
    right.plot(wide.index, wide[region], color=COLOURS[region], lw=2)
    # Put the name at the line's last point, nudged right and centred.
    right.annotate(
        region,
        xy=(wide.index[-1], wide[region].iloc[-1]),
        xytext=(6, 0), textcoords="offset points",
        color=COLOURS[region], fontsize=10, fontweight="bold",
        va="center",
    )
# Leave room on the right for the labels, or they fall off the edge.
right.set_xlim(wide.index[0], wide.index[-1] + (wide.index[-1] - wide.index[-4]))
right.set_title("Direct labels: the name IS the legend")
right.set_ylabel("sales")

fig.tight_layout()
save(fig, __file__, "legend-vs-direct")

# --- 2. when the ends are too close together -------------------------------
# Nudge overlapping labels apart, cheaply: sort by value and enforce a gap.
final = wide.iloc[-1].sort_values()
gap = (wide.to_numpy().max() - wide.to_numpy().min()) * 0.07

positions = {}
last = -1e9
for region, value in final.items():
    position = max(value, last + gap)
    positions[region] = position
    last = position

fig, ax = plt.subplots(figsize=(8, 4.2))
for region in wide.columns:
    ax.plot(wide.index, wide[region], color=COLOURS[region], lw=2)
    ax.annotate(f"{region}  {wide[region].iloc[-1]:.0f}",
                xy=(wide.index[-1], positions[region]),
                xytext=(8, 0), textcoords="offset points",
                color=COLOURS[region], fontsize=9, fontweight="bold", va="center")

ax.set_xlim(wide.index[0], wide.index[-1] + (wide.index[-1] - wide.index[-5]))
ax.set_title("Labels nudged apart, and carrying the final value too")
ax.set_ylabel("sales")
fig.tight_layout()
save(fig, __file__, "nudged-labels")

print("""
  A legend is a lookup table. A label is an answer.
  Put the name where the line ends, and delete the legend.
""")
