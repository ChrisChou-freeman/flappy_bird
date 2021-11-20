import random
from typing import Dict

from pygame import sprite, surface, mask, Vector2

from .. import settings

class Pipe(sprite.Sprite):
    def __init__(self, image: surface.Surface, position: Vector2) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = mask.from_surface(self.image)
        self.rect.left, self.rect.top = int(position.x), int(position.y)
        self.used_for_sore = False

    @staticmethod
    def random_pipe(image: surface.Surface) -> Dict[str, Vector2]:
        base_y = 0.79 * settings.SCREEN_HEIGHT
        up_y = int(base_y * 0.2) + random.randrange(0, int(base_y * 0.6 - settings.PIPE_GAP_SIZE))
        pip_poz = {
            'top': Vector2(settings.SCREEN_WIDTH + 10, up_y - image.get_height()),
            'bottom': Vector2(settings.SCREEN_WIDTH + 10, up_y + settings.PIPE_GAP_SIZE)
        }
        return pip_poz

