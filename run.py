import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def spawn(cmd: list[str]) -> subprocess.Popen:
    return subprocess.Popen(cmd, cwd=ROOT)


def main() -> None:
    procs = [
        spawn([sys.executable, "core/main.py"]),
        spawn([sys.executable, "api/server.py"]),
    ]
    print("Jarvis launcher started. Ctrl+C to stop all services.")
    try:
        while True:
            dead = [p for p in procs if p.poll() is not None]
            if dead:
                raise RuntimeError("One or more subprocesses exited unexpectedly.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping services...")
    finally:
        for p in procs:
            p.terminate()


if __name__ == "__main__":
    main()
