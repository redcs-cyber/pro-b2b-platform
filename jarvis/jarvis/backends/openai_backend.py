from openai import OpenAI

from .base import BrainBackend


class OpenAIBackend(BrainBackend):
    name = "openai"

    def __init__(self, api_key: str, model: str = "gpt-4.1-mini") -> None:
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = model

    def complete(self, prompt: str) -> str:
        if self.client is None:
            raise RuntimeError("OPENAI_API_KEY tanımlı değil")
        result = self.client.responses.create(model=self.model, input=prompt)
        return result.output_text
