from typing import Dict, List

from pygame import Vector2, surface

from .sprite_animation import SpriteAnimation

class Bird(SpriteAnimation):
    def __init__(self, img: surface.Surface, metadata: Dict[str, str], position: Vector2) -> None:
        super().__init__(img, position, 34)
        self.metadata = metadata
        self.is_flapped = False
        self.up_speed_limit = 4.0
        self.up_speed = self.up_speed_limit
        self.down_speed = 0.0
        self.is_dead = False

    def update(self, *_, **kwargs) -> None:
        if not self.is_dead:
            self.play()
        time_passed: float = kwargs['dt']
        boundary: List[int] = kwargs['boundary']
        if self.is_flapped:
            self.up_speed -= 30 * time_passed
            if self.rect is not None:
                self.rect.top -= int(self.up_speed)
            if self.up_speed <= 0:
                self.unsetFlapped()
                self.up_speed = 9
                self.down_speed = 0
        else:
            self.down_speed += 8 * time_passed
            if self.rect is not None:
                self.rect.bottom += int(self.down_speed)
        if self.rect is not None:
            if self.rect.bottom > boundary[1]:
                self.is_dead = True
                self.up_speed = 0
                self.down_speed = 0
                self.rect.bottom = boundary[1]
            if self.rect.top < boundary[0]:
                self.is_dead = True
                self.up_speed = 0
                self.down_speed = 0
                self.rect.top = boundary[0]

    def setFlapped(self) -> None:
        if self.is_flapped:
            self.up_speed = max(self.up_speed_limit, self.up_speed + 1)
        else:
            self.is_flapped = True

    def unsetFlapped(self) -> None:
        self.is_flapped = False

