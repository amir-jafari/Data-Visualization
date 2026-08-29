"""
Two numbers together -- scatter plots, and what to do when they pile up.

The question this chart answers: "does x have anything to do with y?"

What it shows:
    * scatter first, statistics second -- always look before you fit
    * overplotting, and three fixes: transparency, smaller marks, binning
    * a trend line helps, but only if you say what kind it is
    * the same correlation can come from very different pictures

Run it:
    python viz/basics/choosing/relationship.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, students                    # noqa: E402

data = students()

# --- 1. the basic scatter, with and without a trend ------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

left.scatter(data["hours"], data["score"], s=18, color="#4C72B0")
left.set(xlabel="hours studied", ylabel="exam score", title="Just the points")

right.scatter(data["hours"], data["score"], s=18, color="#4C72B0", alpha=0.6)
slope, intercept = np.polyfit(data["hours"], data["score"], 1)
xs = np.linspace(data["hours"].min(), data["hours"].max(), 100)
right.plot(xs, slope * xs + intercept, color="#C44E52", lw=2,
           label=f"least squares: {slope:.1f} points per hour")
right.legend()
right.set(xlabel="hours studied", ylabel="exam score",
          title="With a line -- and the line is labelled")

fig.tight_layout()
save(fig, __file__, "scatter")

# --- 2. overplotting: when there are too many points -----------------------
rng = np.random.default_rng(11)
n = 40_000
x = rng.normal(0, 1, n)
y = x * 0.6 + rng.normal(0, 0.8, n)

fig, axes = plt.subplots(1, 4, figsize=(14, 3.4))

axes[0].scatter(x, y, s=20)
axes[0].set_title("Default: a solid blob")

axes[1].scatter(x, y, s=20, alpha=0.02)
axes[1].set_title("alpha=0.02: density appears")

axes[2].scatter(x, y, s=0.5, alpha=0.3)
axes[2].set_title("Tiny marks")

hb = axes[3].hexbin(x, y, gridsize=45, cmap="Blues")
axes[3].set_title("hexbin: count per cell")
fig.colorbar(hb, ax=axes[3], label="count")

for ax in axes:
    ax.set_xlabel("x")
axes[0].set_ylabel("y")

fig.suptitle(f"{n:,} points. The first panel is not a chart, it is an ink stain.",
             fontsize=11)
fig.tight_layout()
save(fig, __file__, "overplotting")

# --- 3. the same correlation, four different truths ------------------------
# Anscombe's quartet: four datasets with the same mean, variance, correlation
# and regression line. This is why you plot before you summarise.
quartet = {
    "I":   ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
            [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    "II":  ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
            [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    "III": ([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5],
            [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    "IV":  ([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
            [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}

fig, axes = plt.subplots(1, 4, figsize=(14, 3.4), sharex=True, sharey=True)
for ax, (name, (xs_, ys_)) in zip(axes, quartet.items()):
    xs_, ys_ = np.array(xs_), np.array(ys_)
    ax.scatter(xs_, ys_, color="#4C72B0", s=35)
    m, b = np.polyfit(xs_, ys_, 1)
    line = np.array([3, 20])
    ax.plot(line, m * line + b, color="#C44E52", lw=1.5)
    ax.set_title(f"{name}:  r = {np.corrcoef(xs_, ys_)[0, 1]:.2f}")
    ax.set_xlim(2, 20)

fig.suptitle("Anscombe's quartet: identical means, variances, correlation and "
             "regression line", fontsize=11)
fig.tight_layout()
save(fig, __file__, "anscombe")

print("""
  Look at the picture before you trust the number.
    few points     -> plain scatter
    many points    -> alpha, smaller marks, or hexbin
    adding a line  -> say which line it is
""")
