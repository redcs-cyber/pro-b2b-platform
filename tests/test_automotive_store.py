from api.automotive import AutomotiveStore, OrderCreate, OrderLine, StockMutation


def test_automotive_overview_exposes_handheld_terminal_workflows() -> None:
    data = AutomotiveStore().ecosystem_overview()
    assert "El terminali görev kuyruğu" in data["modules"]
    assert "sipariş toplama" in data["handheld_terminal"]["supported_workflows"]


def test_order_creates_terminal_pick_task() -> None:
    store = AutomotiveStore()
    order = store.create_order(
        OrderCreate(
            customer_name="Ankara Oto Servis",
            channel="b2b_portal",
            lines=[OrderLine(sku="FRN-BLK-001", quantity=2)],
        )
    )
    assert order["total"] == 2580.0

    tasks = store.list_terminal_tasks("HT-01")
    assert any(task["sku"] == "FRN-BLK-001" and task["task_type"] == "toplama" for task in tasks)


def test_inventory_update_validates_known_sku() -> None:
    store = AutomotiveStore()
    snapshot = store.set_stock("FLT-YAG-010", StockMutation(location="magaza", quantity=16))
    assert snapshot["locations"]["magaza"] == 16

    try:
        store.set_stock("YOK-001", StockMutation(location="magaza", quantity=1))
    except KeyError as exc:
        assert "Parça bulunamadı" in str(exc)
    else:
        raise AssertionError("Bilinmeyen SKU için KeyError bekleniyordu")
