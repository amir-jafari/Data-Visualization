"""
Comparing categories -- bars, and what to use when bars stop working.

The question this chart answers: "which is biggest?"

What it shows:
    * bars must start at zero, because you read them by LENGTH
    * sort by value, not alphabetically -- ordering is free information
    * horizontal bars when the labels are words
    * a dot plot when there are many categories or a narrow range

The rule underneath: match the mark to the comparison. Length works for
"how much"; position works for "where in the range".

Run it:
    python viz/basics/choosing/comparison.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, survey                      # noqa: E402

data = survey()

# --- 1. the default, and what is wrong with it -----------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

# Alphabetical order, vertical bars, rotated labels: three small problems.
alphabetical = data.sort_values("tool")
left.bar(alphabetical["tool"], alphabetical["users"])
left.set_title("Default: alphabetical, labels fighting for room")
left.tick_params(axis="x", rotation=45)

# Sorted, horizontal, labels readable. Same data, much less work for the eye.
ordered = data.sort_values("users")
right.barh(ordered["tool"], ordered["users"], color="#4C72B0")
right.set_title("Sorted and horizontal: the ranking is now obvious")
right.set_xlabel("users")

fig.tight_layout()
save(fig, __file__, "bars")

# --- 2. why bars must start at zero ----------------------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

left.barh(ordered["tool"], ordered["users"], color="#C44E52")
left.set_xlim(0, 450)
left.set_title("Honest: axis starts at zero")

right.barh(ordered["tool"], ordered["users"], color="#C44E52")
right.set_xlim(300, 430)          # chops the bars off at the bottom
right.set_title("Misleading: axis starts at 300")

fig.suptitle("A bar's LENGTH is the value. Cut the axis and you cut the value.",
             fontsize=11)
fig.tight_layout()
save(fig, __file__, "zero-baseline")

# --- 3. when a dot plot beats a bar ----------------------------------------
# Bars need the zero, so a narrow range wastes most of the picture. A dot is
# read by POSITION, not length, so it can start wherever it likes.
narrow = data[data["users"] > 100].sort_values("users")

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.5))

left.barh(narrow["tool"], narrow["users"], color="#4C72B0")
left.set_title("Bars: honest, but the differences are squashed")

right.hlines(y=narrow["tool"], xmin=narrow["users"].min() - 20,
             xmax=narrow["users"], color="#CCCCCC", lw=1)
right.plot(narrow["users"], narrow["tool"], "o", color="#4C72B0", markersize=9)
right.set_xlim(narrow["users"].min() - 20, narrow["users"].max() + 20)
right.set_title("Dots: read by position, so no zero needed")

fig.tight_layout()
save(fig, __file__, "dot-plot")

print("""
  Choose by the question:
    "which is biggest?"        -> sorted horizontal bars, starting at zero
    "how do these few differ?" -> dot plot, zoomed to the interesting range
""")
