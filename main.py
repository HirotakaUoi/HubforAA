from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import subprocess, socket

BASE = Path(__file__).parent.parent
# 各プロジェクトは共通スクリプトで起動する（.venv の確認・修復もここで行う）。
# Hub 自身の python（sys.executable）は使わない: Hub の .venv も Dropbox 同期で
# 稼働中に差し替わることがあり、以前はそれで全プロジェクトが起動不能になった
RUN_SERVER = BASE / "run_server.sh"

PROJECTS = {
    "aa-for-data-structures": {"dir": BASE / "AAforDataStructures",         "port": 8006},
    "search-bar-animation":   {"dir": BASE / "SearchBarAnimation",           "port": 8004},
    "sort-animation-v3":      {"dir": BASE / "AllSortAnimationByBar_JS_v3",  "port": 8003},
    "array-animation":        {"dir": BASE / "ArrayAnimation",               "port": 8005},
}

_procs: dict[str, subprocess.Popen] = {}

app = FastAPI()

def _is_online(port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.8):
            return True
    except OSError:
        return False

# ── 死活確認 ──────────────────────────────────────────
@app.get("/api/check/{port}")
async def check_port(port: int):
    return {"online": _is_online(port)}

# ── 起動 ─────────────────────────────────────────────
@app.post("/api/start/{name}")
async def start_project(name: str):
    if name not in PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")
    proj = PROJECTS[name]
    if (name in _procs and _procs[name].poll() is None) or _is_online(proj["port"]):
        return {"status": "already_running", "port": proj["port"]}
    print(f"hub: starting {name}", flush=True)
    try:
        proc = subprocess.Popen(["/bin/bash", str(RUN_SERVER), str(proj["dir"]), str(proj["port"])])
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"起動に失敗しました: {e}")
    _procs[name] = proc
    return {"status": "started", "port": proj["port"]}

# ── 静的ファイル ──────────────────────────────────────
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
