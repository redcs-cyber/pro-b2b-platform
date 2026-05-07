def render_status(status: dict) -> str:
    return " | ".join(f"{key}={value}" for key, value in status.items())
