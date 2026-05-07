import json
from pathlib import Path


class MCPRegistry:
    def __init__(self, config_path: str | Path = "mcp_servers.json") -> None:
        self.config_path = Path(config_path)

    def load(self) -> dict:
        if not self.config_path.exists():
            return {"servers": {}}
        return json.loads(self.config_path.read_text(encoding="utf-8"))
