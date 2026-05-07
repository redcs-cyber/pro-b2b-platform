from collections.abc import Iterable

from .base import BrainBackend


class MultiProviderRouter:
    def __init__(self, backends: Iterable[BrainBackend]) -> None:
        self.backends = list(backends)

    def complete(self, prompt: str) -> str:
        errors: list[str] = []
        for backend in self.backends:
            try:
                return backend.complete(prompt)
            except Exception as exc:
                errors.append(f"{backend.name}: {exc}")
        raise RuntimeError("Tüm sağlayıcılar başarısız: " + "; ".join(errors))
