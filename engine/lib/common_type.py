from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Dict

from pygame import surface, event

@dataclass
class Position:
    x: int
    y: int

@dataclass
class PositionF:
    x: float
    y: float


class GameManager(ABC):
    def __init__(self, metadata: Dict[str, str]):
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
