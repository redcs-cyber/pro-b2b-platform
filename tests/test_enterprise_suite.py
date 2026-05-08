from api.b2b_ecosystem import B2BOrderCreate, B2BOrderLine, B2BEcosystemStore
from api.enterprise_suite import ApprovalRequest, EnterpriseSuite, ReturnCreate, ShipmentCreate
from api.quick_order import parse_quick_order_csv


def test_feature_catalog_and_acl_cover_enterprise_domains() -> None:
    suite = EnterpriseSuite()
    catalog = suite.mega_feature_catalog()

    assert "shipment" in catalog["domains"]["operations"]
    assert suite.can("buyer", "order.create", 40_000)
    assert not suite.can("buyer", "order.create", 75_000)


def test_workflow_payment_plan_shipment_return_and_notifications() -> None:
    suite = EnterpriseSuite()
    decision = suite.decide_workflow(
        ApprovalRequest(
            order_total=320_000,
            customer_id="CARI-99",
            actor_role="buyer",
            payment_method="open_account",
            credit_limit_exceeded=True,
        )
    )
    assert decision["decision"] == "needs_finance"

    plan = suite.create_payment_plan(1200, term_days=30, installments=3)
    assert [item["amount"] for item in plan["installments"]] == [400.0, 400.0, 400.0]

    shipment = suite.create_shipment(
        ShipmentCreate("B2B-123456", "fleet", "ANKARA-SUBE", "ADDR-01", package_count=2, desi=14.5)
    )
    assert shipment["tracking_number"].startswith("TRK")

    rma = suite.create_return(ReturnCreate("B2B-123456", "PROD-X", 1, "wrong_item"))
    assert rma["status"] == "approved"
    assert suite.analytics_snapshot()["notifications_queued"] == 2


def test_quick_order_parser_and_search_index() -> None:
    parsed = parse_quick_order_csv("sku,quantity\nPROD-X,100\nBAD,0\n")
    assert parsed.lines[0].sku == "PROD-X"
    assert parsed.errors[0]["row"] == 3

    suite = EnterpriseSuite(B2BEcosystemStore())
    index = suite.build_search_index()
    assert any("yüksek karbon" in item["tokens"] for item in index)


def test_analytics_counts_orders_and_reservations() -> None:
    store = B2BEcosystemStore()
    store.create_order(B2BOrderCreate("CARI-99", "ANKARA-SUBE", [B2BOrderLine("PROD-X", 100)]))
    suite = EnterpriseSuite(store)

    snapshot = suite.analytics_snapshot()
    assert snapshot["orders"] == 1
    assert snapshot["reserved_units"] == 100
    assert snapshot["gmv"] == 4471.2
