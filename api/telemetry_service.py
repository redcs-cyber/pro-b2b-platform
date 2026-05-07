import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class TelemetryEvent:
    kind: str
    payload: dict[str, Any]
    timestamp: str


class TelemetryStore:
    def __init__(self, path: Path | str = "jarvis/telemetry/events.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, kind: str, payload: dict[str, Any] | None = None) -> TelemetryEvent:
        event = TelemetryEvent(
            kind=kind,
            payload=payload or {},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")
        return event

    def list_events(self, limit: int = 100) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").splitlines()[-limit:]
        return [json.loads(line) for line in lines if line.strip()]
