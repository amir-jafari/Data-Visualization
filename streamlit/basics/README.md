# basics — one idea per file

Work through the chapters in order. Run them from the launcher (`streamlit run
streamlit/app.py` at the repo root) or one at a time:

```bash
streamlit run streamlit/basics/charts/matplotlib_chart.py
```

| Chapter | You learn | Needs S3 keys |
| --- | --- | --- |
| `01_text` | Titles, headers, markdown, LaTeX | — |
| `02_dataframes` | Displaying, styling and editing tables; metrics; JSON | — |
| `03_charts` | Built-in charts, Matplotlib, Altair, Vega-Lite, Plotly, maps | — |
| `04_inputs` | Every widget: buttons, sliders, selects, text, numbers, dates, uploads | one file |
| `05_media` | Images, audio, video | yes |
| `06_layout` | Sidebar, columns, tabs, expanders, containers, popovers, dialogs | — |
| `07_chat` | Chat messages, chat input, streaming replies | — |
| `08_status` | Progress bars, spinners, status boxes, alerts | — |
| `09_control_flow` | `st.stop()`, forms, `st.rerun()`, fragments | — |
| `10_state_and_config` | Page config, `st.echo`, `st.help`, **session state**, **caching**, backgrounds | one file |
| `11_extras` | HTML/CSS tooltips, drawable canvas | — |

## Naming a new lesson

One rule: **don't name a lesson file after a package you can import.** A lesson
called `altair.py` or `json.py` sits in a folder that ends up on Python's import
path, so `import altair` — including Streamlit's own, inside `st.line_chart()` —
finds the lesson instead of the library, and the app dies with a confusing
"partially initialized module" error. That is why the chart lessons are
`altair_chart.py` and `plotly_chart.py`, and the `st.json` one is
`display_json.py`.

## Two things worth knowing early

**Streamlit re-runs the whole script on every interaction.** A widget doesn't
fire a callback — it returns its current value, and the script runs again from
line 1. `10_state_and_config/04_session_state.py` shows how to keep a value
across those re-runs, and `06_caching.py` shows how to avoid redoing slow work
on every one of them. Those two are what every app in `apps/` is built on —
read them before you start your own project.

**`with st.echo():` prints the code inside it, then runs it.** Most lessons use
it so the page shows you its own source. That's a teaching device, not something
you need in your own apps.

## If a lesson asks for AWS keys

The media lessons read their files from S3 rather than from disk. Set up the
repo-root `.env` — see [`../s3/README.md`](../s3/README.md).
