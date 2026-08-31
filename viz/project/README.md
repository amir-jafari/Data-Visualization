# project — the makeover

One dataset, one question, and every idea from `basics/` applied in six
visible steps.

```bash
jupyter lab viz/project/makeover.ipynb   # the six steps, one cell each
python viz/run.py project/makeover       # or render them headlessly
streamlit run viz/project/gallery.py     # browse everything, with the source
```

## The question

*Do students who study more score higher, and does the morning group differ
from the evening group?*

## The six steps

| Step | What changed | Chapter it came from |
| --- | --- | --- |
| 1 default | what matplotlib gives you | `foundations/` |
| 2 labelled | axes, units, a title | `annotation/titles` |
| 3 readable | overplotting fixed with alpha | `choosing/relationship` |
| 4 coloured | a palette that survives colour blindness | `color/` |
| 5 focused | one group coloured, the other greyed | `annotation/highlight` |
| 6 finished | declarative title, source note, no chart junk | `layout/chart_junk` |

Step 1 already contains the finding. Nothing was added to the data — only
decisions about how to show it.

## The part worth teaching

The first title on step 6 was *"morning students score 9 points higher at
every level of study."* Every word of it felt reasonable, and the chart
disproves it:

- **The lines are not parallel.** The gap runs from about 4 points at low
  study hours to about 13 at high, so there is no single number to quote.
- **The groups differ in more than one way.** Morning students also studied
  more on average (6.8 h vs 5.8 h), so group and hours are tangled together
  and this chart cannot separate them.
- **Scores are capped at 100** and are piling up on that ceiling, so the
  straight-line fits predict 127 — which is impossible.

The notebook prints all three in its last cell. The finished chart draws the
ceiling so you can watch the fit leave reality.

That is the real lesson of the folder: a beautiful chart with an overclaiming
title is worse than an ugly one, because people believe it.

## The gallery

`gallery.py` is a Streamlit page that finds everything under `viz/output/`,
groups it by lesson, and shows each figure next to the notebook that produced
it — the intro markdown as a caption, the code cells in an expander. It is
also a small demonstration of the two courses meeting: notebooks make the
figures, Streamlit just displays them.

It is the one `.py` file left in the folder, on purpose: `streamlit run` wants
a script, and this is an app rather than a lesson.
