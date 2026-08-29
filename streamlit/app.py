"""
Streamlit Course -- launcher.

    streamlit run streamlit/app.py

Pick a lesson from basics/ or an app from apps/ in the sidebar. It runs
inline, on this same page, exactly as if you had run `streamlit run <that
file>` yourself. Switching to a different lesson/app automatically resets
state left behind by the previous one (imported modules, st.session_state,
GPU memory) -- see reset_between_apps() below. Use the "Clear / stop app"
button in the sidebar to force that same reset by hand at any time.

Apps in apps/ need the extra requirements:

    pip install -r streamlit/requirements.txt -r streamlit/requirements-apps.txt

To run something on its own:

    streamlit run streamlit/basics/charts/matplotlib.py
    streamlit run streamlit/apps/data_mining/classification/main.py
"""

import gc
import runpy
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
BASICS = ROOT / "basics"
APPS = ROOT / "apps"

# The order the course is meant to be read in.
#
# The chapters used to be numbered (01_text, 02_dataframes, ...) and those
# numbers were what put them in order. The numbers are gone from the filenames,
# so the order lives here instead. Anything not listed still appears -- sorted
# alphabetically, after everything that is listed -- so adding a lesson without
# touching this file works, it just lands at the end of its chapter.
CHAPTER_ORDER = [
    "text", "dataframes", "charts", "inputs", "media", "layout", "chat", "status",
    "control_flow", "state_and_config", "extras",
]

LESSON_ORDER = {
    "text": ["title_and_headers", "markdown", "latex"],
    "dataframes": [
        "display_dataframe", "styling", "interactive_table", "data_editor",
        "column_config", "metrics", "json",
    ],
    "charts": [
        "line_chart", "area_chart", "bar_chart", "scatter_chart", "matplotlib",
        "altair", "vega_lite", "plotly", "map",
    ],
    "inputs": [
        "button", "download_button", "checkbox", "toggle", "radio", "selectbox",
        "multiselect", "slider", "select_slider", "text_input", "text_area",
        "number_input", "date_and_time", "file_uploader", "color_picker",
    ],
    "media": ["image", "audio", "video"],
    "layout": [
        "sidebar", "columns", "tabs", "expander", "container", "empty", "popover",
        "dialog",
    ],
    "chat": ["chat_message", "chat_input", "write_stream"],
    "status": ["progress_bar", "spinner", "status_container", "messages"],
    "control_flow": ["stop", "form", "rerun", "fragment"],
    "state_and_config": [
        "page_config", "echo", "help", "session_state", "caching", "page_background",
    ],
    "extras": ["html_tooltip", "drawable_canvas"],
}

st.set_page_config(page_title="Streamlit Course", page_icon="🎈", layout="wide")

# Generic names that both this course's own sibling modules (almost every
# app has a `utils.py`) and a dynamically-loaded third-party tool can use.
# E.g. torch.hub caches the yolov5 repo and its models/common.py does
# `from utils import TryExcept`, expecting *its own* utils/ package -- if
# that name is still cached from our own app's `import utils`, yolov5
# silently gets the wrong module. Purged by name regardless of where they
# live, unlike everything else below which is purged by file location.
GENERIC_MODULE_NAMES = {"utils", "models", "common", "metrics", "hubconf"}


def pretty(name):
    """'charts' -> 'Charts';  'matplotlib.py' -> 'Matplotlib';  'data_mining' -> 'Data Mining'."""
    stem = name[:-3] if name.endswith(".py") else name
    return stem.replace("_", " ").title()


def in_order(names, wanted):
    """`names` arranged to match `wanted`; anything unlisted goes last, A-Z."""
    rank = {name: i for i, name in enumerate(wanted)}
    return sorted(names, key=lambda name: (rank.get(name, len(rank)), name))


def purge_stale_modules():
    """Drop cached modules that could be silently serving the wrong file.

    Almost every app has its own same-named `utils.py`, and Python caches
    imports by name -- without this, the *first* app's utils.py would keep
    being served to every other app that also does `import utils`. Two
    targeted rules, not a blanket reset: course-local files (by location,
    since their names vary) and a short list of generic names third-party
    tools reuse too (by name, since they can live outside the repo -- see
    GENERIC_MODULE_NAMES). A blanket "purge everything imported since the
    launcher started" was tried and rejected: it also forces heavy
    C-extension libraries like numpy to reimport on every switch, which numpy
    itself warns can cause subtle issues -- worse than the bug it fixed.
    """
    root_str = str(ROOT)
    for name in list(sys.modules):
        if name == "__main__":
            continue  # this launcher script itself -- runpy needs it intact
        if name in GENERIC_MODULE_NAMES:
            del sys.modules[name]
            continue
        mod_file = getattr(sys.modules[name], "__file__", None)
        if mod_file and mod_file.startswith(root_str):
            del sys.modules[name]


def reset_between_apps():
    """Clear per-demo state: st.session_state and any GPU memory it pinned.

    st.session_state is one shared dict for the whole page, so a previous
    demo's chat history, widget state, or a model it stashed in
    st.session_state would otherwise silently persist into the next demo.
    Also used directly by the sidebar "Clear / stop app" button.
    """
    for key in list(st.session_state.keys()):
        if key != "_launcher_current_item":
            del st.session_state[key]
    torch = sys.modules.get("torch")
    if torch is not None:
        try:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:
            pass
    gc.collect()


@st.cache_data
def basics_chapters():
    """{chapter dir: [lesson files]}, in the order the course should be read."""
    chapters = {d.name: d for d in BASICS.iterdir()
                if d.is_dir() and not d.name.startswith((".", "_"))}

    result = {}
    for name in in_order(chapters, CHAPTER_ORDER):
        directory = chapters[name]
        lessons = {p.stem: p for p in directory.iterdir() if p.suffix == ".py"}
        result[directory] = [lessons[stem]
                             for stem in in_order(lessons, LESSON_ORDER.get(name, []))]
    return result


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

# Relative to the repo root (the parent of this folder), so the command in the
# sidebar can be pasted straight into a shell sitting at the top of the repo.
rel = item.relative_to(ROOT.parent).as_posix()

# Reset automatically when the selection actually changed since the last run.
if st.session_state.get("_launcher_current_item") != rel:
    reset_between_apps()
    st.session_state["_launcher_current_item"] = rel

st.sidebar.divider()
if st.sidebar.button("🗑️ Clear / stop app", width="stretch",
                      help="Reset this app's state (session data, GPU memory) and reload it fresh."):
    reset_between_apps()
    st.rerun()

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
    purge_stale_modules()
    sys.path.insert(0, str(item.parent))
    # The launcher already called st.set_page_config() once for the whole
    # page. Several apps/lessons call it again themselves (it's normally the
    # first line of their script) -- Streamlit only allows one call per page
    # and raises, which would abort the rest of the script before anything
    # else (sidebar widgets included) ever renders. No-op it for the duration
    # of this run so those scripts keep going past that line.
    real_set_page_config = st.set_page_config
    st.set_page_config = lambda *args, **kwargs: None
    try:
        runpy.run_path(str(item), run_name="__main__")
    except ModuleNotFoundError as exc:
        # A missing package is a setup problem, not a broken lesson -- say which
        # one and how to get it, instead of showing a traceback.
        st.warning(f"This needs a package you don't have: **{exc.name}**")
        st.caption("Install it, then press R to reload:")
        st.code(f"pip install {exc.name.replace('_', '-')}", language="bash")
    except Exception as exc:  # a broken lesson/app should not kill the launcher
        st.exception(exc)
    finally:
        st.set_page_config = real_set_page_config
        sys.path.remove(str(item.parent))