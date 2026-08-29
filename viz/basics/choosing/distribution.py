"""
Showing a distribution -- histogram, box, violin, and the honest strip plot.

The question this chart answers: "what is the shape of this data?"

What it shows:
    * bin width changes the story a histogram tells -- see it happen
    * a box plot hides shape; two very different datasets can share one
    * a violin shows shape but invents smoothness it cannot know
    * with few points, just show the points

The rule underneath: a summary throws information away. Know what you threw.

Run it:
    python viz/basics/choosing/distribution.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, temperatures                # noqa: E402

temps = temperatures()["temp_c"].to_numpy()

# --- 1. the bin width IS an argument you are making ------------------------
fig, axes = plt.subplots(1, 4, figsize=(14, 3.2), sharey=False)

for ax, bins in zip(axes, [3, 10, 30, 200]):
    ax.hist(temps, bins=bins, color="#4C72B0", edgecolor="white")
    ax.set_title(f"bins = {bins}")
    ax.set_xlabel("temp (C)")

fig.suptitle("Same 365 numbers. Too few bins hides the shape; too many shows noise.",
             fontsize=11)
fig.tight_layout()
save(fig, __file__, "bin-width")

# --- 2. the box plot's blind spot ------------------------------------------
# Three datasets, deliberately built to share a five-number summary while
# looking nothing alike.
# The parameters are chosen so all three share a five-number summary: their
# quartiles agree to within about 2 points. That is the whole point -- the
# box plot cannot tell them apart, and the histogram below cannot miss.
rng = np.random.default_rng(7)
normal = rng.normal(50, 11.86, 400)                       # IQR ~16
bimodal = np.concatenate([rng.normal(42, 3.5, 200),       # two tight humps
                          rng.normal(58, 3.5, 200)])      # sitting on Q1 and Q3
uniform = rng.uniform(34, 66, 400)                        # flat, same IQR
groups = [normal, bimodal, uniform]
labels = ["one hump", "two humps", "flat"]

# One wide panel for the boxes, then one panel per histogram. Overlaying the
# three histograms turns them to mud -- separate panels is the whole trick,
# and it is what the layout chapter calls small multiples.
fig, axes = plt.subplot_mosaic([["box", "box", "box"],
                                ["h0", "h1", "h2"]], figsize=(11, 6))

axes["box"].boxplot(groups, tick_labels=labels, vert=False)
axes["box"].set_title("Box plots: near-identical quartiles")
axes["box"].set_xlim(5, 85)

for i, (values, label) in enumerate(zip(groups, labels)):
    ax = axes[f"h{i}"]
    ax.hist(values, bins=35, color="#4C72B0", edgecolor="white")
    ax.set_title(label)
    ax.set_xlim(5, 85)              # same axis, or the comparison is a lie
    ax.set_ylim(0, 45)
    if i:
        ax.set_yticklabels([])

fig.suptitle("Same five-number summary. Three completely different shapes.",
             fontsize=12)
axes["h0"].set_ylabel("count")
fig.tight_layout()
save(fig, __file__, "box-hides-shape")

# --- 3. with few points, show the points -----------------------------------
small = rng.normal(50, 12, 14)

fig, axes = plt.subplots(1, 3, figsize=(11, 3.4))

axes[0].boxplot([small], tick_labels=["n=14"])
axes[0].set_title("Box: implies more data than exists")

axes[1].violinplot([small])
axes[1].set_title("Violin: invents a smooth curve")

axes[2].plot(np.ones(len(small)) + rng.normal(0, 0.02, len(small)), small,
             "o", alpha=0.7, color="#4C72B0")
axes[2].set_xlim(0.8, 1.2)
axes[2].set_xticks([])
axes[2].set_title("Strip: 14 points, shown as 14 points")

fig.tight_layout()
save(fig, __file__, "few-points")

print("""
  Choose by sample size and question:
    n < ~30            -> show every point (strip / dot)
    "what shape?"      -> histogram, and try more than one bin width
    "compare groups?"  -> box or violin, but say n somewhere
""")
