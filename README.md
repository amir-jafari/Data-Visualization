# Data Visualization

Two courses, side by side.

| Folder | What it teaches | Start with |
| --- | --- | --- |
| [`streamlit/`](streamlit/) | Building the page a person looks at | `streamlit run streamlit/app.py` |
| [`fastapi/`](fastapi/) | Building the service behind it | `python fastapi/run.py` |

```bash
# the Streamlit course
pip install -r streamlit/requirements.txt
streamlit run streamlit/app.py

# the FastAPI course
pip install -r fastapi/requirements.txt
python fastapi/run.py
```

Run the commands from this directory (the repo root). Full instructions are in
[`streamlit/README.md`](streamlit/README.md) and
[`fastapi/README.md`](fastapi/README.md).

They meet in `fastapi/project/`: a FastAPI service and a Streamlit page that
consumes it, which is the shape most real data apps end up in.

> **Do not add `streamlit/__init__.py` or `fastapi/__init__.py`.** Both folders
> share a name with the library they teach. Without an `__init__.py` Python
> treats them as namespace packages, which always lose to the real installed
> library, so `import streamlit` and `import fastapi` keep working. Adding that
> one file would turn either into a regular package that shadows its library,
> and every import would break.
