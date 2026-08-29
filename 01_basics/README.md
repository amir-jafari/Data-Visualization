# 01_basics — one idea per file

Work through the chapters in order. Run them from the launcher (`streamlit run
app.py` at the repo root) or one at a time:

```bash
streamlit run 01_basics/03_charts/05_matplotlib.py
```

| Chapter | You learn | Needs S3 keys |
| --- | --- | --- |
| `01_text` | Titles, headers, markdown, LaTeX | — |
| `02_dataframes` | Displaying, styling and editing tables; metrics; JSON | — |
| `03_charts` | Built-in charts, Matplotlib, Altair, Vega-Lite, Plotly, maps | — |
| `04_inputs` | Every widget: buttons, sliders, selects, text, dates, uploads | one file |
| `05_media` | Images, audio, video | yes |
| `06_layout` | Sidebar, columns, tabs, expanders, containers | — |
| `07_chat` | Chat messages and chat input | — |
| `08_status` | Progress bars, spinners, status boxes, alerts | — |
| `09_control_flow` | `st.stop()` and forms — batching input | — |
| `10_state_and_config` | Page config, `st.echo`, `st.help`, **session state**, backgrounds | one file |
| `11_extras` | HTML/CSS tooltips, drawable canvas | — |

## Two things worth knowing early

**Streamlit re-runs the whole script on every interaction.** A widget doesn't
fire a callback — it returns its current value, and the script runs again from
line 1. `10_state_and_config/04_session_state.py` shows how to keep a value
across those re-runs.

**`with st.echo():` prints the code inside it, then runs it.** Most lessons use
it so the page shows you its own source. That's a teaching device, not something
you need in your own apps.

## If a lesson asks for AWS keys

The media lessons read their files from S3 rather than from disk. Set up the
repo-root `.env` — see [`../s3/README.md`](../s3/README.md).
