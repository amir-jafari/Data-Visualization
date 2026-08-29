"""
Start the Data API.

    python fastapi/project/serve.py

Why this file exists: `data_api` is a package, and its modules import each
other with relative imports (`from . import store`). Those only work when the
code is imported *as a package*, so `python data_api/main.py` cannot work --
Python would not know which package `.` refers to. This script puts the
project folder on the import path and hands uvicorn the import string
`data_api.main:app`, which is the form that supports --reload as well.

Equivalent, if you prefer typing it yourself:

    uvicorn data_api.main:app --reload --app-dir fastapi/project
"""

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent

if __name__ == "__main__":
    import uvicorn

    sys.path.insert(0, str(PROJECT))
    # reload=True needs the import string rather than the app object, because
    # the reloader starts a fresh process and has to re-import it.
    uvicorn.run("data_api.main:app", host="127.0.0.1", port=8000, reload=False)
