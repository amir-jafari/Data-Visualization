"""
The truncated axis -- the most common lie in published charts.

Cut the bottom off a bar chart's y axis and a 3% difference can be made to
look like a 300% one. It is the easiest distortion to produce, the easiest to
spot once you know, and it appears constantly in the wild.

What it shows:
    * the same numbers, honest and exaggerated, with the factor measured
    * the rule: BARS need zero, LINES do not -- and why the rule differs
    * how to zoom in honestly when the small differences really are the story

Run it:
    python viz/basics/misleading/truncated_axis.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save                              # noqa: E402

candidates = ["Ashton", "Barrera", "Chen"]
votes = [51.0, 49.5, 48.8]          # percentages, genuinely close

# --- 1. measure the exaggeration -------------------------------------------
def apparent_ratio(values, bottom):
    """How many times taller does the tallest bar LOOK than the shortest?"""
    heights = [v - bottom for v in values]
    return max(heights) / min(heights)

true_ratio = apparent_ratio(votes, 0)
faked_ratio = apparent_ratio(votes, 48)

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

left.bar(candidates, votes, color="#4C72B0")
left.set_ylim(0, 60)
left.set_title(f"Honest: axis from 0\ntallest looks {true_ratio:.2f}x the shortest",
               fontsize=10)
left.set_ylabel("% of vote")

right.bar(candidates, votes, color="#C44E52")
right.set_ylim(48, 51.5)
right.set_title(f"Truncated: axis from 48\ntallest looks {faked_ratio:.1f}x the shortest",
                fontsize=10)
right.set_ylabel("% of vote")

fig.suptitle("Identical numbers. The right-hand chart exaggerates the gap "
             f"{faked_ratio / true_ratio:.0f}-fold.", fontsize=12)
fig.tight_layout()
save(fig, __file__, "bars-truncated")

# --- 2. why lines are different --------------------------------------------
# A bar says "this much". Its LENGTH is the number, so cutting the length
# changes the number. A line says "it went this way". Its SLOPE is the
# message, and slope survives a shifted baseline.
years = list(range(2015, 2025))
temps = [14.8, 14.9, 15.0, 15.1, 15.0, 15.3, 15.4, 15.5, 15.7, 15.9]

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.8))

left.plot(years, temps, "-o", color="#4C72B0")
left.set_ylim(0, 20)
left.set_title("Line forced to zero: the trend disappears", fontsize=10)
left.set_ylabel("mean temp (C)")

right.plot(years, temps, "-o", color="#4C72B0")
right.set_title("Line at its natural range: the trend is the point", fontsize=10)
right.set_ylabel("mean temp (C)")

fig.suptitle("Bars are read by LENGTH, lines by SLOPE. That is the whole rule.",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "lines-are-different")

# --- 3. zooming in honestly ------------------------------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

left.bar(candidates, votes, color="#C44E52")
left.set_ylim(48, 51.5)
left.set_title("Truncated bars: no", fontsize=10)

# Dots are read by POSITION, so they can start anywhere -- and adding the
# margin of error shows whether the difference means anything at all.
error = 1.5
right.errorbar(votes, candidates, xerr=error, fmt="o", color="#4C72B0",
               capsize=5, markersize=9)
right.set_xlim(46, 54)
right.set_xlabel("% of vote (+/- 1.5 margin of error)")
right.set_title("Dots with error bars: honest, and more informative", fontsize=10)

fig.suptitle("If the small differences ARE the story, change the mark, not the axis",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "honest-zoom")

print(f"""
  Measured on these numbers:
    axis from 0   -> tallest bar looks {true_ratio:.2f}x the shortest  (true ratio: {max(votes)/min(votes):.2f})
    axis from 48  -> tallest bar looks {faked_ratio:.1f}x the shortest
    exaggeration  -> {faked_ratio / true_ratio:.0f}x

  Bars: start at zero, always.
  Lines: any range is fine -- slope is the message.
  Need to show tiny differences? Use dots and error bars.
""")
