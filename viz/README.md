# 📊 Learn Data Visualization

The course's namesake. [`streamlit/`](../streamlit/) teaches the app,
[`fastapi/`](../fastapi/) teaches the service — this teaches the **chart**:
which one to draw, how to draw it properly, and how to avoid lying by accident.

Half library mechanics, half design judgement, because you need both.

---

## Start here

```bash
pip install -r viz/requirements.txt     # should install nothing; it is all there

python viz/run.py                       # the lessons, in reading order
python viz/run.py choosing/comparison   # run the first one
python viz/run.py --all                 # render all 27
streamlit run viz/project/gallery.py    # browse the results
```

Lessons save PNGs into `viz/output/` rather than opening a window, so they work
identically over SSH and on a laptop. `viz/output/` is git-ignored — regenerate
it with `--all`.

---

## What's in here

| | |
| --- | --- |
| **[`CONCEPTS.md`](CONCEPTS.md)** | **The ideas in plain words** — analogies, what to demo live, what students get wrong. Start here if you are teaching it. |
| **`run.py`** | Lists the lessons and renders one, or all of them. |
| **`vizkit.py`** | `save()` and the seeded sample data every lesson shares. |
| **`basics/`** | 25 one-idea-per-file lessons in 8 chapters. [Details →](basics/README.md) |
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
talking about, and grey the rest. `annotation/highlight.py` tells three
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

**Nothing appears when I run a lesson** — that is expected. They save files.
Read the printed path, or run `streamlit run viz/project/gallery.py`.

**My figure looks different from the lesson's** — it should not. The sample
data is seeded. Check you have not edited `vizkit.py`.

**`ModuleNotFoundError: vizkit`** — run the lesson as a file
(`python viz/basics/color/palettes.py`) or through `viz/run.py`. The lessons
add `viz/` to the path themselves; copying a snippet elsewhere will not.

**The gallery says nothing is rendered** — run `python viz/run.py --all` first.
