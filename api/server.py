from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from api.telemetry_service import TelemetryStore
from api.automotive import (
    AutomotiveStore,
    OrderCreate,
    PartCreate,
    StockMutation,
    TerminalTaskCreate,
    TerminalTaskStatus,
)

app = FastAPI(title="ProB2B Platform")
store = TelemetryStore()
automotive_store = AutomotiveStore()
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


@app.get("/automotive/overview")
def automotive_overview() -> dict:
    return automotive_store.ecosystem_overview()


@app.get("/automotive/parts")
def automotive_parts(q: str | None = None, vehicle: str | None = None) -> list[dict]:
    return automotive_store.search_parts(q, vehicle)


@app.post("/automotive/parts")
def automotive_add_part(part: PartCreate) -> dict:
    return automotive_store.add_part(part)


@app.get("/automotive/inventory")
def automotive_inventory() -> dict:
    return automotive_store.stock_snapshot()


@app.put("/automotive/inventory/{sku}")
def automotive_set_stock(sku: str, mutation: StockMutation) -> dict:
    try:
        return automotive_store.set_stock(sku, mutation)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/automotive/orders")
def automotive_create_order(order: OrderCreate) -> dict:
    try:
        return automotive_store.create_order(order)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/automotive/orders")
def automotive_orders() -> list[dict]:
    return automotive_store.list_orders()


@app.post("/automotive/terminal/tasks")
def automotive_create_terminal_task(task: TerminalTaskCreate) -> dict:
    try:
        return automotive_store.create_terminal_task(task)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/automotive/terminal/tasks")
def automotive_terminal_tasks(terminal_id: str | None = None) -> list[dict]:
    return automotive_store.list_terminal_tasks(terminal_id)


@app.patch("/automotive/terminal/tasks/{task_id}/{status}")
def automotive_update_terminal_task(task_id: str, status: TerminalTaskStatus) -> dict:
    try:
        return automotive_store.update_terminal_task_status(task_id, status)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


if __name__ == "__main__":
    uvicorn.run("api.server:app", host="127.0.0.1", port=8000, reload=False)
