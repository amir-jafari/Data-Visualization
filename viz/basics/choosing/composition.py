"""
Parts of a whole -- and why the pie chart is usually the wrong answer.

The question this chart answers: "how does the total split up?"

What it shows:
    * people compare angles badly and lengths well -- so bars beat pies
    * a pie is defensible for 2-3 slices where the split is the whole point
    * for parts over time, use lines or a 100% stacked bar, not many pies
    * always say what the total is; percentages without an N mislead

Run it:
    python viz/basics/choosing/composition.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, survey                      # noqa: E402

data = survey().sort_values("users", ascending=False)
total = data["users"].sum()

# --- 1. the same numbers, both ways ----------------------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.2))

left.pie(data["users"], labels=data["tool"], autopct="%1.0f%%", startangle=90)
left.set_title("Pie: rank SQL against Excel without reading the numbers")

ordered = data.sort_values("users")
bars = right.barh(ordered["tool"], ordered["users"], color="#4C72B0")
right.bar_label(bars, fmt="%d", padding=3, fontsize=9)
right.set_xlim(0, ordered["users"].max() * 1.15)
right.set_title(f"Bars: instant ranking  (n = {total:,})")
right.set_xlabel("users")

fig.tight_layout()
save(fig, __file__, "pie-vs-bar")

# --- 2. the one case a pie is fine -----------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))

axes[0].pie([62, 38], labels=["passed", "failed"], autopct="%1.0f%%",
            colors=["#55A868", "#C44E52"], startangle=90)
axes[0].set_title("Two slices: fine.\nThe split IS the message")

axes[1].pie([31, 24, 22, 12, 7, 4], autopct="%1.0f%%", startangle=90,
            labels=list("ABCDEF"))
axes[1].set_title("Six slices: already hard")

many = np.array([14, 12, 11, 10, 9, 9, 8, 7, 6, 5, 4, 3, 2])
axes[2].pie(many, startangle=90)
axes[2].set_title("Thirteen slices: decoration,\nnot information")

fig.tight_layout()
save(fig, __file__, "pie-slices")

# --- 3. parts that change over time ----------------------------------------
years = np.arange(2018, 2025)
shares = {
    "Python": np.array([28, 31, 35, 39, 43, 46, 49]),
    "R":      np.array([24, 23, 21, 19, 17, 16, 15]),
    "Excel":  np.array([33, 31, 29, 27, 25, 23, 21]),
    "Other":  np.array([15, 15, 15, 15, 15, 15, 15]),
}

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

bottom = np.zeros(len(years))
for name, values in shares.items():
    left.bar(years, values, bottom=bottom, label=name)
    bottom += values
left.set_title("100% stacked bar: good for the whole, poor for each part")
left.legend(fontsize=8, loc="lower left")
left.set_ylabel("% of respondents")

for name, values in shares.items():
    right.plot(years, values, "-o", label=name, markersize=4)
right.set_title("Lines: each part's own trend is readable")
right.legend(fontsize=8)
right.set_ylabel("% of respondents")

fig.tight_layout()
save(fig, __file__, "parts-over-time")

print("""
  Parts of a whole:
    2-3 parts, split is the point     -> a pie is fine
    ranking parts                     -> sorted bars
    parts changing over time          -> lines, one per part
    always show the total (n = ...)
""")
