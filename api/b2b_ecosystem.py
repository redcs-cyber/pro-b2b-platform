from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Literal
from uuid import uuid4

CustomerTier = Literal["platinum", "gold", "silver", "standard"]
PaymentMethod = Literal["open_account", "credit_card", "bank_transfer", "check_note", "virtual_pos"]
ApprovalStatus = Literal["auto_approved", "waiting_manager", "waiting_finance", "rejected"]
OrderChannel = Literal["b2b_portal", "api", "edi", "sales_rep", "mobile", "handheld"]


@dataclass
class CustomerAccount:
    customer_id: str
    name: str
    tier: CustomerTier
    tax_office: str
    tax_number: str
    gl_code: str
    payment_term_days: int
    credit_limit: float
    balance: float
    parent_customer_id: str | None = None
    sales_rep_id: str | None = None
    allowed_roles: list[str] = field(default_factory=lambda: ["buyer", "approver"])
    kvkk_consent: bool = True


@dataclass
class B2BProduct:
    sku: str
    name: str
    brand: str
    category: str
    list_price: float
    currency: str = "TRY"
    vat_rate: float = 0.20
    attributes: dict[str, str] = field(default_factory=dict)
    documents: list[str] = field(default_factory=list)


@dataclass
class PriceRule:
    rule_id: str
    priority: int
    rule_type: Literal["customer_net", "tier_discount", "volume_discount", "campaign"]
    sku: str | None = None
    customer_id: str | None = None
    tier: CustomerTier | None = None
    min_quantity: int = 1
    discount_rate: float = 0.0
    net_price: float | None = None
    currency: str = "TRY"
    starts_at: str = "2026-01-01T00:00:00Z"
    ends_at: str = "2026-12-31T23:59:59Z"


@dataclass
class B2BOrderLine:
    sku: str
    quantity: int


@dataclass
class B2BOrderCreate:
    customer_id: str
    branch_id: str
    lines: list[B2BOrderLine]
    payment_method: PaymentMethod = "open_account"
    shipping_address_id: str = "ADDR-01"
    channel: OrderChannel = "b2b_portal"
    notes: str = ""


@dataclass
class StockReservation:
    reservation_id: str
    order_id: str
    sku: str
    quantity: int
    warehouse_id: str
    expires_at: str


@dataclass
class AuditEvent:
    actor_id: str
    action: str
    entity: str
    entity_id: str
    ip_address: str
    timestamp: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class B2BEcosystemStore:
    customers: dict[str, CustomerAccount] = field(default_factory=dict)
    products: dict[str, B2BProduct] = field(default_factory=dict)
    inventory: dict[str, dict[str, int]] = field(default_factory=dict)
    price_rules: list[PriceRule] = field(default_factory=list)
    orders: dict[str, dict[str, Any]] = field(default_factory=dict)
    reservations: dict[str, StockReservation] = field(default_factory=dict)
    audit_trail: list[AuditEvent] = field(default_factory=list)
    crm_leads: dict[str, dict[str, Any]] = field(default_factory=dict)
    integration_jobs: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.customers:
            return
        self.customers["CARI-99"] = CustomerAccount(
            customer_id="CARI-99",
            name="Ankara Oto Servis A.Ş.",
            tier="gold",
            tax_office="Çankaya",
            tax_number="1234567890",
            gl_code="120.01.00099",
            payment_term_days=45,
            credit_limit=500_000.0,
            balance=120_000.0,
            sales_rep_id="SR-ANK-01",
        )
        self.customers["CARI-99-ALT-01"] = CustomerAccount(
            customer_id="CARI-99-ALT-01",
            name="Ankara Oto Servis Şaşmaz Şube",
            tier="gold",
            tax_office="Çankaya",
            tax_number="1234567890",
            gl_code="120.01.00099.01",
            payment_term_days=30,
            credit_limit=150_000.0,
            balance=22_000.0,
            parent_customer_id="CARI-99",
            sales_rep_id="SR-ANK-01",
        )
        self.products["PROD-X"] = B2BProduct(
            sku="PROD-X",
            name="Ağır hizmet fren diski",
            brand="ProParts",
            category="Fren Sistemi",
            list_price=50.0,
            attributes={"çap": "312mm", "malzeme": "yüksek karbon", "araç": "hafif ticari"},
            documents=["assets/pim/PROD-X/katalog.pdf", "assets/pim/PROD-X/montaj-kilavuzu.pdf"],
        )
        self.products["FLT-YAG-010"] = B2BProduct(
            sku="FLT-YAG-010",
            name="Premium yağ filtresi",
            brand="FiltreMax",
            category="Filtre",
            list_price=220.0,
            attributes={"diş": "M20x1.5", "yükseklik": "86mm"},
            documents=["assets/pim/FLT-YAG-010/teknik-fis.pdf"],
        )
        self.inventory = {
            "PROD-X": {"MERKEZ": 20_000, "ANKARA-SUBE": 4_000, "IZMIR-SUBE": 1_200},
            "FLT-YAG-010": {"MERKEZ": 8_500, "ANKARA-SUBE": 900},
        }
        self.price_rules = [
            PriceRule("PR-CARI99-PRODX", 100, "customer_net", sku="PROD-X", customer_id="CARI-99", net_price=45.0),
            PriceRule("PR-GOLD", 80, "tier_discount", tier="gold", discount_rate=0.08),
            PriceRule("PR-VOLUME-100", 70, "volume_discount", min_quantity=100, discount_rate=0.10),
            PriceRule("PR-CAMPAIGN-FILTER", 60, "campaign", sku="FLT-YAG-010", discount_rate=0.05),
        ]
        self.crm_leads["LEAD-001"] = {
            "company": "Marmara Filo Bakım",
            "stage": "teklif",
            "estimated_value": 1_250_000,
            "next_action": "numune ve vade teklifi",
        }

    def platform_blueprint(self) -> dict[str, Any]:
        return {
            "vision": "Tailor-made, SaaS + on-prem çalışabilen uçtan uca B2B işletim sistemi",
            "layers": [
                "Identity, ACL, 2FA, KVKK ve audit trail",
                "ERP/EDI/API entegrasyon köprüsü",
                "PIM, teknik katalog ve medya/CDN yönetimi",
                "Dinamik fiyatlandırma, iskonto ve kampanya motoru",
                "Bayi portalı, quick order, Excel/CSV toplu sipariş",
                "CRM lead/teklif/onay ve satış temsilcisi analitiği",
                "Finans: cari ekstre, vade, açık fatura, sanal POS, çek/senet",
                "WMS/el terminali, stok rezervasyon ve lojistik entegrasyonu",
                "BI dashboard, raporlama, anomaly/fraud monitoring",
                "SaaS Kubernetes + on-prem Docker/Nginx dağıtım seçenekleri",
            ],
            "data_files": {
                "order_schema": "schemas/order_schema.json",
                "migration": "migrations/001_b2b_core.sql",
                "erp_mapping": "integrations/erp/erp_field_mapping.json",
                "product_sync": "integrations/erp/product_sync.xml",
                "stock_update": "integrations/erp/stock_update.json",
                "price_list": "integrations/erp/price_list.json",
                "order_export": "integrations/erp/order_export.csv",
                "edi_purchase_order": "integrations/edi/x12_850_purchase_order.txt",
                "docker_compose": "deploy/onprem/docker-compose.yml",
                "nginx": "deploy/onprem/nginx.conf",
                "kubernetes": "deploy/saas/k8s/prob2b-api-deployment.yaml",
                "environment": ".env.example",
                "dockerfile": "deploy/Dockerfile",
                "backup_script": "deploy/onprem/scripts/backup_postgres.sh",
            },
            "counts": {
                "customers": len(self.customers),
                "products": len(self.products),
                "price_rules": len(self.price_rules),
                "orders": len(self.orders),
                "reservations": len(self.reservations),
                "audit_events": len(self.audit_trail),
            },
        }

    def customer_tree(self, root_customer_id: str | None = None) -> list[dict[str, Any]]:
        customers = list(self.customers.values())
        if root_customer_id:
            customers = [c for c in customers if c.customer_id == root_customer_id or c.parent_customer_id == root_customer_id]
        return [asdict(customer) for customer in customers]

    def calculate_quote(self, request: B2BOrderCreate) -> dict[str, Any]:
        customer = self._require_customer(request.customer_id)
        quote_lines = []
        subtotal = Decimal("0")
        vat_total = Decimal("0")
        discount_total = Decimal("0")
        for line in request.lines:
            product = self._require_product(line.sku)
            unit_list_price = money(product.list_price)
            best_price, applied_rules = self._best_unit_price(customer, product, line.quantity)
            line_subtotal = unit_list_price * line.quantity
            line_net = best_price * line.quantity
            line_vat = line_net * money(product.vat_rate)
            subtotal += line_net
            vat_total += line_vat
            discount_total += line_subtotal - line_net
            quote_lines.append(
                {
                    "sku": product.sku,
                    "name": product.name,
                    "quantity": line.quantity,
                    "list_unit_price": float(unit_list_price),
                    "net_unit_price": float(best_price),
                    "discount_amount": float(line_subtotal - line_net),
                    "vat_rate": product.vat_rate,
                    "vat_amount": float(line_vat.quantize(Decimal("0.01"), ROUND_HALF_UP)),
                    "applied_rules": applied_rules,
                }
            )
        grand_total = subtotal + vat_total
        approval_status = self._approval_status(customer, float(grand_total), request.payment_method)
        return {
            "customer_id": customer.customer_id,
            "branch_id": request.branch_id,
            "currency": "TRY",
            "lines": quote_lines,
            "subtotal": float(subtotal.quantize(Decimal("0.01"), ROUND_HALF_UP)),
            "discount_total": float(discount_total.quantize(Decimal("0.01"), ROUND_HALF_UP)),
            "vat_total": float(vat_total.quantize(Decimal("0.01"), ROUND_HALF_UP)),
            "grand_total": float(grand_total.quantize(Decimal("0.01"), ROUND_HALF_UP)),
            "payment_method": request.payment_method,
            "approval_status": approval_status,
            "workflow": self.workflow_for(approval_status),
        }

    def create_order(self, request: B2BOrderCreate, actor_id: str = "system", ip_address: str = "127.0.0.1") -> dict[str, Any]:
        quote = self.calculate_quote(request)
        order_id = f"B2B-{uuid4().hex[:6].upper()}"
        order = {
            "order_id": order_id,
            "customer_id": request.customer_id,
            "branch_id": request.branch_id,
            "order_date": _now(),
            "items": quote["lines"],
            "payment_method": request.payment_method,
            "shipping_address_id": request.shipping_address_id,
            "notes": request.notes,
            "channel": request.channel,
            "totals": {
                "subtotal": quote["subtotal"],
                "discount_total": quote["discount_total"],
                "vat_total": quote["vat_total"],
                "grand_total": quote["grand_total"],
            },
            "approval_status": quote["approval_status"],
            "workflow": quote["workflow"],
        }
        self.orders[order_id] = order
        for line in request.lines:
            self.reserve_stock(order_id, line.sku, line.quantity, request.branch_id)
        self.integration_jobs.append(self._erp_order_job(order))
        self.audit(actor_id, "order.create", "order", order_id, ip_address, {"grand_total": quote["grand_total"]})
        return order

    def reserve_stock(self, order_id: str, sku: str, quantity: int, branch_id: str) -> dict[str, Any]:
        available = self.inventory.get(sku, {}).get(branch_id, 0)
        if available < quantity:
            branch_id = "MERKEZ"
            available = self.inventory.get(sku, {}).get(branch_id, 0)
        if available < quantity:
            raise ValueError(f"Yetersiz stok: {sku}")
        self.inventory[sku][branch_id] -= quantity
        reservation = StockReservation(
            reservation_id=f"RSV-{uuid4().hex[:8].upper()}",
            order_id=order_id,
            sku=sku,
            quantity=quantity,
            warehouse_id=branch_id,
            expires_at=(datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat(),
        )
        self.reservations[reservation.reservation_id] = reservation
        return asdict(reservation)

    def workflow_for(self, approval_status: ApprovalStatus) -> list[dict[str, str]]:
        if approval_status == "auto_approved":
            return [{"step": "ERP sipariş fişi", "owner": "integration-service", "sla": "30 saniye"}]
        if approval_status == "waiting_finance":
            return [
                {"step": "Finans limit kontrolü", "owner": "finance-manager", "sla": "2 saat"},
                {"step": "ERP sipariş fişi", "owner": "integration-service", "sla": "30 saniye"},
            ]
        return [
            {"step": "Bayi yöneticisi onayı", "owner": "customer-approver", "sla": "4 saat"},
            {"step": "Satış müdürü marj onayı", "owner": "sales-manager", "sla": "4 saat"},
            {"step": "ERP sipariş fişi", "owner": "integration-service", "sla": "30 saniye"},
        ]

    def export_integration_packets(self) -> dict[str, Any]:
        return {
            "rest_endpoints": ["GET /b2b/products", "POST /b2b/orders", "GET /b2b/customers/{id}/balance"],
            "soap_actions": ["GetCariEkstre", "SendOrderToERP", "SyncStock", "CustomerStatementPDF"],
            "edi_transactions": ["X12 850 Purchase Order", "X12 810 Invoice", "EDIFACT ORDERS", "EDIFACT INVOIC"],
            "queued_jobs": self.integration_jobs,
            "mapper_files": ["integrations/erp/erp_field_mapping.json"],
        }

    def audit(self, actor_id: str, action: str, entity: str, entity_id: str, ip_address: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        event = AuditEvent(actor_id, action, entity, entity_id, ip_address, _now(), metadata or {})
        self.audit_trail.append(event)
        return asdict(event)

    def _best_unit_price(self, customer: CustomerAccount, product: B2BProduct, quantity: int) -> tuple[Decimal, list[str]]:
        price = money(product.list_price)
        applied: list[str] = []
        for rule in sorted(self.price_rules, key=lambda item: item.priority, reverse=True):
            if not self._rule_matches(rule, customer, product, quantity):
                continue
            if rule.net_price is not None:
                candidate = money(rule.net_price)
            else:
                candidate = price * (Decimal("1") - money(rule.discount_rate))
            if candidate < price:
                price = candidate
                applied.append(rule.rule_id)
        return price.quantize(Decimal("0.01"), ROUND_HALF_UP), applied

    def _rule_matches(self, rule: PriceRule, customer: CustomerAccount, product: B2BProduct, quantity: int) -> bool:
        return all(
            [
                rule.sku in (None, product.sku),
                rule.customer_id in (None, customer.customer_id),
                rule.tier in (None, customer.tier),
                quantity >= rule.min_quantity,
            ]
        )

    def _approval_status(self, customer: CustomerAccount, grand_total: float, payment_method: PaymentMethod) -> ApprovalStatus:
        if payment_method == "open_account" and customer.balance + grand_total > customer.credit_limit:
            return "waiting_finance"
        if grand_total > 250_000:
            return "waiting_manager"
        return "auto_approved"

    def _erp_order_job(self, order: dict[str, Any]) -> dict[str, Any]:
        return {
            "job_id": f"ERPJOB-{uuid4().hex[:8].upper()}",
            "type": "Push_Order_To_ERP",
            "status": "queued",
            "target": "LOGO|SAP|NETSIS|MIKRO adapter",
            "payload": {
                "FIS_NO": order["order_id"],
                "CARI_KOD": order["customer_id"],
                "SUBE_KOD": order["branch_id"],
                "ODEME_TIPI": order["payment_method"],
                "GENEL_TOPLAM": order["totals"]["grand_total"],
            },
            "created_at": _now(),
        }

    def _require_customer(self, customer_id: str) -> CustomerAccount:
        if customer_id not in self.customers:
            raise KeyError(f"Cari bulunamadı: {customer_id}")
        return self.customers[customer_id]

    def _require_product(self, sku: str) -> B2BProduct:
        if sku not in self.products:
            raise KeyError(f"Ürün bulunamadı: {sku}")
        return self.products[sku]


def money(value: float) -> Decimal:
    return Decimal(str(value))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
