import json
from pathlib import Path

REQUIRED_FILES = [
    "vercel.json",
    "api/vercel_app.py",
    "requirements.txt",
    "api/server.py",
    "api/static/dashboard.html",
    "docs/vercel-deploy-tr.md",
]
REQUIRED_ROUTES = ["/(.*)"]


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not Path(path).exists()]
    if missing:
        raise SystemExit(f"Vercel için eksik dosyalar: {', '.join(missing)}")

    config = json.loads(Path("vercel.json").read_text(encoding="utf-8"))
    routes = [route["src"] for route in config.get("routes", [])]
    missing_routes = [route for route in REQUIRED_ROUTES if route not in routes]
    if missing_routes:
        raise SystemExit(f"Vercel route eksik: {', '.join(missing_routes)}")

    build_sources = [build["src"] for build in config.get("builds", [])]
    if "api/vercel_app.py" not in build_sources:
        raise SystemExit("Vercel Python build kaynağı api/vercel_app.py olmalı")

    print("Vercel deploy check passed")


if __name__ == "__main__":
    main()
