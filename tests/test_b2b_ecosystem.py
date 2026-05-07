from api.b2b_ecosystem import B2BEcosystemStore, B2BOrderCreate, B2BOrderLine


def test_enterprise_blueprint_lists_tailor_made_files_and_layers() -> None:
    store = B2BEcosystemStore()
    blueprint = store.platform_blueprint()

    assert "ERP/EDI/API entegrasyon köprüsü" in blueprint["layers"]
    assert blueprint["data_files"]["order_schema"] == "schemas/order_schema.json"
    assert blueprint["data_files"]["kubernetes"] == "deploy/saas/k8s/prob2b-api-deployment.yaml"


def test_quote_applies_customer_tier_and_volume_pricing() -> None:
    store = B2BEcosystemStore()
    quote = store.calculate_quote(
        B2BOrderCreate(
            customer_id="CARI-99",
            branch_id="ANKARA-SUBE",
            lines=[B2BOrderLine(sku="PROD-X", quantity=100)],
            notes="Acil teslimat",
        )
    )

    line = quote["lines"][0]
    assert line["net_unit_price"] == 37.26
    assert line["applied_rules"] == ["PR-CARI99-PRODX", "PR-GOLD", "PR-VOLUME-100"]
    assert quote["approval_status"] == "auto_approved"
    assert quote["grand_total"] == 4471.2


def test_order_reserves_stock_queues_erp_job_and_audits() -> None:
    store = B2BEcosystemStore()
    order = store.create_order(
        B2BOrderCreate(
            customer_id="CARI-99",
            branch_id="ANKARA-SUBE",
            lines=[B2BOrderLine(sku="PROD-X", quantity=100)],
            channel="api",
        ),
        actor_id="buyer-1",
        ip_address="10.0.0.8",
    )

    assert order["order_id"].startswith("B2B-")
    assert store.inventory["PROD-X"]["ANKARA-SUBE"] == 3900
    assert next(iter(store.reservations.values())).warehouse_id == "ANKARA-SUBE"
    assert store.integration_jobs[0]["type"] == "Push_Order_To_ERP"
    assert store.audit_trail[0].action == "order.create"


def test_credit_limit_routes_large_open_account_order_to_finance() -> None:
    store = B2BEcosystemStore()
    quote = store.calculate_quote(
        B2BOrderCreate(
            customer_id="CARI-99-ALT-01",
            branch_id="MERKEZ",
            lines=[B2BOrderLine(sku="PROD-X", quantity=3000)],
            payment_method="open_account",
        )
    )

    assert quote["approval_status"] == "waiting_finance"
    assert quote["workflow"][0]["owner"] == "finance-manager"
