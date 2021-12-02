from abc import ABC, abstractmethod

from pygame import surface, event

class GameManager(ABC):
    def __init__(self, metadata: dict[str, str]) -> None:
        self.metadata = metadata

    @abstractmethod
    def handle_input(self, key_event: event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: surface.Surface) -> None:
        pass

    @abstractmethod
    def clear(self, screen: surface.Surface) -> None:
        pass
