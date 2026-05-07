import requests

from .base import BrainBackend


class OllamaBackend(BrainBackend):
    name = "ollama"

    def __init__(self, url: str = "http://localhost:11434", model: str = "llama3") -> None:
        self.url = url.rstrip("/")
        self.model = model

    def complete(self, prompt: str) -> str:
        response = requests.post(f"{self.url}/api/generate", json={"model": self.model, "prompt": prompt, "stream": False}, timeout=30)
        response.raise_for_status()
        return response.json().get("response", "")
