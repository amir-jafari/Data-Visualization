"""
Figure and Axes -- the one piece of matplotlib everyone gets confused by.

The words, once and for all:

    Figure  = the sheet of paper. One per picture. It has a size.
    Axes    = one plot ON that paper. A figure can hold many. Confusingly,
              "Axes" (plural word, single object) means ONE plot.
    Axis    = the x or y line itself, with its ticks and label.

So: a Figure holds Axes; an Axes holds two Axis objects.

What it shows:
    * the two styles you will see online, and why to prefer one
    * plt.something() secretly means "the current Axes", which breaks in loops
    * ax.set(...) to set several things at once

Run it:
    python viz/basics/foundations/figure_and_axes.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save                              # noqa: E402

x = np.linspace(0, 10, 200)

# --- 1. the anatomy, labelled ----------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))
# `fig` is the paper. `ax` is the single plot on it.

ax.plot(x, np.sin(x), label="sin(x)")
ax.plot(x, np.cos(x), label="cos(x)")

# ax.set() is shorthand for four separate ax.set_*() calls.
ax.set(xlabel="x", ylabel="value", title="One Figure, one Axes, two lines",
       xlim=(0, 10), ylim=(-1.5, 1.5))
ax.legend()

# Things that belong to the FIGURE, not the axes:
fig.suptitle("fig.suptitle() belongs to the Figure", fontsize=13)

# Leave a margin so the Figure is visible AROUND the Axes, otherwise the
# labels below would point at the wrong thing.
fig.subplots_adjust(left=0.18, right=0.95, top=0.80, bottom=0.22)

# Label each part where it actually is. Figure coordinates (0-1 across the
# whole sheet) for the figure itself; data coordinates with an arrow for the
# parts inside.
fig.text(0.02, 0.02, "everything inside this border is the FIGURE",
         fontsize=9, color="#888888")

ax.annotate("this box is the AXES", xy=(0.02, 0.97), xycoords="axes fraction",
            xytext=(0.30, 1.12), textcoords="axes fraction",
            fontsize=9, color="#C44E52",
            arrowprops=dict(arrowstyle="->", color="#C44E52"))

ax.annotate("this line, with its ticks\nand label, is the x AXIS",
            xy=(6.0, -1.5), xytext=(5.2, -1.15),
            fontsize=9, color="#4C72B0",
            arrowprops=dict(arrowstyle="->", color="#4C72B0"))

save(fig, __file__, "anatomy")

# --- 2. the two styles -----------------------------------------------------
# Style A -- pyplot, "state machine". Every call acts on whatever plot is
# 'current'. Fine for one quick chart, a trap as soon as there are two.
plt.figure(figsize=(5, 3))
plt.plot(x, np.sin(x))
plt.title("pyplot style: plt.plot, plt.title")
plt.xlabel("x")
save(plt.gcf(), __file__, "style-pyplot")

# Style B -- object oriented. You hold the Axes and say which one you mean.
# Use this. Every other lesson in this folder does.
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(x, np.sin(x))
ax.set(title="object style: ax.plot, ax.set", xlabel="x")
save(fig, __file__, "style-object")

# --- 3. why it matters: many plots at once ---------------------------------
fig, axes = plt.subplots(2, 2, figsize=(9, 6))
# axes is a 2x2 numpy array of Axes objects. Flatten it to loop.

functions = [("sin", np.sin), ("cos", np.cos),
             ("exp(-x/3)", lambda v: np.exp(-v / 3)), ("sqrt", np.sqrt)]

for ax, (name, func) in zip(axes.flat, functions):
    ax.plot(x, func(x), color="#4C72B0")
    ax.set_title(name)          # unambiguous: THIS axes
    ax.grid(alpha=0.3)

fig.suptitle("With four plots, 'the current one' stops being a useful idea",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "many-axes")

print("""
  Figure = the paper.  Axes = one plot on it.  Axis = the x or y line.
  Start every chart with:   fig, ax = plt.subplots()
  and you will never wonder what plt.title() is talking to.
""")
