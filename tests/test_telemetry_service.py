from api.telemetry_service import TelemetryStore


def test_telemetry_store_records_event(tmp_path) -> None:
    store = TelemetryStore(tmp_path / "events.jsonl")
    event = store.record("startup", {"ok": True})
    assert event.kind == "startup"
    assert store.list_events()[0]["payload"] == {"ok": True}
