"""
A Streamlit gallery for everything the lessons render.

Ties this folder to the Streamlit course: the figures are made by Jupyter
notebooks, and this page just finds and displays them, next to the notebook
that drew each one.

It is a .py file rather than a notebook on purpose -- `streamlit run` wants a
script, and this is the one thing in the folder that is an app rather than a
lesson.

Run it (after rendering at least one lesson):
    python viz/run.py --all
    streamlit run viz/project/gallery.py
"""

import json
import sys
from pathlib import Path

import streamlit as st

VIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(VIZ))

OUTPUT = VIZ / "output"
BASICS = VIZ / "basics"

# Reading order, same as run.py. Chapters not listed appear afterwards, A-Z.
ORDER = ["choosing", "foundations", "color", "annotation", "layout",
         "misleading", "interactive", "networks", "project"]

st.set_page_config(page_title="Visualization gallery", page_icon="📊",
                   layout="wide")


@st.cache_data(show_spinner=False)
def read_notebook(path: Path):
    """(intro markdown, [code cell sources]) from a lesson notebook.

    Reading the JSON directly keeps nbformat off the Streamlit app's
    dependency list -- a notebook is only a dict with a "cells" list.
    """
    cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
    intro = ""
    code_cells = []
    for cell in cells:
        # nbformat writes "source" as either a string or a list of lines.
        source = cell["source"]
        text = "".join(source) if isinstance(source, list) else source
        if cell["cell_type"] == "markdown" and not intro:
            intro = text.strip()
        elif cell["cell_type"] == "code":
            code_cells.append(text.strip())

    # The intro cell opens with the lesson's own "# Title" and closes with a
    # "---" footer pointing back at this page. Both are noise here.
    body = intro.split("\n---\n")[0].split("\n")
    if body and body[0].startswith("# "):
        body = body[1:]
    return "\n".join(body).strip(), code_cells


st.title("📊 Visualization gallery")

if not OUTPUT.exists():
    st.warning("Nothing rendered yet. Run this first:")
    st.code("python viz/run.py --all", language="bash")
    st.stop()

chapters = {d.name: d for d in OUTPUT.iterdir() if d.is_dir()}
ordered = [c for c in ORDER if c in chapters] + sorted(
    c for c in chapters if c not in ORDER)

chapter = st.sidebar.radio("Chapter", ordered,
                           format_func=lambda c: c.replace("_", " ").title())

images = sorted(chapters[chapter].glob("*.png"))
pages = sorted(chapters[chapter].glob("*.html"))

st.sidebar.caption(f"{len(images)} figures, {len(pages)} interactive")
st.sidebar.divider()
st.sidebar.caption("Re-render everything:")
st.sidebar.code("python viz/run.py --all", language="bash")

# Group by the lesson that produced them: "lesson-name.png" -> lesson
lessons: dict[str, list[Path]] = {}
for path in images + pages:
    lesson = path.stem.split("-")[0]
    lessons.setdefault(lesson, []).append(path)

for lesson, files in lessons.items():
    st.subheader(lesson.replace("_", " "))

    source = (BASICS / chapter / f"{lesson}.ipynb")
    if not source.exists():
        source = VIZ / "project" / f"{lesson}.ipynb"

    if source.exists():
        intro, code_cells = read_notebook(source)
        # The notebook's first markdown cell is the lesson -- show it before
        # the pictures.
        if intro:
            st.info(intro)
        with st.expander("Source"):
            st.code("\n\n".join(code_cells), language="python")

    for path in files:
        if path.suffix == ".png":
            # No width= argument on purpose: the figures are already sized
            # for reading, and the spelling of that option changed between
            # Streamlit versions.
            st.image(str(path), caption=path.name)
        else:
            st.caption(f"{path.name} — interactive")
            st.components.v1.html(path.read_text(encoding="utf-8"), height=560,
                                  scrolling=True)

    st.divider()
