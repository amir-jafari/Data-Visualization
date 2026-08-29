"""
A Streamlit gallery for everything the lessons render.

Ties this folder to the Streamlit course: the figures are made by plain Python
scripts, and this page just finds and displays them, next to the source that
drew each one.

Run it (after rendering at least one lesson):
    python viz/run.py --all
    streamlit run viz/project/gallery.py
"""

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

    source = (BASICS / chapter / f"{lesson}.py")
    if not source.exists():
        source = VIZ / "project" / f"{lesson}.py"

    if source.exists():
        # The docstring is the lesson -- show it before the pictures.
        text = source.read_text()
        if text.startswith('"""'):
            st.info(text.split('"""')[1].strip())
        with st.expander("Source"):
            st.code(text, language="python")

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
