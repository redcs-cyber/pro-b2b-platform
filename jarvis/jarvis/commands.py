import subprocess

ALLOWED_COMMANDS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
}


def run_command(name: str) -> str:
    if name not in ALLOWED_COMMANDS:
        raise ValueError(f"Komut beyaz listede değil: {name}")
    subprocess.Popen(ALLOWED_COMMANDS[name])
    return f"Komut başlatıldı: {name}"
