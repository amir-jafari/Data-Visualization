# Data Visualization — Streamlit course

Everything lives in [`streamlit/`](streamlit/).

```bash
pip install -r streamlit/requirements.txt
streamlit run streamlit/app.py
```

Run the commands from this directory (the repo root). Full instructions are in
[`streamlit/README.md`](streamlit/README.md).

> **Do not add `streamlit/__init__.py`.** The folder shares its name with the
> Streamlit package. Without an `__init__.py` Python treats it as a namespace
> package, which always loses to the real installed library, so `import
> streamlit` keeps working. Adding that one file would turn it into a regular
> package that shadows the library, and every import would break.
