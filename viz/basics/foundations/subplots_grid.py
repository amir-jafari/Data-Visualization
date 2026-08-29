"""
Many plots in one figure -- subplots, shared axes, and uneven grids.

What it shows:
    * plt.subplots(rows, cols) and the array of Axes it hands back
    * sharex / sharey -- essential when panels must be compared
    * subplot_mosaic for layouts that are not a plain grid
    * tight_layout / constrained_layout, and when each one gives up

Run it:
    python viz/basics/foundations/subplots_grid.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, sales                       # noqa: E402

data = sales()
wide = data.pivot(index="month", columns="region", values="sales")

# --- 1. sharing axes is not cosmetic ---------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(13, 3.2))
for ax, region in zip(axes, wide.columns):
    ax.plot(wide.index, wide[region], color="#4C72B0")
    ax.set_title(region)
    ax.tick_params(axis="x", rotation=45, labelsize=7)
fig.suptitle("NOT shared: each panel has its own y range. West looks like North.",
             fontsize=11)
fig.tight_layout()
save(fig, __file__, "not-shared")

fig, axes = plt.subplots(1, 4, figsize=(13, 3.2), sharey=True)
for ax, region in zip(axes, wide.columns):
    ax.plot(wide.index, wide[region], color="#4C72B0")
    ax.set_title(region)
    ax.tick_params(axis="x", rotation=45, labelsize=7)
axes[0].set_ylabel("sales")
fig.suptitle("sharey=True: now the panels are actually comparable", fontsize=11)
fig.tight_layout()
save(fig, __file__, "shared")

# --- 2. uneven layouts with subplot_mosaic ---------------------------------
# Each string is a row; repeated letters make a panel span cells.
fig, axes = plt.subplot_mosaic(
    [["main", "main", "side"],
     ["main", "main", "side"],
     ["bottom", "bottom", "bottom"]],
    figsize=(10, 6),
)

for region in wide.columns:
    axes["main"].plot(wide.index, wide[region], label=region)
axes["main"].set_title("main: the headline chart")
axes["main"].legend(fontsize=8)

axes["side"].barh(wide.columns, wide.iloc[-1], color="#4C72B0")
axes["side"].set_title("side: latest month")

axes["bottom"].bar(wide.index, wide.sum(axis=1), width=20, color="#8172B2")
axes["bottom"].set_title("bottom: total across regions")

fig.suptitle("subplot_mosaic: draw the layout as text, get it as Axes",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "mosaic")

# --- 3. when tight_layout gives up -----------------------------------------
# tight_layout cannot make room for anything placed OUTSIDE the axes, such as
# a legend anchored beyond the right edge. There are three ways out, and it is
# worth knowing all three because they act at different moments.
rng = np.random.default_rng(0)
x = np.arange(30)


def six_series(ax):
    for i in range(6):
        ax.plot(x, np.cumsum(rng.normal(0, 1, 30)), label=f"series {i}")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")


# (a) the problem, saved with no rescue -- crop=False, or you would not see it
fig, ax = plt.subplots(figsize=(6, 3))
six_series(ax)
ax.set_title("tight_layout: the legend is cut off")
fig.tight_layout()
save(fig, __file__, "tight-fails", crop=False)

# (b) fix at DRAW time: constrained_layout knows about the legend
fig, ax = plt.subplots(figsize=(6, 3), layout="constrained")
six_series(ax)
ax.set_title("constrained_layout: room made while drawing")
save(fig, __file__, "constrained-works", crop=False)

# (c) fix at SAVE time: bbox_inches="tight" grows the image to fit
fig, ax = plt.subplots(figsize=(6, 3))
six_series(ax)
ax.set_title('savefig(bbox_inches="tight"): image grown to fit')
fig.tight_layout()
save(fig, __file__, "bbox-tight", crop=True)

print("""
  Panels:
    comparing panels?          -> sharey=True, or the comparison is a lie
    layout is not a grid?      -> subplot_mosaic, drawn as text
    anything outside the axes? -> layout="constrained", not tight_layout()
""")
