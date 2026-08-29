"""
Streamlit Course -- launcher.

    streamlit run app.py

Pick a lesson from 01_basics/ or an app from 02_apps/ in the sidebar. The
"Demo" tab runs it exactly as if you had run `streamlit run <that file>`
yourself; the "Source" tab shows the code that produced it, so you can read
and run side by side.

Apps in 02_apps/ need the extra requirements:

    pip install -r requirements.txt -r requirements-apps.txt

To run something on its own:

    streamlit run 01_basics/03_charts/05_matplotlib.py
    streamlit run 02_apps/data_mining/classification/main.py
"""

import runpy
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
BASICS = ROOT / "01_basics"
APPS = ROOT / "02_apps"

st.set_page_config(page_title="Streamlit Course", page_icon="🎈", layout="wide")


def pretty(name):
    """'03_charts' -> 'Charts';  '05_matplotlib.py' -> 'Matplotlib';  'data_mining' -> 'Data Mining'."""
    stem = name[:-3] if name.endswith(".py") else name
    head, sep, rest = stem.partition("_")
    if sep and head.isdigit():
        stem = rest
    return stem.replace("_", " ").title()


def purge_local_modules():
    """Drop already-imported course-local modules (utils.py, metrics.py, ...).

    Many lessons/apps import a same-named sibling module (almost every app has
    its own `utils.py`). Python caches imports in sys.modules by name, so
    without this, the *first* app's utils.py would silently keep being served
    to every other app that also does `import utils`. Third-party packages
    live outside ROOT and are untouched, so their cache -- and its speed --
    is preserved.
    """
    root_str = str(ROOT)
    for name, mod in list(sys.modules.items()):
        mod_file = getattr(mod, "__file__", None)
        if mod_file and mod_file.startswith(root_str):
            del sys.modules[name]


@st.cache_data
def basics_chapters():
    """{chapter dir: [lesson files]} in numeric filename order."""
    return {
        d: sorted(p for p in d.iterdir() if p.suffix == ".py")
        for d in sorted(BASICS.iterdir())
        if d.is_dir() and not d.name.startswith("_")
    }


@st.cache_data
def apps_catalog():
    """{category dir: [main.py paths]}, found at any depth under it."""
    result = {}
    for cat in sorted(d for d in APPS.iterdir() if d.is_dir() and not d.name.startswith((".", "_"))):
        mains = sorted(cat.rglob("main.py"))
        if mains:
            result[cat] = mains
    return result


basics = basics_chapters()
apps = apps_catalog()

# ---------------------------------------------------------------- sidebar ----
st.sidebar.title("🎈 Streamlit Course")
st.sidebar.caption("Run any lesson or app, then read its source.")

section = st.sidebar.radio("Section", ["01 — Basics", "02 — Apps"])

if section == "01 — Basics":
    if not basics:
        st.error(f"No lessons found in `{BASICS}`.")
        st.stop()
    chapter = st.sidebar.radio("Chapter", list(basics), format_func=lambda d: pretty(d.name))
    item = st.sidebar.radio("Lesson", basics[chapter], format_func=lambda p: pretty(p.name))
else:
    if not apps:
        st.error(f"No apps found in `{APPS}`.")
        st.stop()
    category = st.sidebar.radio("Category", list(apps), format_func=lambda d: pretty(d.name))
    item = st.sidebar.radio(
        "App",
        apps[category],
        format_func=lambda p: " › ".join(pretty(part) for part in p.parent.relative_to(category).parts),
    )

rel = item.relative_to(ROOT).as_posix()
st.sidebar.divider()
st.sidebar.caption("Run this one on its own:")
st.sidebar.code(f"streamlit run {rel}", language="bash")

# ------------------------------------------------------------------- body ----
st.caption(f"`{rel}`")

demo_tab, source_tab = st.tabs(["▶️ Demo", "📄 Source"])

with source_tab:
    st.code(item.read_text(encoding="utf-8"), language="python")

with demo_tab:
    # The lesson/app expects to be the main script, and some of them import a
    # sibling module (e.g. utils.py), so put its folder on sys.path first --
    # same as Streamlit does when you run the file directly.
    purge_local_modules()
    sys.path.insert(0, str(item.parent))
    try:
        runpy.run_path(str(item), run_name="__main__")
    except ModuleNotFoundError as exc:
        # A missing package is a setup problem, not a broken lesson -- say which
        # one and how to get it, instead of showing a traceback.
        st.warning(f"This needs a package you don't have: **{exc.name}**")
        st.caption("Install it, then press R to reload:")
        st.code(f"pip install {exc.name.replace('_', '-')}", language="bash")
    except Exception as exc:  # a broken lesson/app should not kill the launcher
        if "set_page_config" in str(exc):
            # The launcher already configured the page, so a lesson/app that
            # calls st.set_page_config() cannot -- it only works once per page.
            st.info("Run this on its own to see it work — see the sidebar.")
        else:
            st.exception(exc)
    finally:
        sys.path.remove(str(item.parent))