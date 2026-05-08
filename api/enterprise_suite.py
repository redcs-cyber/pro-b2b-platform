from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from uuid import uuid4

from api.b2b_ecosystem import B2BEcosystemStore

ActorRole = Literal["super_admin", "dealer_admin", "buyer", "approver", "finance", "sales_rep", "warehouse", "support"]
WorkflowDecision = Literal["approved", "rejected", "needs_finance", "needs_manager"]
ShipmentStatus = Literal["draft", "created", "in_transit", "delivered", "exception"]
ReturnStatus = Literal["requested", "approved", "rejected", "received", "refunded"]
NotificationChannel = Literal["email", "sms", "push", "webhook"]


@dataclass
class RolePolicy:
    role: ActorRole
    permissions: set[str]
    max_order_total: float | None = None
    can_approve_own_order: bool = False


@dataclass
class ApprovalRequest:
    order_total: float
    customer_id: str
    actor_role: ActorRole
    payment_method: str
    credit_limit_exceeded: bool = False
    margin_below_threshold: bool = False


@dataclass
class PaymentInstallment:
    installment_no: int
    due_date: str
    amount: float
    status: Literal["open", "paid", "overdue"] = "open"


@dataclass
class ShipmentCreate:
    order_id: str
    carrier: Literal["yurtici", "aras", "mng", "hepsijet", "dhl", "fleet"]
    warehouse_id: str
    address_id: str
    package_count: int
    desi: float


@dataclass
class ReturnCreate:
    order_id: str
    sku: str
    quantity: int
    reason: Literal["damaged", "wrong_item", "warranty", "commercial_return"]
    notes: str = ""


@dataclass
class NotificationTemplate:
    template_id: str
    channels: list[NotificationChannel]
    subject: str
    body: str


@dataclass
class EnterpriseSuite:
    b2b_store: B2BEcosystemStore = field(default_factory=B2BEcosystemStore)
    role_policies: dict[ActorRole, RolePolicy] = field(default_factory=dict)
    shipments: dict[str, dict[str, Any]] = field(default_factory=dict)
    returns: dict[str, dict[str, Any]] = field(default_factory=dict)
    notifications: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.role_policies:
            return
        self.role_policies = {
            "super_admin": RolePolicy("super_admin", {"*"}, None, True),
            "dealer_admin": RolePolicy("dealer_admin", {"order.create", "order.approve", "finance.view", "user.manage"}, 250_000, False),
            "buyer": RolePolicy("buyer", {"catalog.view", "quote.create", "order.create"}, 50_000, False),
            "approver": RolePolicy("approver", {"catalog.view", "quote.create", "order.approve"}, 150_000, False),
            "finance": RolePolicy("finance", {"finance.view", "finance.approve", "order.hold.release"}, None, False),
            "sales_rep": RolePolicy("sales_rep", {"crm.view", "quote.create", "order.create", "customer.view"}, 100_000, False),
            "warehouse": RolePolicy("warehouse", {"wms.pick", "wms.pack", "shipment.create", "return.receive"}, None, False),
            "support": RolePolicy("support", {"ticket.view", "return.create", "customer.view"}, 25_000, False),
        }

    def mega_feature_catalog(self) -> dict[str, Any]:
        return {
            "domains": {
                "commerce": ["catalog", "quick_order", "cart", "quote", "order", "campaign"],
                "finance": ["open_account", "invoice_aging", "virtual_pos", "installments", "check_note"],
                "operations": ["wms", "handheld", "shipment", "return", "sla", "quality_control"],
                "growth": ["crm", "lead_scoring", "marketplace", "recommendation", "segmentation"],
                "platform": ["identity", "acl", "audit", "kvkk", "observability", "integration_hub"],
            },
            "automation_rules": [
                "Limit aşımı finans onayına düşer",
                "Düşük marj satış müdürü onayına düşer",
                "Sipariş onaylanınca stok rezervasyonu ve ERP job üretilir",
                "Kargo oluşunca bayi SMS/e-posta/push ile bilgilendirilir",
                "İade talebi kalite kontrol ve finans iade adımlarına ayrılır",
            ],
            "recommended_next_repos": [
                "prob2b-web-nextjs",
                "prob2b-mobile-handheld",
                "prob2b-integration-workers",
                "prob2b-data-platform",
                "prob2b-terraform-live",
            ],
        }

    def can(self, role: ActorRole, permission: str, order_total: float = 0) -> bool:
        policy = self.role_policies[role]
        permission_allowed = "*" in policy.permissions or permission in policy.permissions
        limit_allowed = policy.max_order_total is None or order_total <= policy.max_order_total
        return permission_allowed and limit_allowed

    def decide_workflow(self, request: ApprovalRequest) -> dict[str, Any]:
        if request.credit_limit_exceeded:
            decision: WorkflowDecision = "needs_finance"
            owner = "finance"
        elif request.margin_below_threshold or not self.can(request.actor_role, "order.approve", request.order_total):
            decision = "needs_manager"
            owner = "approver"
        else:
            decision = "approved"
            owner = "integration-service"
        return {
            "decision": decision,
            "owner": owner,
            "steps": self._workflow_steps(decision),
        }

    def create_payment_plan(self, grand_total: float, term_days: int, installments: int = 1) -> dict[str, Any]:
        if installments < 1:
            raise ValueError("Taksit sayısı en az 1 olmalıdır")
        base_amount = round(grand_total / installments, 2)
        plan = []
        remaining = round(grand_total, 2)
        for index in range(1, installments + 1):
            amount = base_amount if index < installments else round(remaining, 2)
            remaining = round(remaining - amount, 2)
            plan.append(
                asdict(
                    PaymentInstallment(
                        installment_no=index,
                        due_date=_day_offset(term_days * index),
                        amount=amount,
                    )
                )
            )
        return {"plan_id": f"PAY-{uuid4().hex[:8].upper()}", "installments": plan, "total": round(grand_total, 2)}

    def create_shipment(self, shipment: ShipmentCreate) -> dict[str, Any]:
        shipment_id = f"SHP-{uuid4().hex[:8].upper()}"
        record = asdict(shipment) | {
            "shipment_id": shipment_id,
            "status": "created",
            "tracking_number": f"TRK{uuid4().hex[:10].upper()}",
            "created_at": _now(),
        }
        self.shipments[shipment_id] = record
        self.queue_notification(
            "shipment.created",
            ["email", "sms", "push"],
            {"order_id": shipment.order_id, "tracking_number": record["tracking_number"]},
        )
        return record

    def create_return(self, request: ReturnCreate) -> dict[str, Any]:
        return_id = f"RMA-{uuid4().hex[:8].upper()}"
        status: ReturnStatus = "approved" if request.reason in {"wrong_item", "damaged"} else "requested"
        record = asdict(request) | {"return_id": return_id, "status": status, "created_at": _now()}
        self.returns[return_id] = record
        self.queue_notification("return.created", ["email", "webhook"], {"return_id": return_id, "status": status})
        return record

    def queue_notification(self, event: str, channels: list[NotificationChannel], payload: dict[str, Any]) -> dict[str, Any]:
        record = {
            "notification_id": f"NTF-{uuid4().hex[:8].upper()}",
            "event": event,
            "channels": channels,
            "payload": payload,
            "status": "queued",
            "created_at": _now(),
        }
        self.notifications.append(record)
        return record

    def build_search_index(self) -> list[dict[str, Any]]:
        index = []
        for product in self.b2b_store.products.values():
            tokens = " ".join([product.sku, product.name, product.brand, product.category, *product.attributes.values()]).casefold()
            index.append(
                {
                    "sku": product.sku,
                    "title": product.name,
                    "brand": product.brand,
                    "category": product.category,
                    "tokens": tokens,
                    "filterable_attributes": product.attributes,
                    "documents": product.documents,
                }
            )
        return index

    def analytics_snapshot(self) -> dict[str, Any]:
        reserved_units = sum(reservation.quantity for reservation in self.b2b_store.reservations.values())
        open_finance_count = sum(1 for order in self.b2b_store.orders.values() if order.get("approval_status") == "waiting_finance")
        return {
            "gmv": round(sum(order["totals"]["grand_total"] for order in self.b2b_store.orders.values()), 2),
            "orders": len(self.b2b_store.orders),
            "reserved_units": reserved_units,
            "open_finance_approvals": open_finance_count,
            "shipments": len(self.shipments),
            "returns": len(self.returns),
            "notifications_queued": len(self.notifications),
        }

    def _workflow_steps(self, decision: WorkflowDecision) -> list[dict[str, str]]:
        if decision == "approved":
            return [{"step": "ERP aktarımı", "owner": "integration-service"}]
        if decision == "needs_finance":
            return [
                {"step": "Cari limit ve vade kontrolü", "owner": "finance"},
                {"step": "ERP aktarımı", "owner": "integration-service"},
            ]
        if decision == "needs_manager":
            return [
                {"step": "Bayi/satış yönetici onayı", "owner": "approver"},
                {"step": "ERP aktarımı", "owner": "integration-service"},
            ]
        return [{"step": "Ret bildirimi", "owner": "support"}]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _day_offset(days: int) -> str:
    due_date = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0) + timedelta(days=days)
    return due_date.isoformat().replace("+00:00", "Z")
