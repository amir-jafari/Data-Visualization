"""
Saving a figure -- for a slide, a paper, or a web page.

What it shows:
    * figsize is in INCHES, dpi is dots per inch; together they set the pixels
    * text does not scale with the figure, so a shrunk figure has tiny labels
    * PNG for slides and the web, SVG/PDF for print -- and why
    * bbox_inches="tight" to stop matplotlib cropping your labels off

The mistake this prevents: drawing a chart, shrinking it into a slide, and
wondering why nobody in the back row can read the axis.

Run it:
    python viz/basics/foundations/saving.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save, OUTPUT                      # noqa: E402

x = np.linspace(0, 10, 100)


def demo_plot(ax, title):
    ax.plot(x, np.sin(x), label="signal")
    ax.set(xlabel="time (s)", ylabel="amplitude", title=title)
    ax.legend()


# --- 1. size the figure for its destination --------------------------------
# Do NOT draw big and shrink later: the text shrinks with it.
targets = {
    "slide": (10, 5.6),        # 16:9, read from across a room
    "paper-column": (3.5, 2.6),  # a single journal column
    "web": (8, 4.5),
}

for name, size in targets.items():
    fig, ax = plt.subplots(figsize=size)
    demo_plot(ax, f"{name}: figsize={size}")
    save(fig, __file__, name)

# --- 2. what shrinking does to text ----------------------------------------
# Both panels below end up the same width on this page. The left one was drawn
# small; the right one was drawn large and then scaled down. Same code, very
# different readability.
fig, ax = plt.subplots(figsize=(4, 2.5))
demo_plot(ax, "drawn at 4x2.5 inches")
save(fig, __file__, "drawn-small", dpi=160)

fig, ax = plt.subplots(figsize=(16, 10))
demo_plot(ax, "drawn at 16x10, then scaled down")
save(fig, __file__, "drawn-large", dpi=40)     # low dpi = same pixel width

# --- 3. raster vs vector ---------------------------------------------------
fig, ax = plt.subplots(figsize=(6, 3.5))
demo_plot(ax, "same figure, three formats")

folder = OUTPUT / "foundations"
folder.mkdir(parents=True, exist_ok=True)

sizes = {}
for ext in ("png", "svg", "pdf"):
    path = folder / f"saving-formats.{ext}"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    sizes[ext] = path.stat().st_size
plt.close(fig)

for ext, size in sizes.items():
    print(f"  saving-formats.{ext:<4} {size/1024:7.1f} KB")

print(f"""
  Size it for where it is going -- do not draw big and shrink:
    slide         figsize=(10, 5.6), dpi 150+
    paper column  figsize=(3.5, 2.6), and raise the font size
    web           figsize=(8, 4.5), dpi 100-150

  Format:
    PNG  pixels. Slides, web, anything with a photo or a heatmap.
    SVG  shapes. Sharp at any zoom, editable in Illustrator/Inkscape.
    PDF  shapes. What journals want.

  Always: bbox_inches="tight", or your y label ends up outside the image.
""")
