"""
Chart junk -- everything on the chart that is not the data.

Tufte's question: if you removed this ink, would the reader lose anything? If
not, remove it. Heavy gridlines, 3D effects, boxes around everything, and a
legend for a single series are all ink that costs attention and returns
nothing.

What it shows:
    * the same bar chart at four levels of decoration
    * what to remove, in the order to remove it
    * where restraint stops: labels and units are NOT junk

Run it:
    python viz/basics/layout/chart_junk.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, survey                      # noqa: E402

data = survey().sort_values("users")

fig, axes = plt.subplots(1, 4, figsize=(15, 4))

# (1) Everything on. Heavy grid, full frame, dark bars, legend for one series.
ax = axes[0]
ax.barh(data["tool"], data["users"], color="#333366", label="users",
        edgecolor="black", linewidth=1.2)
ax.grid(True, which="both", color="#999999", linewidth=1.0)
ax.legend()
ax.set_title("1. everything on", fontsize=10)
ax.set_xlabel("number of users")

# (2) Grid tamed: horizontal only, faint, behind the bars.
ax = axes[1]
ax.barh(data["tool"], data["users"], color="#333366", edgecolor="black", linewidth=1.2)
ax.grid(axis="x", color="#DDDDDD", linewidth=0.8)
ax.set_axisbelow(True)
ax.set_title("2. grid tamed, legend gone", fontsize=10)
ax.set_xlabel("number of users")

# (3) Frame opened up, bar outlines dropped, colour softened.
ax = axes[2]
ax.barh(data["tool"], data["users"], color="#4C72B0")
ax.grid(axis="x", color="#DDDDDD", linewidth=0.8)
ax.set_axisbelow(True)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.set_title("3. frame opened, bars softened", fontsize=10)
ax.set_xlabel("number of users")

# (4) Values on the bars, so the x axis itself becomes unnecessary.
ax = axes[3]
bars = ax.barh(data["tool"], data["users"], color="#4C72B0")
ax.bar_label(bars, padding=4, fontsize=9, color="#333333")
for side in ("top", "right", "left", "bottom"):
    ax.spines[side].set_visible(False)
ax.set_xticks([])
ax.set_xlim(0, data["users"].max() * 1.18)
ax.set_title("4. values labelled, axis retired", fontsize=10)

fig.suptitle("Same numbers. Each step removes ink and adds clarity.", fontsize=12)
fig.tight_layout()
save(fig, __file__, "four-levels")

# --- where restraint stops -------------------------------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.8))

bars = left.barh(data["tool"], data["users"], color="#4C72B0")
for side in ("top", "right", "left", "bottom"):
    left.spines[side].set_visible(False)
left.set_xticks([])
left.set_title("Too far: what is being counted? Over what period?", fontsize=10)

bars = right.barh(data["tool"], data["users"], color="#4C72B0")
right.bar_label(bars, padding=4, fontsize=9)
for side in ("top", "right", "left", "bottom"):
    right.spines[side].set_visible(False)
right.set_xticks([])
right.set_xlim(0, data["users"].max() * 1.18)
right.set_title("Tools used daily, 2025 survey", fontsize=12,
                fontweight="bold", loc="left")
right.text(0.0, 1.02, f"n = {data['users'].sum():,} respondents, multiple answers allowed",
           transform=right.transAxes, fontsize=8, color="#666666")

fig.tight_layout()
save(fig, __file__, "restraint-limit")

print("""
  Remove, in this order:
    1. legends for a single series, and 3D anything
    2. heavy gridlines -> faint, one direction, behind the data
    3. the top/right frame, and outlines on bars
    4. the axis itself, if you label the values directly

  Never remove: what is measured, the units, the sample size, the source.
""")
