"""
Streamlit Course -- lesson launcher.

    streamlit run app.py

Pick a lesson in the sidebar. The "Demo" tab runs the lesson file exactly as if
you had run `streamlit run <that file>` yourself; the "Source" tab shows the
code that produced it, so you can read and run side by side.

Everything the launcher shows lives in 01_basics/. To run a lesson on its own:

    streamlit run 01_basics/03_charts/05_matplotlib.py
"""

import runpy
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
LESSONS = ROOT / "01_basics"

st.set_page_config(page_title="Streamlit Course", page_icon="🎈", layout="wide")


def pretty(name):
    """'03_charts' -> 'Charts';  '05_matplotlib.py' -> 'Matplotlib'."""
    stem = name[:-3] if name.endswith(".py") else name
    _, _, rest = stem.partition("_")
    return rest.replace("_", " ").title()


@st.cache_data
def chapters():
    """{chapter dir: [lesson files]} in numeric filename order."""
    return {
        d: sorted(p for p in d.iterdir() if p.suffix == ".py")
        for d in sorted(LESSONS.iterdir())
        if d.is_dir() and not d.name.startswith("__")
    }


book = chapters()
if not book:
    st.error(f"No lessons found in `{LESSONS}`.")
    st.stop()

# ---------------------------------------------------------------- sidebar ----
st.sidebar.title("🎈 Streamlit Course")
st.sidebar.caption("Run any lesson, then read its source.")

chapter = st.sidebar.radio("Chapter", list(book), format_func=lambda d: pretty(d.name))
lesson = st.sidebar.radio("Lesson", book[chapter], format_func=lambda p: pretty(p.name))

rel = lesson.relative_to(ROOT).as_posix()
st.sidebar.divider()
st.sidebar.caption("Run this one on its own:")
st.sidebar.code(f"streamlit run {rel}", language="bash")

# ------------------------------------------------------------------- body ----
st.caption(f"`{rel}`")

demo_tab, source_tab = st.tabs(["▶️ Demo", "📄 Source"])

with source_tab:
    st.code(lesson.read_text(encoding="utf-8"), language="python")

with demo_tab:
    # The lesson expects to be the main script, and some of them import a
    # sibling module, so put its folder on sys.path first -- same as Streamlit
    # does when you run the file directly.
    sys.path.insert(0, str(lesson.parent))
    try:
        runpy.run_path(str(lesson), run_name="__main__")
    except ModuleNotFoundError as exc:
        # A missing package is a setup problem, not a broken lesson -- say which
        # one and how to get it, instead of showing a traceback.
        st.warning(f"This lesson needs a package you don't have: **{exc.name}**")
        st.caption("Install it, then press R to reload:")
        st.code(f"pip install {exc.name.replace('_', '-')}", language="bash")
    except Exception as exc:  # a broken lesson should not kill the launcher
        if "set_page_config" in str(exc):
            # The launcher already configured the page, so a lesson that calls
            # st.set_page_config() cannot -- it only works once per page.
            st.info("Run this lesson on its own to see it work — see the sidebar.")
        else:
            st.exception(exc)
    finally:
        sys.path.remove(str(lesson.parent))
