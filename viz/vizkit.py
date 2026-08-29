"""
Shared helpers for the visualization lessons.

Two jobs only:

  * save(fig, __file__)  -- put a figure in viz/output/, so it works over SSH
    on a headless server where plt.show() draws nothing
  * sample data          -- small, seeded, offline tables, so every lesson
    produces the same picture on every machine, every time

Lessons import it with the same four lines the Streamlit apps use:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from vizkit import save, sales
"""

from pathlib import Path

import matplotlib

# Agg draws to a file instead of a window. Set before pyplot is imported, so
# a lesson never dies with "no display" on the course server.
matplotlib.use("Agg")

import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                       # noqa: E402
import pandas as pd                      # noqa: E402

VIZ_ROOT = Path(__file__).resolve().parent
OUTPUT = VIZ_ROOT / "output"


def save(fig, source_file, name=None, dpi=110, crop=True):
    """Save `fig` under viz/output/<chapter>/<lesson>[-name].png and say where.

    `source_file` is the lesson's own __file__, so the output mirrors the
    lesson tree and you can always tell which script drew which picture.

    crop=True passes bbox_inches="tight" to savefig, which grows the saved
    image to fit anything hanging outside the axes -- a legend parked to the
    right, for instance. That is usually what you want, which is why it is the
    default. Pass crop=False when you deliberately want to SHOW a layout
    problem, as foundations/subplots_grid.py does.
    """
    source = Path(source_file).resolve()
    chapter = source.parent.name
    stem = source.stem if name is None else f"{source.stem}-{name}"

    folder = OUTPUT / chapter
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{stem}.png"

    fig.savefig(path, dpi=dpi, bbox_inches="tight" if crop else None)
    plt.close(fig)

    print(f"  saved  {path.relative_to(VIZ_ROOT.parent)}")
    return path


def save_html(chart, source_file, name=None):
    """Same idea as save(), for things that are HTML rather than pixels.

    Plotly figures, Altair charts and PyVis networks are interactive, so a PNG
    would throw away the point of them. Open the saved file in a browser.
    """
    source = Path(source_file).resolve()
    folder = OUTPUT / source.parent.name
    folder.mkdir(parents=True, exist_ok=True)
    stem = source.stem if name is None else f"{source.stem}-{name}"
    path = folder / f"{stem}.html"

    # Dispatch on the library, not on which methods happen to exist: plotly
    # figures and pyvis networks BOTH have .write_html, with different
    # signatures, so duck-typing picks the wrong one.
    module = type(chart).__module__.split(".")[0]

    if module == "plotly":
        chart.write_html(path, include_plotlyjs="cdn")
    elif module == "pyvis":
        chart.write_html(str(path), notebook=False, open_browser=False)
    elif module == "altair":
        chart.save(str(path))
    else:
        raise TypeError(f"Don't know how to save a {module}.{type(chart).__name__}")

    print(f"  saved  {path.relative_to(VIZ_ROOT.parent)}   (open in a browser)")
    return path


# --------------------------------------------------------------------------- #
# sample data -- seeded, so the figures never change under you
# --------------------------------------------------------------------------- #
def sales(seed=0):
    """Monthly sales for four regions over two years."""
    rng = np.random.default_rng(seed)
    months = pd.date_range("2024-01-01", periods=24, freq="MS")
    base = {"North": 120, "South": 90, "East": 60, "West": 45}
    growth = {"North": 0.4, "South": 1.8, "East": 0.2, "West": 2.6}

    rows = []
    for region, start in base.items():
        trend = start + growth[region] * np.arange(24)
        season = 8 * np.sin(np.arange(24) / 12 * 2 * np.pi)
        noise = rng.normal(0, 4, 24)
        rows.append(pd.DataFrame({"month": months, "region": region,
                                  "sales": trend + season + noise}))
    return pd.concat(rows, ignore_index=True)


def temperatures(seed=1):
    """Daily temperature for one year -- for distributions and time series."""
    rng = np.random.default_rng(seed)
    days = pd.date_range("2024-01-01", periods=365, freq="D")
    seasonal = 12 + 12 * np.sin((np.arange(365) - 100) / 365 * 2 * np.pi)
    return pd.DataFrame({"date": days,
                         "temp_c": seasonal + rng.normal(0, 2.5, 365)})


def students(seed=2, n=200):
    """Study hours vs exam score, with a group -- for scatter and grouping."""
    rng = np.random.default_rng(seed)
    hours = rng.gamma(4, 1.6, n)
    group = rng.choice(["morning", "evening"], n)
    bonus = np.where(group == "morning", 4, 0)
    score = 45 + 4.2 * hours + bonus + rng.normal(0, 7, n)
    return pd.DataFrame({"hours": hours, "score": score.clip(0, 100),
                         "group": group})


def survey(seed=3):
    """Counts by category -- for bars, and for the pie-chart argument."""
    return pd.DataFrame({
        "tool": ["Python", "R", "Excel", "SQL", "Julia", "SAS"],
        "users": [412, 168, 355, 291, 34, 27],
    })


def two_series(seed=4):
    """Two quantities on very different scales -- for the dual-axis lesson."""
    rng = np.random.default_rng(seed)
    months = pd.date_range("2024-01-01", periods=36, freq="MS")
    revenue = 200 + 6 * np.arange(36) + rng.normal(0, 12, 36)
    headcount = 12 + 0.35 * np.arange(36) + rng.normal(0, 0.8, 36)
    return pd.DataFrame({"month": months, "revenue_k": revenue,
                         "headcount": headcount})
