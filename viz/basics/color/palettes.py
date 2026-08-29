"""
Three kinds of colour, and picking the right one.

The single most useful idea in this whole folder:

    CATEGORICAL  -- unordered things (regions, species). Distinct hues.
    SEQUENTIAL   -- a quantity from low to high. One hue, light to dark.
    DIVERGING    -- distance from a meaningful middle (zero, average).
                    Two hues meeting at a neutral centre.

Use the wrong family and the picture lies before anyone reads a number.

What it shows:
    * the three families, side by side, on data that suits each
    * a sequential palette used on categories -- inventing an order
    * a diverging palette without a meaningful centre -- inventing a middle
    * how many categories is too many (about seven)

Run it:
    python viz/basics/color/palettes.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save                              # noqa: E402

rng = np.random.default_rng(5)

# --- 1. the three families -------------------------------------------------
fig, axes = plt.subplots(3, 1, figsize=(9, 5))

gradient = np.linspace(0, 1, 256).reshape(1, -1)
for ax, cmap, label in [
    (axes[0], "tab10", "CATEGORICAL (tab10) -- unordered groups"),
    (axes[1], "viridis", "SEQUENTIAL (viridis) -- low to high"),
    (axes[2], "RdBu_r", "DIVERGING (RdBu_r) -- below / at / above a centre"),
]:
    ax.imshow(gradient, aspect="auto", cmap=cmap)
    ax.set_title(label, fontsize=10, loc="left")
    ax.set_xticks([]); ax.set_yticks([])

fig.tight_layout()
save(fig, __file__, "three-families")

# --- 2. sequential used on categories = an order that is not there ---------
fruit = ["apple", "banana", "cherry", "date", "elderberry"]
counts = [23, 17, 35, 12, 28]

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.6))

wrong = plt.get_cmap("viridis")(np.linspace(0.15, 0.9, len(fruit)))
left.bar(fruit, counts, color=wrong)
left.set_title("Sequential on categories:\nimplies apple < banana < cherry", fontsize=10)

right.bar(fruit, counts, color=plt.get_cmap("tab10").colors[:len(fruit)])
right.set_title("Categorical: no order implied", fontsize=10)

fig.tight_layout()
save(fig, __file__, "sequential-on-categories")

# --- 3. diverging needs a real centre --------------------------------------
grid_positive = rng.uniform(10, 90, (12, 12))                 # no natural middle
grid_change = rng.normal(0, 25, (12, 12))                     # centred on zero

fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))

im0 = axes[0].imshow(grid_positive, cmap="RdBu_r")
axes[0].set_title("Diverging on 10-90:\nwhite is meaningless here", fontsize=10)
fig.colorbar(im0, ax=axes[0])

im1 = axes[1].imshow(grid_positive, cmap="viridis")
axes[1].set_title("Sequential: correct for\na plain quantity", fontsize=10)
fig.colorbar(im1, ax=axes[1])

# For diverging, pin the centre yourself -- otherwise it lands wherever the
# data happens to average out.
limit = np.abs(grid_change).max()
im2 = axes[2].imshow(grid_change, cmap="RdBu_r", vmin=-limit, vmax=limit)
axes[2].set_title("Diverging on change:\nwhite = zero, and vmin/vmax pinned", fontsize=10)
fig.colorbar(im2, ax=axes[2])

fig.tight_layout()
save(fig, __file__, "diverging-centre")

# --- 4. too many categories ------------------------------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

x = np.arange(20)
for i in range(14):
    left.plot(x, np.cumsum(rng.normal(0, 1, 20)), label=f"item {i}")
left.legend(fontsize=6, ncol=2)
left.set_title("14 colours: nobody can match line to legend", fontsize=10)

series = [np.cumsum(rng.normal(0, 1, 20)) for _ in range(14)]
for values in series:
    right.plot(x, values, color="#CCCCCC", lw=1)
for i in (2, 7):
    right.plot(x, series[i], lw=2.5, label=f"item {i}")
right.legend(fontsize=9)
right.set_title("Grey the rest, colour the two you mean", fontsize=10)

fig.tight_layout()
save(fig, __file__, "too-many-categories")

print("""
  Pick the family from the data, not from taste:
    unordered groups        -> categorical (tab10), max ~7
    a quantity low to high  -> sequential (viridis)
    distance from a centre  -> diverging (RdBu_r), and PIN vmin/vmax
  More than 7 groups? Colour the ones you are talking about, grey the rest.
""")
