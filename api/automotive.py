from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

StockLocation = Literal["merkez_depo", "magaza", "servis", "saha_araci"]
TerminalTaskStatus = Literal["open", "in_progress", "done", "cancelled"]


@dataclass
class PartCreate:
    sku: str
    name: str
    brand: str
    unit_price: float
    oem_numbers: list[str] = field(default_factory=list)
    compatible_vehicles: list[str] = field(default_factory=list)
    category: str = "Genel"


@dataclass
class StockMutation:
    location: StockLocation
    quantity: int


@dataclass
class OrderLine:
    sku: str
    quantity: int


@dataclass
class OrderCreate:
    customer_name: str
    lines: list[OrderLine]
    channel: Literal["b2b_portal", "telefon", "pazaryeri", "el_terminali"] = "b2b_portal"


@dataclass
class TerminalTaskCreate:
    terminal_id: str
    task_type: Literal["sayim", "toplama", "mal_kabul", "raf_transferi", "teslimat"]
    sku: str | None = None
    quantity: int | None = None
    source_location: StockLocation | None = None
    target_location: StockLocation | None = None
    notes: str = ""


@dataclass
class AutomotiveStore:
    parts: dict[str, dict[str, Any]] = field(default_factory=dict)
    inventory: dict[str, dict[str, int]] = field(default_factory=dict)
    orders: dict[str, dict[str, Any]] = field(default_factory=dict)
    terminal_tasks: dict[str, dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.parts:
            self.add_part(
                PartCreate(
                    sku="FRN-BLK-001",
                    name="Ön fren balatası",
                    brand="ProParts",
                    oem_numbers=["OEM-34116761244", "OEM-34116859066"],
                    compatible_vehicles=["BMW 3 Serisi 2012-2018", "BMW 4 Serisi 2013-2020"],
                    category="Fren Sistemi",
                    unit_price=1290.0,
                )
            )
            self.add_part(
                PartCreate(
                    sku="FLT-YAG-010",
                    name="Yağ filtresi",
                    brand="FiltreMax",
                    oem_numbers=["OEM-06L115562"],
                    compatible_vehicles=["Volkswagen Golf 2013-2020", "Audi A3 2013-2020"],
                    category="Filtre",
                    unit_price=220.0,
                )
            )
            self.set_stock("FRN-BLK-001", StockMutation(location="merkez_depo", quantity=24))
            self.set_stock("FLT-YAG-010", StockMutation(location="merkez_depo", quantity=120))

    def add_part(self, part: PartCreate) -> dict[str, Any]:
        data = asdict(part)
        data["created_at"] = _now()
        self.parts[part.sku] = data
        self.inventory.setdefault(part.sku, {})
        return data

    def search_parts(self, query: str | None = None, vehicle: str | None = None) -> list[dict[str, Any]]:
        results = list(self.parts.values())
        if query:
            needle = query.casefold()
            results = [
                part
                for part in results
                if needle in part["sku"].casefold()
                or needle in part["name"].casefold()
                or needle in part["brand"].casefold()
                or any(needle in oem.casefold() for oem in part["oem_numbers"])
            ]
        if vehicle:
            vehicle_needle = vehicle.casefold()
            results = [
                part
                for part in results
                if any(vehicle_needle in item.casefold() for item in part["compatible_vehicles"])
            ]
        return results

    def set_stock(self, sku: str, mutation: StockMutation) -> dict[str, Any]:
        self._require_part(sku)
        self.inventory.setdefault(sku, {})[mutation.location] = mutation.quantity
        return self.stock_snapshot(sku)

    def stock_snapshot(self, sku: str | None = None) -> dict[str, Any]:
        if sku:
            self._require_part(sku)
            locations = self.inventory.get(sku, {})
            return {"sku": sku, "locations": locations, "total": sum(locations.values())}
        return {
            item_sku: {"locations": locations, "total": sum(locations.values())}
            for item_sku, locations in self.inventory.items()
        }

    def create_order(self, order: OrderCreate) -> dict[str, Any]:
        order_id = f"ORD-{uuid4().hex[:8].upper()}"
        lines = []
        total = 0.0
        for line in order.lines:
            part = self._require_part(line.sku)
            line_total = part["unit_price"] * line.quantity
            lines.append({"sku": line.sku, "name": part["name"], "quantity": line.quantity, "line_total": line_total})
            total += line_total
        record = {
            "id": order_id,
            "customer_name": order.customer_name,
            "channel": order.channel,
            "status": "hazirlaniyor",
            "lines": lines,
            "total": total,
            "created_at": _now(),
        }
        self.orders[order_id] = record
        for line in order.lines:
            self.create_terminal_task(
                TerminalTaskCreate(
                    terminal_id="HT-01",
                    task_type="toplama",
                    sku=line.sku,
                    quantity=line.quantity,
                    source_location="merkez_depo",
                    notes=f"{order_id} siparişi için ürün topla",
                )
            )
        return record

    def list_orders(self) -> list[dict[str, Any]]:
        return list(self.orders.values())

    def create_terminal_task(self, task: TerminalTaskCreate) -> dict[str, Any]:
        task_id = f"HTASK-{uuid4().hex[:8].upper()}"
        record = asdict(task) | {"id": task_id, "status": "open", "created_at": _now()}
        self.terminal_tasks[task_id] = record
        return record

    def list_terminal_tasks(self, terminal_id: str | None = None) -> list[dict[str, Any]]:
        tasks = list(self.terminal_tasks.values())
        if terminal_id:
            tasks = [task for task in tasks if task["terminal_id"] == terminal_id]
        return tasks

    def update_terminal_task_status(self, task_id: str, status: TerminalTaskStatus) -> dict[str, Any]:
        if task_id not in self.terminal_tasks:
            raise KeyError(f"Terminal görevi bulunamadı: {task_id}")
        self.terminal_tasks[task_id]["status"] = status
        self.terminal_tasks[task_id]["updated_at"] = _now()
        return self.terminal_tasks[task_id]

    def ecosystem_overview(self) -> dict[str, Any]:
        return {
            "modules": [
                "B2B parça kataloğu",
                "OEM/araç uyumluluk araması",
                "Çok lokasyonlu stok",
                "Sipariş ve toplama akışı",
                "El terminali görev kuyruğu",
                "Telemetri ve operasyon paneli",
            ],
            "counts": {
                "parts": len(self.parts),
                "orders": len(self.orders),
                "terminal_tasks": len(self.terminal_tasks),
            },
            "handheld_terminal": {
                "supported_workflows": ["sayım", "mal kabul", "sipariş toplama", "raf transferi", "teslimat"],
                "recommended_device_profile": "Android barkod okuyuculu el terminali veya kamera barkod taramalı PWA",
            },
        }

    def _require_part(self, sku: str) -> dict[str, Any]:
        if sku not in self.parts:
            raise KeyError(f"Parça bulunamadı: {sku}")
        return self.parts[sku]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
