from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from api.telemetry_service import TelemetryStore
from api.b2b_ecosystem import B2BEcosystemStore, B2BOrderCreate
from api.compliance import ComplianceProgram
from api.enterprise_suite import ApprovalRequest, EnterpriseSuite, ReturnCreate, ShipmentCreate
from api.quick_order import parse_quick_order_csv
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
b2b_store = B2BEcosystemStore()
enterprise_suite = EnterpriseSuite(b2b_store)
compliance_program = ComplianceProgram()
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


@app.get("/b2b/platform/blueprint")
def b2b_platform_blueprint() -> dict:
    return b2b_store.platform_blueprint()


@app.get("/b2b/customers/tree")
def b2b_customer_tree(root_customer_id: str | None = None) -> list[dict]:
    return b2b_store.customer_tree(root_customer_id)


@app.post("/b2b/quote")
def b2b_quote(order: B2BOrderCreate) -> dict:
    try:
        return b2b_store.calculate_quote(order)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/b2b/orders")
def b2b_create_order(order: B2BOrderCreate) -> dict:
    try:
        return b2b_store.create_order(order, actor_id=order.customer_id, ip_address="api")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.get("/b2b/orders")
def b2b_orders() -> list[dict]:
    return list(b2b_store.orders.values())


@app.get("/b2b/integrations/packets")
def b2b_integration_packets() -> dict:
    return b2b_store.export_integration_packets()


@app.get("/b2b/audit")
def b2b_audit() -> list[dict]:
    return [event.__dict__ for event in b2b_store.audit_trail]


@app.get("/b2b/enterprise/features")
def b2b_enterprise_features() -> dict:
    return enterprise_suite.mega_feature_catalog()


@app.post("/b2b/enterprise/workflow/decide")
def b2b_workflow_decide(request: ApprovalRequest) -> dict:
    return enterprise_suite.decide_workflow(request)


@app.post("/b2b/quick-order/parse")
def b2b_quick_order_parse(payload: dict) -> dict:
    parsed = parse_quick_order_csv(payload.get("csv", ""))
    return {"lines": [line.__dict__ for line in parsed.lines], "errors": parsed.errors}


@app.post("/b2b/shipments")
def b2b_create_shipment(shipment: ShipmentCreate) -> dict:
    return enterprise_suite.create_shipment(shipment)


@app.post("/b2b/returns")
def b2b_create_return(request: ReturnCreate) -> dict:
    return enterprise_suite.create_return(request)


@app.get("/b2b/search/index")
def b2b_search_index() -> list[dict]:
    return enterprise_suite.build_search_index()


@app.get("/b2b/analytics/snapshot")
def b2b_analytics_snapshot() -> dict:
    return enterprise_suite.analytics_snapshot()


@app.get("/b2b/compliance/readiness")
def b2b_compliance_readiness() -> dict:
    return compliance_program.readiness_overview()


@app.get("/b2b/compliance/certifications")
def b2b_compliance_certifications() -> list[dict]:
    return compliance_program.certification_matrix()


@app.get("/b2b/compliance/curriculum")
def b2b_compliance_curriculum() -> list[dict]:
    return compliance_program.curriculum_map()


@app.get("/b2b/compliance/missing-actions")
def b2b_compliance_missing_actions() -> list[dict]:
    return compliance_program.missing_go_live_actions()


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
