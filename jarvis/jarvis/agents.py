from dataclasses import dataclass


@dataclass
class GoodMoodEngine:
    score: int = 50

    def observe(self, text: str) -> int:
        positive = {"teşekkür", "harika", "süper", "iyi"}
        negative = {"hata", "kötü", "sorun", "acil"}
        lowered = text.lower()
        if any(word in lowered for word in positive):
            self.score = min(100, self.score + 5)
        if any(word in lowered for word in negative):
            self.score = max(0, self.score - 5)
        return self.score


def classify_intent(text: str) -> str:
    lowered = text.lower()
    if lowered.startswith(("aç ", "çalıştır ", "run ")):
        return "command"
    return "llm"
