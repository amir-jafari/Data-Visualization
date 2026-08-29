"""
Lesson runner for the visualization course.

    python viz/run.py                    list the lessons, in reading order
    python viz/run.py color/palettes     run one lesson
    python viz/run.py palettes           ...the chapter is optional
    python viz/run.py --all              render everything into viz/output/
    python viz/run.py --clean            delete viz/output/

Every lesson is a plain script you can also run directly:

    python viz/basics/color/palettes.py

They save PNGs (and a few HTML files) into viz/output/ rather than opening a
window, so they work the same over SSH on the course server as they do on a
laptop. To browse the results:

    streamlit run viz/project/gallery.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASICS = HERE / "basics"
PROJECT = HERE / "project"
OUTPUT = HERE / "output"

CHAPTERS = {
    "choosing":    ["comparison", "distribution", "relationship",
                    "change_over_time", "composition"],
    "foundations": ["figure_and_axes", "scales_and_ticks", "subplots_grid",
                    "saving"],
    "color":       ["palettes", "colorblind", "rainbow"],
    "annotation":  ["direct_labels", "highlight", "titles"],
    "layout":      ["small_multiples", "chart_junk"],
    "misleading":  ["truncated_axis", "dual_axis", "area_vs_radius",
                    "cherry_picking"],
    "interactive": ["when_interactive", "plotly_basics", "altair_basics"],
    "networks":    ["networkx_basics", "pyvis_interactive"],
}

BLURB = {
    "choosing":    "which chart answers which question",
    "foundations": "matplotlib's actual mechanics",
    "color":       "palettes, colour blindness, and why rainbow lies",
    "annotation":  "labels, highlighting, and titles that say something",
    "layout":      "small multiples, and removing everything that is not data",
    "misleading":  "how charts lie -- so you can stop doing it by accident",
    "interactive": "plotly and altair, and when interactivity is worth it",
    "networks":    "graphs, where position means nothing unless you say so",
}


def lessons():
    """[(chapter, lesson, path)] in teaching order, plus anything unlisted."""
    found = []
    for chapter, names in CHAPTERS.items():
        folder = BASICS / chapter
        if not folder.is_dir():
            continue
        on_disk = {p.stem: p for p in folder.glob("*.py")}
        ordered = [n for n in names if n in on_disk]
        ordered += sorted(n for n in on_disk if n not in names)
        found += [(chapter, name, on_disk[name]) for name in ordered]
    found += [("project", p.stem, p) for p in sorted(PROJECT.glob("*.py"))
              if p.stem != "gallery"]
    return found


def show_list():
    print(__doc__.strip().split("\n\n")[0])
    current = None
    for chapter, name, _ in lessons():
        if chapter != current:
            current = chapter
            print(f"\n  {chapter}  --  {BLURB.get(chapter, 'the capstone')}")
        print(f"      {chapter}/{name}")
    print(f"\nRun one:      python viz/run.py choosing/comparison")
    print(f"Run them all: python viz/run.py --all")


def run(path):
    result = subprocess.run([sys.executable, str(path)], capture_output=True,
                            text=True)
    sys.stdout.write(result.stdout)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
    return result.returncode == 0


def main():
    args = sys.argv[1:]

    if not args:
        show_list()
        return

    if args[0] == "--clean":
        if OUTPUT.exists():
            shutil.rmtree(OUTPUT)
            print(f"  removed {OUTPUT.relative_to(HERE.parent)}")
        else:
            print("  nothing to clean")
        return

    if args[0] == "--all":
        every = lessons()
        failed = []
        for chapter, name, path in every:
            print(f"\n=== {chapter}/{name} ===")
            if not run(path):
                failed.append(f"{chapter}/{name}")
        print(f"\n{len(every) - len(failed)}/{len(every)} lessons rendered.")
        if failed:
            print("  failed: " + ", ".join(failed))
            sys.exit(1)
        print(f"  output in {OUTPUT.relative_to(HERE.parent)}/")
        print("  browse it:  streamlit run viz/project/gallery.py")
        return

    target = args[0].removesuffix(".py")
    matches = [(c, n, p) for c, n, p in lessons()
               if target in (n, f"{c}/{n}")]

    if not matches:
        print(f"No lesson called {target!r}.\n")
        show_list()
        sys.exit(1)
    if len(matches) > 1:
        print(f"{target!r} is ambiguous: "
              + ", ".join(f"{c}/{n}" for c, n, _ in matches))
        sys.exit(1)

    run(matches[0][2])


if __name__ == "__main__":
    main()
