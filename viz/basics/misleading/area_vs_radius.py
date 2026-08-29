"""
Bubbles, icons and the squared-error trap.

To show that B is twice A, people often draw circle B with twice the RADIUS.
That gives it FOUR times the area -- and area is what the eye reads. The same
mistake doubles the height and width of an icon, giving four times the ink.

What it shows:
    * radius scaling versus area scaling, with the exaggeration measured
    * matplotlib's scatter `s` argument, which is area (and people forget)
    * a legend for bubble size, which almost nobody bothers to draw

Run it:
    python viz/basics/misleading/area_vs_radius.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save                              # noqa: E402

values = np.array([1, 2, 4, 8])

# --- 1. the same four numbers, two ways --------------------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

# WRONG: radius proportional to the value -> area grows with the SQUARE.
for i, v in enumerate(values):
    left.add_patch(plt.Circle((i, 0), radius=v * 0.05, color="#C44E52"))
    left.text(i, -0.42, f"{v}", ha="center", fontsize=11)
left.set_xlim(-0.6, 3.9); left.set_ylim(-0.55, 0.55)
left.set_aspect("equal"); left.axis("off")
left.set_title("WRONG: radius proportional to value\n8 looks 64x bigger than 1",
               fontsize=10)

# RIGHT: area proportional to the value -> radius grows with the SQUARE ROOT.
for i, v in enumerate(values):
    right.add_patch(plt.Circle((i, 0), radius=np.sqrt(v) * 0.05, color="#4C72B0"))
    right.text(i, -0.42, f"{v}", ha="center", fontsize=11)
right.set_xlim(-0.6, 3.9); right.set_ylim(-0.55, 0.55)
right.set_aspect("equal"); right.axis("off")
right.set_title("RIGHT: area proportional to value\n8 looks 8x bigger than 1",
                fontsize=10)

fig.suptitle("Scale the AREA. The eye measures ink, not radius.", fontsize=12)
fig.tight_layout()
save(fig, __file__, "radius-vs-area")

# --- 2. what matplotlib's `s` actually means -------------------------------
# scatter's s is the marker AREA in points^2. Passing the raw value is correct;
# passing value**2 squares it a second time.
x = np.arange(4)

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.6))

left.scatter(x, np.zeros(4), s=(values * 40) ** 2 / 40, color="#C44E52")
left.set_title("s = value squared: exaggerated again", fontsize=10)

right.scatter(x, np.zeros(4), s=values * 300, color="#4C72B0")
right.set_title("s = value * constant: correct, because s IS area", fontsize=10)

for ax in (left, right):
    ax.set_xticks(x); ax.set_xticklabels(values)
    ax.set_yticks([]); ax.set_xlabel("value")

fig.tight_layout()
save(fig, __file__, "scatter-s")

# --- 3. a size legend ------------------------------------------------------
rng = np.random.default_rng(9)
n = 40
gdp = rng.uniform(1, 60, n)

fig, ax = plt.subplots(figsize=(7.5, 5))
scatter = ax.scatter(rng.uniform(0, 10, n), rng.uniform(0, 10, n),
                     s=gdp * 12, alpha=0.6, color="#0072B2")

# legend_elements does the sqrt maths for you, so the key matches the marks.
handles, labels = scatter.legend_elements(prop="sizes", num=4, alpha=0.6,
                                          func=lambda s: s / 12)
ax.legend(handles, labels, title="GDP ($bn)", loc="upper right",
          labelspacing=1.6, borderpad=1.1, frameon=True)
ax.set(title="Bubble chart with a size legend", xlabel="x", ylabel="y")

fig.tight_layout()
save(fig, __file__, "size-legend")

print(f"""
  The maths:
    radius x {values[-1]}  ->  area x {values[-1] ** 2}   (a {values[-1] ** 2}-fold exaggeration)
    area   x {values[-1]}  ->  radius x {np.sqrt(values[-1]):.2f}   (correct)

  In matplotlib, scatter(s=...) is AREA in points^2. Pass the value itself,
  scaled by a constant. Never pass value**2.
  And draw a size legend, or nobody can read the sizes at all.
""")
