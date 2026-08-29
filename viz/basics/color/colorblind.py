"""
Colour vision deficiency -- and how to check instead of hoping.

About 1 in 12 men and 1 in 200 women see colour differently. Red-green
confusion (deuteranopia and protanopia) is by far the most common. If your
chart's meaning lives in the difference between red and green, those readers
get nothing.

What it shows:
    * a simulation of how a palette looks with each kind of CVD
    * matplotlib's default tab10 measured -- which pairs actually collide
    * Okabe-Ito measured the same way. Better, but read the numbers: it is
      clean for deuteranopia (the common case) and still has collisions for
      tritanopia (the rare one). No palette is safe for everything.
    * which is exactly why colour must never be the ONLY channel

The simulation is the standard Viénot-Brettel-Mollon approximation. It is a
teaching tool, not a clinical one -- but it is far better than guessing.

Run it:
    python viz/basics/color/colorblind.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save                              # noqa: E402

# --- the simulation --------------------------------------------------------
RGB_TO_LMS = np.array([[17.8824, 43.5161, 4.11935],
                       [3.45565, 27.1554, 3.86714],
                       [0.0299566, 0.184309, 1.46709]])
LMS_TO_RGB = np.linalg.inv(RGB_TO_LMS)

PROJECTIONS = {
    "protanopia":   np.array([[0, 2.02344, -2.52581], [0, 1, 0], [0, 0, 1]]),
    "deuteranopia": np.array([[1, 0, 0], [0.494207, 0, 1.24827], [0, 0, 1]]),
    "tritanopia":   np.array([[1, 0, 0], [0, 1, 0], [-0.395913, 0.801109, 0]]),
}


def simulate(colour, kind):
    """One RGB colour (0-1), as a person with `kind` would see it."""
    rgb = np.array(to_rgb(colour)) * 255
    lms = RGB_TO_LMS @ rgb
    seen = LMS_TO_RGB @ (PROJECTIONS[kind] @ lms)
    return np.clip(seen / 255, 0, 1)


def confusable_pairs(palette, kind, threshold=0.18):
    """Which pairs become hard to tell apart? Distance in RGB, roughly."""
    seen = [simulate(c, kind) for c in palette]
    pairs = []
    for i in range(len(seen)):
        for j in range(i + 1, len(seen)):
            distance = float(np.linalg.norm(seen[i] - seen[j]))
            if distance < threshold:
                pairs.append((i, j, distance))
    return pairs


# --- 1. see the difference -------------------------------------------------
TAB10 = list(plt.get_cmap("tab10").colors)[:6]
# Okabe-Ito: designed for colour vision deficiency, and widely recommended.
SAFE = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00"]

fig, axes = plt.subplots(2, 4, figsize=(13, 4))

for row, (palette, name) in enumerate([(TAB10, "matplotlib tab10"),
                                       (SAFE, "Okabe-Ito (CVD-safe)")]):
    for col, kind in enumerate(["normal"] + list(PROJECTIONS)):
        ax = axes[row, col]
        # imshow wants RGB triples, not "#0072B2" strings.
        shown = ([to_rgb(c) for c in palette] if kind == "normal"
                 else [simulate(c, kind) for c in palette])
        ax.imshow([shown], aspect="auto")
        ax.set_xticks([]); ax.set_yticks([])
        if row == 0:
            ax.set_title(kind, fontsize=10)
        if col == 0:
            ax.set_ylabel(name, fontsize=9)

fig.suptitle("The same two palettes, as four different readers see them", fontsize=12)
fig.tight_layout()
save(fig, __file__, "palettes-simulated")

# --- 2. measure it, do not eyeball it --------------------------------------
print("  colours that become hard to tell apart (RGB distance < 0.18):")
for palette, name in [(TAB10, "tab10"), (SAFE, "Okabe-Ito")]:
    print(f"\n    {name}")
    for kind in PROJECTIONS:
        pairs = confusable_pairs(palette, kind)
        if pairs:
            detail = ", ".join(f"{i}&{j} ({d:.2f})" for i, j, d in pairs)
            print(f"      {kind:<13} {len(pairs)} collision(s): {detail}")
        else:
            print(f"      {kind:<13} none")

# --- 3. colour should never be the only channel ----------------------------
x = np.linspace(0, 10, 100)
series = {"control": np.sin(x), "treatment": np.sin(x) + 0.6,
          "placebo": np.sin(x) - 0.6}
risky = ["#D62728", "#2CA02C", "#8C564B"]        # red / green / brown

fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))

for (name, values), colour in zip(series.items(), risky):
    axes[0].plot(x, values, color=colour, label=name, lw=2)
axes[0].legend(); axes[0].set_title("Colour only", fontsize=10)

for (name, values), colour in zip(series.items(), risky):
    axes[1].plot(x, values, color=simulate(colour, "deuteranopia"), label=name, lw=2)
axes[1].legend(); axes[1].set_title("...as deuteranopia sees it", fontsize=10)

for (name, values), colour, style, marker in zip(
        series.items(), SAFE, ["-", "--", ":"], ["o", "s", "^"]):
    axes[2].plot(x, values, color=colour, label=name, lw=2,
                 linestyle=style, marker=marker, markevery=15, markersize=5)
axes[2].legend(); axes[2].set_title("Colour + line style + marker", fontsize=10)

fig.suptitle("If colour is the only difference, some readers see one chart",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "redundant-encoding")

print("""
  Read those numbers again: Okabe-Ito is clean for deuteranopia -- the most
  common kind -- but still collides for tritanopia. There is no palette that
  is safe for every reader, which is the real argument for the third figure.

  Rules:
    do not put meaning in red-vs-green alone
    use Okabe-Ito for categories, viridis for continuous data
    add a second channel: line style, marker, direct labels
    print it in greyscale -- if it still works, it works for everyone
""")
