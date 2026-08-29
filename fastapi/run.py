"""
Lesson runner for the FastAPI course.

    python fastapi/run.py                      list every lesson
    python fastapi/run.py endpoints/hello      run one lesson
    python fastapi/run.py hello                ...the chapter is optional
    python fastapi/run.py project              run the capstone Data API

Each lesson is an ordinary file you can also run directly:

    python fastapi/basics/endpoints/hello.py

The runner exists for two conveniences: it lists the chapters in the order
they are meant to be read, and it starts uvicorn with --reload so the server
picks up your edits while you experiment.
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASICS = HERE / "basics"
PORT = 8000

# Chapter order is the teaching order; folder names are not numbered, so it
# lives here. Lessons within a chapter are ordered here too.
CHAPTERS = {
    "endpoints": ["hello", "path_params", "query_params", "headers"],
    "models": ["request_body", "response_model", "validation", "nested_models"],
    "errors": ["status_codes", "http_errors", "custom_errors"],
    "structure": ["routers", "dependencies", "settings"],
    "async_work": ["sync_vs_async", "background_tasks", "concurrency"],
    "security": ["api_key", "oauth2"],
    "files": ["upload", "download", "static_and_cors"],
    "testing": ["test_client", "overriding_dependencies"],
}

BLURB = {
    "endpoints": "routes, and where their values come from",
    "models": "describing data once, with Pydantic",
    "errors": "status codes and failing clearly",
    "structure": "routers, dependencies, settings -- how projects are laid out",
    "async_work": "def vs async def, background work, doing things at once",
    "security": "API keys and OAuth2 logins",
    "files": "uploads, downloads, static files and CORS",
    "testing": "testing an API without running a server",
}


def lessons():
    """[(chapter, lesson, path)] in teaching order, plus anything unlisted."""
    found = []
    for chapter, names in CHAPTERS.items():
        folder = BASICS / chapter
        if not folder.is_dir():
            continue
        on_disk = {p.stem: p for p in folder.glob("*.py")}
        ordered = [n for n in names if n in on_disk]
        ordered += sorted(n for n in on_disk if n not in names)
        found += [(chapter, name, on_disk[name]) for name in ordered]
    return found


def show_list():
    print(__doc__.strip().split("\n\n")[0])
    print()
    current = None
    for chapter, name, _ in lessons():
        if chapter != current:
            current = chapter
            print(f"\n  {chapter}  --  {BLURB.get(chapter, '')}")
        print(f"      {chapter}/{name}")
    print("\n  project  --  the Data API: everything above, put together")
    print(f"\nRun one:  python fastapi/run.py {lessons()[0][0]}/{lessons()[0][1]}")


def find(target: str):
    """Accept 'chapter/lesson' or just 'lesson'."""
    target = target.removesuffix(".py")
    matches = [
        (chapter, name, path) for chapter, name, path in lessons()
        if target in (name, f"{chapter}/{name}")
    ]
    if not matches:
        print(f"No lesson called {target!r}.\n")
        show_list()
        sys.exit(1)
    if len(matches) > 1:
        print(f"{target!r} is ambiguous: " +
              ", ".join(f"{c}/{n}" for c, n, _ in matches))
        sys.exit(1)
    return matches[0]


def serve(app_dir: Path, module: str):
    """Hand uvicorn an import string, which is what --reload requires."""
    print(f"\n  {module}:app  ->  http://127.0.0.1:{PORT}")
    print(f"  docs         ->  http://127.0.0.1:{PORT}/docs")
    print("  stop with Ctrl-C\n")
    command = [sys.executable, "-m", "uvicorn", f"{module}:app",
               "--reload", "--app-dir", str(app_dir), "--port", str(PORT)]
    try:
        subprocess.run(command, check=False)
    except KeyboardInterrupt:
        pass


def main():
    if len(sys.argv) < 2:
        show_list()
        return

    target = sys.argv[1]

    if target in ("project", "api", "data_api"):
        serve(HERE / "project", "data_api.main")
        return

    chapter, name, path = find(target)
    serve(path.parent, name)


if __name__ == "__main__":
    main()
