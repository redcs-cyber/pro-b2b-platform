from pathlib import Path

REQUIRED = ["README.md", "requirements.txt", "api/server.py", "jarvis/jarvis/main.py"]


def main() -> None:
    missing = [path for path in REQUIRED if not Path(path).exists()]
    if missing:
        raise SystemExit(f"Eksik dosyalar: {', '.join(missing)}")
    print("Self check passed")


if __name__ == "__main__":
    main()
