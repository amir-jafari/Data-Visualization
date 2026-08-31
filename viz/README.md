# 📊 Learn Data Visualization

The course's namesake. [`streamlit/`](../streamlit/) teaches the app,
[`fastapi/`](../fastapi/) teaches the service — this teaches the **chart**:
which one to draw, how to draw it properly, and how to avoid lying by accident.

Half library mechanics, half design judgement, because you need both.

---

## Start here

The lessons are **Jupyter notebooks**. Open one and run the cells:

```bash
pip install -r viz/requirements.txt          # should install nothing; it is all there

jupyter lab viz/basics/choosing/comparison.ipynb
```

Each notebook explains the idea in markdown, draws the figure in the next cell,
and ends with exercises that ask you to change a number and re-run. That is the
whole method: read, run, break, re-run.

There is also a headless runner, for the course server, for CI, and for
refilling the gallery:

```bash
python viz/run.py                       # the lessons, in reading order
python viz/run.py choosing/comparison   # execute one, without opening it
python viz/run.py --all                 # render all 27
streamlit run viz/project/gallery.py    # browse the results
```

Every notebook also writes its figures into `viz/output/` as it runs, so they
survive outside the notebook and the gallery has something to show.
`viz/output/` is git-ignored — regenerate it with `--all`.

---

## What's in here

| | |
| --- | --- |
| **[`CONCEPTS.md`](CONCEPTS.md)** | **The ideas in plain words** — analogies, what to demo live, what students get wrong. Start here if you are teaching it. |
| **`run.py`** | Lists the notebooks and executes one, or all of them, headlessly. |
| **`vizkit.py`** | `save()`, `save_html()` and the seeded sample data every lesson shares. |
| **`basics/`** | 25 one-idea-per-notebook lessons in 8 chapters. [Details →](basics/README.md) |
| **`project/`** | The makeover: one chart, six steps, plus a Streamlit gallery. [Details →](project/README.md) |

---

## The path through it

**1. `choosing/`** — before any code, which chart answers which question.

**2. `foundations/`** — Figure vs Axes, scales, subplot grids, saving. The
mechanics you need for everything after this.

**3. `color/`, `annotation/`, `layout/`** — the design half. Palettes that
survive colour blindness, labels instead of legends, titles that state a
finding, and removing everything that is not data.

**4. `misleading/`** — the same rules, seen from the other side. Every chart
in this chapter is built from true numbers.

**5. `interactive/` and `networks/`** — Plotly, Altair and graphs, plus an
honest account of when each is worth the trouble.

**6. `project/`** — all of it, on one chart, in six steps.

---

## Three things the folder keeps coming back to

**Match the mark to the question.** Bars are read by length, so they need a
zero. Dots are read by position, so they do not. Angles are read badly, which
is most of the case against pie charts.

**Colour is the loudest signal you have.** Spend it on the one thing you are
talking about, and grey the rest. `annotation/highlight.ipynb` tells three
different stories from one dataset by changing nothing but what is grey.

**The words must match the picture.** The capstone's first title claimed
something the chart itself disproves. That is the most common failure in
student work, and the easiest to fix once you look for it.

---

## How this connects to the rest of the repo

Every chart in `streamlit/apps/` is drawn with matplotlib or plotly, and this
folder is what makes those charts good rather than merely present. The gallery
in `project/` is a Streamlit page, so the two halves meet there.

| Where | What it teaches |
| --- | --- |
| `viz/` | what to draw, and how to draw it honestly |
| `streamlit/` | how to put it in front of a person |
| `fastapi/` | how to serve the data behind it |

---

## Troubleshooting

**No figure appears under a cell** — check the notebook's first code cell ran;
it contains `%matplotlib inline`. If you ran the lesson through `viz/run.py`
instead, nothing was ever meant to appear: it renders into `viz/output/` and
prints the path.

**My figure looks different from the lesson's** — it should not. The sample
data is seeded. Check you have not edited `vizkit.py`.

**`ModuleNotFoundError: vizkit`** — the setup cell finds `viz/` by walking up
from the notebook's own folder until it sees `vizkit.py`, so it only works if
the notebook is still somewhere under `viz/`. Moved it? Set the path yourself.

**`ModuleNotFoundError` for the kernel, not the lesson** — Jupyter is running a
different Python from the one you installed the requirements into. Check with
`import sys; print(sys.executable)` in a cell.

**The gallery says nothing is rendered** — run `python viz/run.py --all` first.

**Git diffs full of base64** — you committed a notebook with its outputs
stored. `python viz/run.py --strip` clears them again.
