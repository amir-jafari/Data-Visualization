# 🎈 Learn Streamlit

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.60-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)

Course material for building data apps with **Streamlit** — from `st.title()` to
a working object detector. Every example is a small, runnable file.

Maintained by [Amir Jafari](mailto:ajafari@gwu.edu), The George Washington University.

---

## Start here

```bash
git clone https://github.com/amir-jafari/Data-Visualization.git
cd Data-Visualization

python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

pip install -r requirements.txt
streamlit run app.py
```

Your browser opens at <http://localhost:8501>. Pick a lesson in the sidebar:
the **Demo** tab runs it, the **Source** tab shows the code behind it.

That's the whole setup. Read on when you want to run files individually.

---

## What's in here

| Folder | What it is |
| --- | --- |
| **`app.py`** | The launcher. One command, every lesson. |
| **`01_basics/`** | 57 one-idea-per-file lessons: text, charts, widgets, layout, state. [Details →](01_basics/README.md) |
| **`02_apps/`** | Full apps that combine those pieces: NLP, vision, audio, ML, time series. [Details →](02_apps/README.md) |
| **`s3/`** | Where the data comes from, and the keys to reach it. [Details →](s3/README.md) |

---

## How to work through it

**1. Read a lesson, then change it.** Every file in `01_basics/` is small enough
to read in a minute. Open one, run it, break something, run it again — that
loop is the point.

```bash
streamlit run 01_basics/03_charts/05_matplotlib.py
```

**2. Notice `with st.echo():`.** Most lessons wrap their body in it, so the app
shows you its own source next to its output. Nothing is hidden.

**3. Remember the execution model.** Streamlit re-runs your **entire script**,
top to bottom, on every interaction. There is no callback, no event handler —
a widget just returns its current value. Once that clicks, Streamlit is easy.
See `01_basics/10_state_and_config/04_session_state.py` for the escape hatch
when you need something to survive a re-run.

**4. Move to `02_apps/` when you want a project.** Each one is a `main.py` plus
a `utils.py`, and they need the extra install:

```bash
pip install -r requirements-apps.txt
streamlit run 02_apps/data_mining/classification/main.py
```

---

## Getting the data working

No datasets or images are stored in this repo — they live in S3 and are fetched
at runtime. **Lessons 01–04 need nothing.** Anything that loads a CSV, image,
audio, or video needs AWS keys:

```bash
cp .env.example .env      # then paste your keys into .env at the repo root
```

If an app shows a **"AWS keys need to be updated"** panel, your Learner Lab
session expired: restart the lab, paste the fresh keys into the `[s3]` block
of the repo-root `.env`, and press
the retry button in the app. No restart needed. Full details in
[`s3/README.md`](s3/README.md).

---

## Troubleshooting

**Python version** — Streamlit 1.60 needs **Python 3.10 or newer**. Check with
`python --version` before anything else.

**A lesson says it needs a package** — the launcher tells you which one and gives
you the `pip install` line. That only happens for optional extras; everything in
`requirements.txt` covers the rest.

**`streamlit: command not found`** — your virtual environment isn't active, or
you installed into a different one. Use `python -m streamlit run app.py`.

**Port already in use** — another app is still running. Pick another port:
`streamlit run app.py --server.port 8888`.

---

## License

MIT.
