from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import subprocess, sys, socket

BASE   = Path(__file__).parent.parent
PYTHON = sys.executable

PROJECTS = {
    "aa-for-data-structures": {"dir": BASE / "AAforDataStructures",         "port": 8006},
    "search-bar-animation":   {"dir": BASE / "SearchBarAnimation",           "port": 8004},
    "sort-animation-v3":      {"dir": BASE / "AllSortAnimationByBar_JS_v3",  "port": 8003},
    "array-animation":        {"dir": BASE / "ArrayAnimation",               "port": 8005},
}

_procs: dict[str, subprocess.Popen] = {}

app = FastAPI()

# ── 死活確認 ──────────────────────────────────────────
@app.get("/api/check/{port}")
async def check_port(port: int):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.8):
            return {"online": True}
    except OSError:
        return {"online": False}

# ── 起動 ─────────────────────────────────────────────
@app.post("/api/start/{name}")
async def start_project(name: str):
    if name not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")
    proj = PROJECTS[name]
    if name in _procs and _procs[name].poll() is None:
        return {"status": "already_running", "port": proj["port"]}
    proc = subprocess.Popen(
        [PYTHON, "-m", "uvicorn", "main:app", "--port", str(proj["port"])],
        cwd=str(proj["dir"]),
    )
    _procs[name] = proc
    return {"status": "started", "port": proj["port"]}

# ── 静的ファイル ──────────────────────────────────────
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
