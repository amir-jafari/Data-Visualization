"""
When interactivity earns its place -- and when it is just showing off.

Interactivity costs something: the reader has to discover it, it does not
survive being printed or pasted into a slide, and it hides information behind
actions people never take. It is worth it only when there is genuinely more
data than a static picture can hold.

Use interactive when:
    * there are more points than pixels, and the reader needs to zoom
    * each point has extra fields worth a tooltip (name, date, id)
    * the reader has their own question -- which subset, which range
    * it lives on a web page, where hovering is natural

Use static when:
    * it is going in a paper, a slide, or a PDF
    * there is ONE finding, and you already know what it is
    * the reader is being shown, not exploring

The honest test: if the finding only appears after someone hovers, the chart
has not made its point.

What it shows:
    * one dataset as a static "here is the answer" chart
    * the same as an exploratory chart, and what each is good for

Run it:
    python viz/basics/interactive/when_interactive.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, students                    # noqa: E402

data = students()

fig, (left, right) = plt.subplots(1, 2, figsize=(12, 4.2))

# Static, declarative: one finding, stated, no interaction required.
morning = data[data["group"] == "morning"]
evening = data[data["group"] == "evening"]
left.scatter(evening["hours"], evening["score"], s=16, color="#D9D9D9")
left.scatter(morning["hours"], morning["score"], s=16, color="#0072B2")
left.set_title("Static: 'morning students score higher at every study level'",
               fontsize=10, loc="left")
left.set(xlabel="hours studied", ylabel="exam score")

# Exploratory: everything shown, no claim made. Fine as a starting point --
# but do not hand this to an audience and call it a finding.
right.scatter(data["hours"], data["score"], s=16, c=(data["group"] == "morning"),
              cmap="coolwarm", alpha=0.7)
right.set_title("Exploratory: everything, no argument", fontsize=10, loc="left")
right.set(xlabel="hours studied", ylabel="exam score")

fig.suptitle("Explore interactively. Present statically.", fontsize=12)
fig.tight_layout()
save(fig, __file__, "explore-vs-present")

print("""
  Interactive earns its place when the reader has their own question.
  If YOU know the finding, say it in a static chart and stop making them work.
""")
