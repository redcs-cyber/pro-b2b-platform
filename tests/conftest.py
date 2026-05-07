import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JARVIS_ROOT = ROOT / "jarvis"
for path in (ROOT, JARVIS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
