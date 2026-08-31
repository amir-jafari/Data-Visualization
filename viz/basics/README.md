# basics — one idea per notebook

Every lesson is a Jupyter notebook. Open it, run the cells top to bottom, then
change a number and re-run. Each one has the same shape:

1. **What this is** — the idea, the question the chart answers, the rule.
2. **Setup** — find `vizkit.py`, import, name the lesson.
3. **A section per figure** — markdown saying what to look at, then the code.
4. **Rules of thumb** — the summary worth keeping.
5. **Try it yourself** — three exercises, and an empty cell to work in.

```bash
jupyter lab viz/basics/choosing/comparison.ipynb   # the usual way

python viz/run.py                    # the list, in reading order
python viz/run.py color/palettes     # execute one headlessly
python viz/run.py --all              # render everything
streamlit run viz/project/gallery.py # browse the results
```

Every figure is also written to `viz/output/` as the notebook runs, so the
lessons behave the same over SSH on the course server as on a laptop.

| Chapter | You learn |
| --- | --- |
| `choosing` | Which chart answers which question — comparison, distribution, relationship, change, composition |
| `foundations` | Figure vs Axes, scales and ticks, subplot grids, saving for slides or print |
| `color` | Categorical / sequential / diverging, colour blindness, why rainbow maps lie |
| `annotation` | Direct labels, greying the context, titles that state the finding |
| `layout` | Small multiples, and removing everything that is not data |
| `misleading` | Truncated axes, dual axes, bubble areas, cherry-picked windows and bins |
| `interactive` | Plotly and Altair, and when interactivity is worth its cost |
| `networks` | Graphs — where layout position means nothing unless you give it meaning |

Read them in that order. `choosing` needs almost no code and sets up
everything else; `misleading` only lands once you know the rules it breaks.

## The three ideas the whole folder rests on

**Match the mark to the question.** Length for "how much", position for "where
in the range", angle almost never. Choosing the chart is a decision about the
question, not about taste.

**Colour is your loudest signal — spend it deliberately.** On a group, on a
quantity, or on the one series you are talking about. Never on all ten.

**The chart must not claim more than the data supports.** Every lesson in
`misleading/` is a chart whose numbers are all true.

## A thing worth knowing

`vizkit.py` at the top of `viz/` holds `save()`, `save_html()` and the sample
datasets. The data is seeded, so every figure looks identical on every
machine — if your output differs from a classmate's, something is genuinely
wrong.

`save()` does two things at once: it writes the PNG to `viz/output/` **and**
leaves the figure open so the notebook shows it under the cell. The same call
works when the notebook is executed headlessly by `run.py`, where there is
nothing to show it to.

## Adding a lesson

Copy the nearest notebook and keep its shape — intro, setup, a section per
figure, rules of thumb, exercises. Two things to get right:

**Set `LESSON`** to `"chapter/lesson_name"` in the setup cell. That is what
tells `save()` where the figures belong, and what the gallery groups by.

**Add it to `CHAPTERS`** in `viz/run.py`, or it lands at the end of its
chapter in the listing instead of in teaching order.

**Commit it without stored outputs** — `python viz/run.py --strip` clears
them. A notebook full of base64 PNGs makes for an unreviewable diff.

One naming trap carried over from the script days: don't name a lesson after a
package you can import. A `json` or `requests` lesson shadows the real library
for anything in the same folder. The Streamlit half of this repo learned that
the hard way — see `streamlit/basics/README.md`.
