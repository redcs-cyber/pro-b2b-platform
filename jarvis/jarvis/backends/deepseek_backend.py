from openai import OpenAI

from .base import BrainBackend


class DeepSeekBackend(BrainBackend):
    name = "deepseek"

    def __init__(self, api_key: str, model: str = "deepseek-chat") -> None:
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com") if api_key else None
        self.model = model

    def complete(self, prompt: str) -> str:
        if self.client is None:
            raise RuntimeError("DEEPSEEK_API_KEY tanımlı değil")
        result = self.client.chat.completions.create(model=self.model, messages=[{"role": "user", "content": prompt}])
        return result.choices[0].message.content or ""
