import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    brain_providers: tuple[str, ...] = tuple(p.strip() for p in os.getenv("BRAIN_PROVIDERS", "ollama,deepseek,openai").split(",") if p.strip())
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
