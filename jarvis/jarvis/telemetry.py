import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class Telemetry:
    def __init__(self, path: str | Path = "telemetry/events.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, kind: str, payload: dict[str, Any] | None = None) -> None:
        event = {"kind": kind, "payload": payload or {}, "timestamp": datetime.now(timezone.utc).isoformat()}
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")
