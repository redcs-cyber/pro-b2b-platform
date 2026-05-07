from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from telemetry_service import TelemetryStore

app = FastAPI(title="ProB2B Platform")
store = TelemetryStore()
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse((STATIC_DIR / "dashboard.html").read_text(encoding="utf-8"))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/telemetry/{kind}")
def telemetry(kind: str, payload: dict | None = None) -> dict:
    return store.record(kind, payload).payload | {"kind": kind, "status": "recorded"}


@app.get("/telemetry")
def events() -> list[dict]:
    return store.list_events()


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False)
