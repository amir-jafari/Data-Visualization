# basics — one idea per file

Every lesson is a plain Python script. Run it, look at what it saved, then
change a number and run it again.

```bash
python viz/run.py                    # the list, in reading order
python viz/run.py color/palettes     # run one
python viz/run.py --all              # render everything
streamlit run viz/project/gallery.py # browse the results
```

Lessons save PNGs into `viz/output/` instead of opening a window, so they
behave the same over SSH on the course server as on a laptop.

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

`vizkit.py` at the top of `viz/` holds `save()` and the sample datasets. The
data is seeded, so every figure looks identical on every machine — if your
output differs from a classmate's, something is genuinely wrong.

## Naming a new lesson

Don't name a lesson file after a package you can import. A lesson called
`json.py` or `requests.py` ends up on Python's import path and shadows the
real library, and everything breaks confusingly. The Streamlit half of this
repo learned that the hard way — see `streamlit/basics/README.md`.
