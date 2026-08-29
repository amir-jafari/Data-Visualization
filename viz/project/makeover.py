"""
The makeover -- one dataset, one question, six deliberate steps.

Everything in basics/ applied in order to a single chart, so you can see each
decision change the picture. Each step is saved separately, and the last
figure puts all six side by side.

The question: do students who study more score higher, and does the morning
group differ from the evening group?

The steps, and where each one comes from:

    1  default          what matplotlib gives you           foundations/
    2  labelled         axes, units, a title                annotation/titles
    3  readable         overplotting fixed                  choosing/relationship
    4  coloured         a palette that survives CVD         color/
    5  focused          grey the context, colour the point  annotation/highlight
    6  finished         declarative title, source, no junk  layout/chart_junk

Run it:
    python viz/project/makeover.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vizkit import save, students                    # noqa: E402

data = students()
morning = data[data["group"] == "morning"]
evening = data[data["group"] == "evening"]

BLUE, ORANGE, GREY = "#0072B2", "#D55E00", "#D9D9D9"


def fit(frame):
    slope, intercept = np.polyfit(frame["hours"], frame["score"], 1)
    xs = np.linspace(data["hours"].min(), data["hours"].max(), 50)
    return xs, slope * xs + intercept, slope


# --- step 1: the default ---------------------------------------------------
def step1(ax):
    ax.scatter(data["hours"], data["score"])
    ax.set_title("1. default")


# --- step 2: say what it is ------------------------------------------------
def step2(ax):
    ax.scatter(data["hours"], data["score"])
    ax.set(xlabel="hours studied per week", ylabel="exam score (0-100)",
           title="2. labelled")


# --- step 3: fix the overplotting ------------------------------------------
def step3(ax):
    ax.scatter(data["hours"], data["score"], s=18, alpha=0.55,
               edgecolor="none")
    ax.set(xlabel="hours studied per week", ylabel="exam score (0-100)",
           title="3. readable")


# --- step 4: colour that means something -----------------------------------
def step4(ax):
    ax.scatter(evening["hours"], evening["score"], s=18, alpha=0.6,
               color=ORANGE, label="evening")
    ax.scatter(morning["hours"], morning["score"], s=18, alpha=0.6,
               color=BLUE, label="morning")
    ax.legend(title="group")
    ax.set(xlabel="hours studied per week", ylabel="exam score (0-100)",
           title="4. coloured (Okabe-Ito)")


# --- step 5: focus on the finding ------------------------------------------
def step5(ax):
    ax.scatter(evening["hours"], evening["score"], s=18, alpha=0.5, color=GREY)
    ax.scatter(morning["hours"], morning["score"], s=18, alpha=0.65, color=BLUE)

    for frame, colour in ((evening, "#999999"), (morning, BLUE)):
        xs, ys, _ = fit(frame)
        ax.plot(xs, ys, color=colour, lw=2)

    ax.set(xlabel="hours studied per week", ylabel="exam score (0-100)",
           title="5. focused")


# --- step 6: the finished article ------------------------------------------
def step6(ax, full=False):
    ax.scatter(evening["hours"], evening["score"], s=20, alpha=0.5, color=GREY)
    ax.scatter(morning["hours"], morning["score"], s=20, alpha=0.7, color=BLUE)

    gaps = []
    for frame, colour, name in ((evening, "#AAAAAA", "evening"),
                                (morning, BLUE, "morning")):
        xs, ys, slope = fit(frame)
        ax.plot(xs, ys, color=colour, lw=2.5)
        ax.annotate(name, xy=(xs[-1], ys[-1]), xytext=(6, 0),
                    textcoords="offset points", color=colour,
                    fontweight="bold", va="center", fontsize=10)
        gaps.append(ys)

    # The two groups get their own fitted line, so the gap between them is NOT
    # a single number -- it widens as study hours rise. Reporting the average
    # gap would hide exactly the thing the picture is showing.
    gap = gaps[1] - gaps[0]
    gap_low, gap_high = float(gap[0]), float(gap[-1])

    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_xlim(data["hours"].min() - 0.5, data["hours"].max() + 2.5)

    if full:
        # Scores cannot exceed 100 -- you can see them piling up on that
        # ceiling. A straight line does not know that, and happily predicts
        # 128. Draw the ceiling so the reader can see the fit leaving reality.
        ax.axhline(100, color="#BBBBBB", lw=1, linestyle="--", zorder=0)
        ax.annotate("maximum possible score", xy=(data["hours"].min(), 100),
                    xytext=(0, 4), textcoords="offset points",
                    fontsize=8, color="#999999")
        ax.set_ylim(top=118)

        # The title I first wrote here was "morning students score 9 points
        # higher at every level of study". The chart disproves it: the lines
        # are not parallel. Write the title from the picture, not from the
        # summary statistic you happened to compute.
        ax.set_title("Morning students pull further ahead the more they study",
                     fontsize=15, fontweight="bold", loc="left", pad=26)
        ax.text(0.0, 1.04,
                f"{len(data)} students. The gap grows from ~{gap_low:.0f} points "
                f"at low study hours to ~{gap_high:.0f} at high. "
                f"Lines are least-squares fits within each group.",
                transform=ax.transAxes, fontsize=9.5, color="#666666")
    else:
        ax.set_title("6. finished")

    ax.set(xlabel="hours studied per week", ylabel="exam score (0-100)")
    return gap_low, gap_high


# --- render each step on its own -------------------------------------------
steps = [step1, step2, step3, step4, step5]
for i, step in enumerate(steps, start=1):
    fig, ax = plt.subplots(figsize=(5, 3.6))
    step(ax)
    save(fig, __file__, f"step{i}")

fig, ax = plt.subplots(figsize=(9, 5.5))
gap_low, gap_high = step6(ax, full=True)
fig.text(0.01, -0.02, "Source: vizkit.students() — synthetic course data",
         fontsize=8, color="#999999")
fig.tight_layout()
save(fig, __file__, "step6")

# --- all six together ------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
for ax, step in zip(axes.flat, steps + [step6]):
    step(ax)
fig.suptitle("The same data and the same question, six decisions apart",
             fontsize=14)
fig.tight_layout()
save(fig, __file__, "all-steps")

# One model with a shared slope and a group offset -- the estimate you would
# actually report, as opposed to the average distance between two free lines.
design = np.column_stack([np.ones(len(data)), data["hours"],
                          (data["group"] == "morning").astype(float)])
offset = np.linalg.lstsq(design, data["score"], rcond=None)[0][2]
morning_hours = morning["hours"].mean()
evening_hours = evening["hours"].mean()
_slope, _intercept = np.polyfit(morning["hours"], morning["score"], 1)
ceiling_pred = _slope * data["hours"].max() + _intercept

print(f"""
  The finding, measured: the gap runs from about {gap_low:.0f} points at low
  study hours to about {gap_high:.0f} at high. Fitting one line with a shared
  slope and a group offset instead gives {offset:+.1f} points.

  Three warnings this chart earns, none of them visible in step 1:

    * the fitted lines are NOT parallel, so there is no single "morning
      advantage" to quote. A title saying "X points higher" would be wrong.
    * morning students also studied more on average ({morning_hours:.1f} h vs
      {evening_hours:.1f} h), so group and hours are tangled together. This
      chart cannot separate the two.
    * scores are capped at 100 and are piling up on that ceiling, so the
      straight-line fits are wrong at the top -- they predict {ceiling_pred:.0f}.

  Step 1 contains the data. Step 6 communicates a finding -- and the job is
  not finished until the words match what the picture actually supports.
""")
