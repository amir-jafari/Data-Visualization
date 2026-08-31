# The ideas behind the charts

A plain-words companion to `viz/`. Every idea points at a lesson you can run,
and most of them at a number the lesson measures — so you can show rather than
assert.

**How to use it.** Each section has the same four parts:

- **The idea** — one sentence to say out loud
- **A picture** — the analogy that makes it stick
- **Show them** — the lesson, and what to point at
- **Watch them trip** — the mistake students actually make

Numbers quoted below are printed by the lessons themselves. Run them and the
same figures come out, because the sample data is seeded.

---

## 0. Why this folder exists

**The idea.** A chart is an argument. Choosing one is choosing what to claim.

**A picture.** A sentence. Nobody thinks "which words shall I use?" is a
decorative question — the words *are* the meaning. A chart is the same, except
students have been taught that it is a formatting step at the end.

Say this: *"You do not `plt.plot()` your data and then decide what it means.
You decide what you are claiming, then draw the chart that makes that claim
honestly."*

**How this connects to the rest of the repo.** `streamlit/` puts a chart in
front of a person, `fastapi/` serves the data behind it, and this folder is
what makes the chart in the middle worth looking at.

---

## 1. Match the mark to the question

**The idea.** Different shapes are read by different parts of your visual
system, and they are not equally good.

**A picture.** Rank these by how accurately a person can judge them:

1. **Position** on a common scale — very accurate (scatter, dot plot)
2. **Length** — accurate (bars)
3. **Angle / area** — poor (pie charts, bubbles)
4. **Colour intensity** — worst (heatmaps for exact values)

That ranking explains most of the rules in this folder. It is why bars beat
pies, why dots beat bars for small differences, and why a heatmap is for
patterns rather than for reading numbers off.

**Show them.** `choosing/comparison.ipynb` — the same six numbers as an
alphabetical vertical bar chart and as a sorted horizontal one. Then
`choosing/composition.ipynb` — the pie chart, and the same data as bars. Ask the
class to rank SQL against Excel from the pie. They cannot. Then show the bars.

**Watch them trip.** Reaching for a chart type because it is available in the
library, rather than because it fits the question. Ask: *"what is the question,
in words, before you pick?"*

---

## 2. Bars need zero. Lines do not.

**The idea.** A bar's **length** is the number, so cutting the axis cuts the
number. A line's **slope** is the message, and slope survives a shifted
baseline.

**Show them.** `misleading/truncated_axis.ipynb` prints the measurement:

| axis starts at | tallest bar *looks* | true ratio |
| --- | --- | --- |
| 0 | 1.05× the shortest | 1.05 |
| 48 | **3.8×** the shortest | 1.05 |

A **4-fold exaggeration**, from one line of code, with every number true.

Then the second figure: the same rule applied to a line chart forced to zero,
where the trend vanishes into a flat line at the top of the frame.

**Say this:** *"Bars, zero, always. Lines, whatever range shows the slope.
That is not a style preference — it is about which thing your eye is
measuring."*

**Watch them trip.** They learn "always start at zero" as a blanket rule and
then flatten every time series they draw. The rule has a reason; teach the
reason.

---

## 3. A summary throws information away

**The idea.** Every mean, box and trend line is a compression. Know what you
compressed.

**Show them.** Two figures, and they are the best pair in the folder.

`choosing/distribution.ipynb` — three datasets built so their **quartiles agree
to within about 2 points**. Their box plots are indistinguishable. Their histograms are
one hump, two humps, and flat. Show the boxes first, ask "are these the same
data?", let them answer, then reveal the histograms.

`choosing/relationship.ipynb` — Anscombe's quartet. Four datasets with identical
means, variances, correlation and regression line **to two decimal places**
(the lesson prints the table). One is linear, one is curved, one has an
outlier dragging the line, one is a single leverage point.

**Say this:** *"Plot it before you summarise it. The summary cannot warn you
about what it left out."*

---

## 4. Colour has three jobs, and you must pick one

**The idea.**

| Family | For | Example |
| --- | --- | --- |
| **Categorical** | unordered groups | regions, species |
| **Sequential** | a quantity, low to high | population, temperature |
| **Diverging** | distance from a real centre | change vs last year, error |

Using the wrong family makes a false claim before anyone reads a number: a
sequential palette on categories invents a ranking; a diverging palette
without a real middle invents a neutral point.

**Show them.** `color/palettes.ipynb` — five fruits coloured with viridis, which
silently implies apple < banana < cherry. Then the same bars in tab10.

**Watch them trip.** Diverging colour maps applied to all-positive data, where
the white midpoint lands wherever the data happens to average out. The fix is
one line: pin `vmin` and `vmax` symmetrically.

---

## 5. Rainbow colour maps lie, and here is the number

**The idea.** For a colour map to be honest, equal steps in the data must look
like equal steps in colour. Rainbow maps fail this badly.

**Show them.** `color/rainbow.ipynb` measures it:

> **jet's lightness decreases at 92 of 255 steps.** viridis: **0.**

Every one of those 92 is a place where a *bigger* number looks *darker* than a
smaller one. Then the visual proof: a perfectly linear ramp rendered in jet
grows visible bands that are not in the data.

**Say this:** *"Ninety-two times, jet tells you the value went down when it
went up. That is not aesthetics, that is a broken instrument."*

Finish with the greyscale test — print it in black and white; if it still
works, it works for everyone.

---

## 6. One in twelve men sees colour differently

**The idea.** If your chart's meaning lives in red-versus-green, roughly 8% of
men get nothing from it.

**Show them.** `color/colorblind.ipynb` simulates three kinds of colour vision
deficiency and then *measures* which colour pairs collide:

- **tab10** (matplotlib's default): 2–3 colliding pairs under each type
- **Okabe-Ito** (designed for this): **0 collisions for deuteranopia**, the
  common kind — but still 3 for tritanopia

**Do not oversell it.** No palette is safe for everyone, which is exactly why
the third figure matters: add a **second channel**. Line style, marker shape,
or a direct label. Then colour is a bonus rather than the whole message.

**Watch them trip.** Red = bad, green = good, with nothing else to tell them
apart. It is the single most common accessibility failure in student work.

---

## 7. Grey everything, colour the point

**The idea.** Colour is the loudest signal you have. Spending it on all ten
series spends it on none.

**Show them.** `annotation/highlight.ipynb` is the demo that changes how students
draw. **One dataset, three panels, identical axes** — the only difference is
which line is coloured and which are grey. The three titles are:

- *"West is growing fastest"*
- *"East has stalled"*
- *"West is catching North"*

Same data. Three different arguments. Nothing was filtered.

**Then** `annotation/direct_labels.ipynb`: put the series name at the end of the
line and delete the legend. A legend is a lookup table; a label is an answer.

**Say this:** *"A legend makes the reader do homework. Put the name where the
line is."*

---

## 8. The title says the finding

**The idea.** *"Sales by region, 2024–2025"* tells the reader what they are
looking at, which they can already see. *"West overtook East in July"* tells
them what to conclude — which is why you drew it.

**Show them.** `annotation/titles.ipynb` — the same chart with each title, side by
side, then the finished version: declarative title, subtitle carrying the
detail, source note, no top/right frame, faint gridlines.

The pattern to write on the board:

```
Title      = the finding      "West overtook East in July 2024"
Subtitle   = the detail       "Monthly sales by region"
Source     = credibility      "Source: internal sales data"
```

**Watch them trip.** Titling the chart with its own axis labels — *"Score vs
Hours"* — which adds nothing at all.

---

## 9. How charts lie

**The idea.** Every chart in `misleading/` is built from true numbers. That is
the point: you cannot defend yourself by checking the data.

**Show them,** in this order, and each one prints its own measurement:

**Truncated axis** (`truncated_axis.ipynb`) — 4× exaggeration, shown above.

**Dual axes** (`dual_axis.ipynb`) — one pair of series, three panels, three
opposite conclusions, produced by changing nothing but the two y ranges. The
crossing point is a property of your scale choices, not of the data. The
honest alternatives: separate panels, index both to 100, or plot the ratio.

**Bubble area** (`area_vs_radius.ipynb`) — to show B is 8× A, people scale the
radius by 8, which multiplies the **area by 64**. The eye reads ink. Scale by
√8 = 2.83 instead. In matplotlib, `scatter(s=...)` is already an area, so pass
the value, never the square.

**Cherry-picking** (`cherry_picking.ipynb`) — the hardest to spot. A window
chosen to reverse a trend; bin boundaries chosen to make a bump appear or
vanish; a "50% risk reduction" with no baseline.

**The three questions to ask any chart, including your own:**

1. Why does the axis start *there*?
2. Who chose the bins, and what happens if I change them?
3. A percentage of *what* — where is the baseline and the sample size?

---

## 10. The capstone, and the mistake in it

`project/makeover.ipynb` takes one question through six steps: default →
labelled → readable → coloured → focused → finished. Step 1 already contains
the finding; nothing is added to the data.

**The part worth the whole session.** The first title on step 6 was:

> *"Morning students score 9 points higher at every level of study."*

It sounds careful. The chart disproves it three ways, and the notebook prints
all three:

- **The lines are not parallel.** The gap runs from ~4 points at low study
  hours to ~13 at high. There is no single number to quote.
- **The groups differ in more than one way.** Morning students also studied
  more on average (6.8 h vs 5.8 h), so group and hours are tangled together.
  This chart cannot separate them.
- **Scores are capped at 100** and are piling up on that ceiling, so the
  straight-line fits predict **127** — impossible.

The finished chart draws the ceiling line so you can watch the fit leave
reality.

**Say this:** *"A beautiful chart with an overclaiming title is worse than an
ugly one, because people believe it. The job is not done until the words match
what the picture actually supports."*

That is the sentence to end the course on.

---

## The ten things students get wrong

1. Truncating a bar chart's y axis
2. Forcing a line chart to start at zero, flattening the trend
3. Rainbow / jet colour maps for continuous data
4. Meaning carried by red-vs-green alone
5. A sequential palette on unordered categories
6. Ten colours where two would do
7. Titling the chart with its axis labels
8. A legend where a direct label would do
9. Scaling bubbles by radius instead of area
10. A title that claims more than the chart shows

---

## A three-session plan

**Session 1 — "a chart is an argument"**
`choosing/` and `foundations/`. End with the box-plot reveal and Anscombe.
*Homework: take one chart from your project and justify the chart type in
one sentence.*

**Session 2 — "making it readable"**
`color/`, `annotation/`, `layout/`. End with the three-stories highlight demo.
*Homework: re-draw your chart with a declarative title and direct labels.*

**Session 3 — "making it honest"**
`misleading/`, then the capstone makeover including the title that was wrong.
*Homework: find a misleading chart in the wild and say which trick it used.*

---

## Glossary, in words a beginner can use

| Word | What it actually means |
| --- | --- |
| **Figure** | The whole sheet of paper. One per picture. |
| **Axes** | *One plot* on that sheet. Confusing name — plural word, single object. |
| **Axis** | The x or y line itself, with its ticks and label. |
| **Encoding** | Which column maps to which visual property (x, colour, size). |
| **Categorical palette** | Distinct hues for unordered groups. |
| **Sequential palette** | One hue, light to dark, for a quantity. |
| **Diverging palette** | Two hues meeting at a meaningful middle. |
| **Small multiples** | Many small charts, same scales, compared at a glance. |
| **Chart junk** | Ink that carries no information. |
| **Data-ink ratio** | How much of the ink is actually data. Higher is better. |
| **Overplotting** | So many points they merge into a blob. |
| **Direct labelling** | Putting the name on the line instead of in a legend. |

---

## One-sentence summaries, if you are short on time

- **Choosing** — pick the chart from the question, not from the library menu
- **Foundations** — `fig, ax = plt.subplots()`, and know which is which
- **Colour** — three families; pick by the data, and never rely on hue alone
- **Annotation** — grey the context, label the line, let the title say the finding
- **Layout** — same scales or no comparison; delete ink that says nothing
- **Misleading** — every one of these charts is made of true numbers
- **Interactive** — explore interactively, present statically
- **The project** — the chart is not finished until the words match the picture
