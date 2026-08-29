"""
The title should say the finding, not name the axes.

"Sales by region, 2024-2025" tells the reader what they are looking at. They
could see that. "West overtook East in March" tells them what to conclude --
which is the reason you drew the chart.

What it shows:
    * descriptive versus declarative titles, side by side
    * a subtitle carrying the detail so the title can carry the point
    * a source note, which is what makes a chart quotable
    * removing chart junk so the message has room

Run it:
    python viz/basics/annotation/titles.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, sales                       # noqa: E402

wide = sales().pivot(index="month", columns="region", values="sales")
crossover = None
for month in wide.index:
    if wide.loc[month, "West"] > wide.loc[month, "East"]:
        crossover = month
        break

# --- 1. descriptive vs declarative -----------------------------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(13, 4.5))

for ax in (left, right):
    for region in wide.columns:
        ax.plot(wide.index, wide[region], color="#D9D9D9", lw=1.5)
    ax.plot(wide.index, wide["West"], color="#0072B2", lw=2.5)
    ax.plot(wide.index, wide["East"], color="#D55E00", lw=2.5)
    ax.tick_params(axis="x", rotation=30, labelsize=8)

left.set_title("Sales by region, 2024-2025")
left.legend(["North", "South", "East", "West"], fontsize=7)

# Declarative: the title states the conclusion, a subtitle holds the detail.
right.set_title(f"West overtook East in {crossover:%B %Y}",
                fontsize=13, fontweight="bold", loc="left")
right.text(0.0, 1.02, "Monthly sales by region, all four regions shown",
           transform=right.transAxes, fontsize=9, color="#666666")
right.annotate("West", xy=(wide.index[-1], wide["West"].iloc[-1]),
               xytext=(6, 0), textcoords="offset points",
               color="#0072B2", fontweight="bold", va="center")
right.annotate("East", xy=(wide.index[-1], wide["East"].iloc[-1]),
               xytext=(6, 0), textcoords="offset points",
               color="#D55E00", fontweight="bold", va="center")
right.set_xlim(wide.index[0], wide.index[-1] + (wide.index[-1] - wide.index[-4]))

fig.tight_layout()
save(fig, __file__, "descriptive-vs-declarative")

# --- 2. the finished article -----------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))

for region in wide.columns:
    ax.plot(wide.index, wide[region], color="#D9D9D9", lw=1.5)
ax.plot(wide.index, wide["West"], color="#0072B2", lw=2.8)
ax.plot(wide.index, wide["East"], color="#D55E00", lw=2.8)

ax.axvline(crossover, color="#999999", lw=1, linestyle="--", zorder=0)
ax.annotate("crossover", xy=(crossover, wide.to_numpy().min()),
            xytext=(6, 4), textcoords="offset points",
            fontsize=8, color="#666666")

for region, colour in [("West", "#0072B2"), ("East", "#D55E00")]:
    ax.annotate(region, xy=(wide.index[-1], wide[region].iloc[-1]),
                xytext=(6, 0), textcoords="offset points",
                color=colour, fontweight="bold", va="center")

# Chart junk removal: no top/right frame, faint horizontal guides only.
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.grid(axis="y", alpha=0.3)
ax.set_axisbelow(True)

ax.set_title(f"West overtook East in {crossover:%B %Y}",
             fontsize=15, fontweight="bold", loc="left", pad=26)
ax.text(0.0, 1.04, "Monthly sales by region. Other regions shown in grey.",
        transform=ax.transAxes, fontsize=10, color="#666666")
ax.set_ylabel("sales ($k)")
ax.set_xlim(wide.index[0], wide.index[-1] + (wide.index[-1] - wide.index[-4]))
fig.text(0.01, -0.02, "Source: vizkit.sales() — synthetic course data",
         fontsize=8, color="#999999")

fig.tight_layout()
save(fig, __file__, "finished")

print("""
  Title  = the finding      ("West overtook East in March")
  Subtitle = the detail     ("Monthly sales by region")
  Source note = credibility (where the numbers came from)
""")
