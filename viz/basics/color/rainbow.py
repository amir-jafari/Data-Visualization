"""
Why rainbow (jet) colour maps mislead -- measured, not asserted.

A colour map turns numbers into colours. For that to be honest, equal steps in
the DATA must look like equal steps in COLOUR. Rainbow maps fail this badly:
they have bright bands that invent boundaries, and dark stretches that hide
real differences.

What it shows:
    * the same data in jet and in viridis -- jet grows features that are not there
    * lightness plotted along each colour map, which is where jet's problem is
    * a greyscale test: does the map still work in black and white?

Run it:
    python viz/basics/color/rainbow.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save                              # noqa: E402


def lightness(cmap_name, n=256):
    """Perceived lightness along a colour map (0 = black, 100 = white).

    Uses the standard luminance weights for sRGB. A good sequential map rises
    steadily; a rainbow map wanders up and down.
    """
    colours = plt.get_cmap(cmap_name)(np.linspace(0, 1, n))[:, :3]
    return 100 * (0.2126 * colours[:, 0] + 0.7152 * colours[:, 1]
                  + 0.0722 * colours[:, 2])


# --- 1. the same smooth data, two colour maps ------------------------------
# A perfectly smooth ramp. Any structure you see is the colour map's doing.
x = np.linspace(0, 1, 400)
smooth = np.tile(x, (60, 1))

fig, axes = plt.subplots(2, 1, figsize=(10, 3.4))
for ax, cmap in zip(axes, ["jet", "viridis"]):
    ax.imshow(smooth, cmap=cmap, aspect="auto")
    ax.set_title(f"{cmap}: a perfectly linear ramp", fontsize=10, loc="left")
    ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("The data is a straight line. jet invents bands in it.", fontsize=12)
fig.tight_layout()
save(fig, __file__, "linear-ramp")

# --- 2. the lightness curve, which is the actual problem -------------------
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.6))

for cmap in ["jet", "viridis", "Greys"]:
    left.plot(np.linspace(0, 1, 256), lightness(cmap), label=cmap, lw=2)
left.set(xlabel="position in the colour map", ylabel="perceived lightness",
         title="Lightness should climb steadily")
left.legend()

jet_l = lightness("jet")
viridis_l = lightness("viridis")
right.plot(np.linspace(0, 1, 255), np.diff(jet_l), label="jet", lw=1.5)
right.plot(np.linspace(0, 1, 255), np.diff(viridis_l), label="viridis", lw=1.5)
right.axhline(0, color="black", lw=0.8)
right.set(xlabel="position", ylabel="change in lightness",
          title="jet goes UP and DOWN -- crossing zero invents edges")
right.legend()

fig.tight_layout()
save(fig, __file__, "lightness")

# --- 3. real data, and the greyscale test ----------------------------------
yy, xx = np.mgrid[-3:3:200j, -3:3:200j]
field = np.exp(-(xx**2 + yy**2) / 4) + 0.35 * np.sin(3 * xx) * np.cos(3 * yy)

fig, axes = plt.subplots(2, 2, figsize=(9, 7))

axes[0, 0].imshow(field, cmap="jet");     axes[0, 0].set_title("jet")
axes[0, 1].imshow(field, cmap="viridis"); axes[0, 1].set_title("viridis")

# The greyscale test: convert each colour map's lightness only.
for ax, cmap in [(axes[1, 0], "jet"), (axes[1, 1], "viridis")]:
    colours = plt.get_cmap(cmap)(plt.Normalize()(field))[:, :, :3]
    grey = (0.2126 * colours[..., 0] + 0.7152 * colours[..., 1]
            + 0.0722 * colours[..., 2])
    ax.imshow(grey, cmap="gray")
    ax.set_title(f"{cmap}, printed in greyscale")

for ax in axes.flat:
    ax.set_xticks([]); ax.set_yticks([])

fig.suptitle("Greyscale test: jet's rings vanish and its middle turns to mush",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "greyscale-test")

drops = int((np.diff(jet_l) < 0).sum())
print(f"""
  Measured on this machine:
    jet's lightness DECREASES at {drops} of 255 steps -- every one of those is
    a place where a bigger number looks darker than a smaller one.
    viridis decreases at {int((np.diff(viridis_l) < 0).sum())} steps.

  Use viridis / magma / cividis for continuous data.
  Keep jet for pretty pictures where nobody has to read a value.
""")
