from abc import ABC, abstractmethod


class BrainBackend(ABC):
    name: str

    @abstractmethod
    def complete(self, prompt: str) -> str:
        raise NotImplementedError
