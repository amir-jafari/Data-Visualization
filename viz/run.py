"""
Lesson runner for the visualization course.

    python viz/run.py                    list the lessons, in reading order
    python viz/run.py color/palettes     run one lesson
    python viz/run.py palettes           ...the chapter is optional
    python viz/run.py --all              render everything into viz/output/
    python viz/run.py --all --keep       ...and store the figures IN the
                                         notebooks, so they can be read
                                         without a kernel
    python viz/run.py --strip            clear stored notebook outputs again
    python viz/run.py --clean            delete viz/output/

The lessons are Jupyter notebooks. The normal way to use one is to open it and
run the cells yourself:

    jupyter lab viz/basics/color/palettes.ipynb

This script is for the other case -- rendering everything headlessly, on the
course server or in CI, so the gallery has something to show:

    python viz/run.py --all
    streamlit run viz/project/gallery.py

Executing a notebook here runs it in a real kernel, exactly as opening it
would, and every `save()` inside writes a PNG (or HTML) into viz/output/.
Nothing is written back into the notebook unless you pass --keep.
"""

import shutil
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
        on_disk = {p.stem: p for p in folder.glob("*.ipynb")}
        ordered = [n for n in names if n in on_disk]
        ordered += sorted(n for n in on_disk if n not in names)
        found += [(chapter, name, on_disk[name]) for name in ordered]
    found += [("project", p.stem, p) for p in sorted(PROJECT.glob("*.ipynb"))]
    return found


def show_list():
    print(__doc__.strip().split("\n\n")[0])
    current = None
    for chapter, name, _ in lessons():
        if chapter != current:
            current = chapter
            print(f"\n  {chapter}  --  {BLURB.get(chapter, 'the capstone')}")
        print(f"      {chapter}/{name}")
    print("\nOpen one:     jupyter lab viz/basics/choosing/comparison.ipynb")
    print("Render one:   python viz/run.py choosing/comparison")
    print("Render all:   python viz/run.py --all")


def run(path, keep=False):
    """Execute one notebook in a real kernel. Returns True if it finished."""
    try:
        import nbformat
        from nbclient import NotebookClient
    except ModuleNotFoundError:
        print("  nbclient is missing.  pip install -r viz/requirements.txt")
        return False

    notebook = nbformat.read(path, as_version=4)
    # run_path: the kernel's working directory, so the notebook's own
    # "walk up until vizkit.py appears" bootstrap resolves the same way it
    # does when you open the file in Jupyter.
    client = NotebookClient(notebook, timeout=600, kernel_name="python3",
                            resources={"metadata": {"path": str(path.parent)}})
    try:
        client.execute()
    except Exception as error:                       # noqa: BLE001
        print(f"  FAILED: {type(error).__name__}: {str(error)[:400]}")
        return False

    for cell in notebook.cells:
        for out in cell.get("outputs", []):
            if out.get("output_type") == "stream":
                sys.stdout.write(out.get("text", ""))

    if keep:
        nbformat.write(notebook, path)
        print(f"  stored outputs in {path.relative_to(HERE.parent)}")
    return True


def strip():
    import nbformat

    count = 0
    for _, _, path in lessons():
        notebook = nbformat.read(path, as_version=4)
        changed = False
        for cell in notebook.cells:
            if cell.get("outputs") or cell.get("execution_count") is not None:
                cell["outputs"] = []
                cell["execution_count"] = None
                changed = True
        if changed:
            nbformat.write(notebook, path)
            count += 1
    print(f"  cleared stored outputs in {count} notebook(s)")


def main():
    args = sys.argv[1:]
    keep = "--keep" in args
    args = [a for a in args if a != "--keep"]

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

    if args[0] == "--strip":
        strip()
        return

    if args[0] == "--all":
        every = lessons()
        failed = []
        for chapter, name, path in every:
            print(f"\n=== {chapter}/{name} ===")
            if not run(path, keep):
                failed.append(f"{chapter}/{name}")
        print(f"\n{len(every) - len(failed)}/{len(every)} lessons rendered.")
        if failed:
            print("  failed: " + ", ".join(failed))
            sys.exit(1)
        print(f"  output in {OUTPUT.relative_to(HERE.parent)}/")
        print("  browse it:  streamlit run viz/project/gallery.py")
        return

    target = args[0].removesuffix(".ipynb")
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

    if not run(matches[0][2], keep):
        sys.exit(1)


if __name__ == "__main__":
    main()
