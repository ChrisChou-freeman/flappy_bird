import os
from typing import Dict

import pygame
from pygame import surface, event, image

from .lib import GameManager, pygame_load_images_list
from . import settings

class GamePlay(GameManager):
    def __init__(self, metadata: Dict[str, str]) -> None:
        super().__init__(metadata)
        self.metadata = metadata
        self.number_images = pygame_load_images_list(settings.NUMBER_IMG_PATH)
        self.bird_image = image.load(os.path.join(settings.BIRD_IMG_PATHS, self.metadata['bird']))
        self.score = 0

    def handle_input(self, key_event: event.Event) -> None:
        if key_event.key == pygame.K_SPACE or key_event.key == pygame.K_UP:
            self.metadata['game_mode'] = 'game_start'

    def _show_score(self, score: int, screen: surface.Surface) -> None:
        digits = list(str(score))
        width = 0
        for d in digits:
            width += self.number_images[int(d)].get_width()
        offset = (settings.SCREEN_WIDTH - width) / 2
        for d in digits:
            screen.blit(self.number_images[int(d)], (offset, settings.SCREEN_HEIGHT*0.1))
            offset += self.number_images[int(d)].get_width()

    def _show_hud(self, screen: surface.Surface) -> None:
        self._show_score(self.score, screen)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: surface.Surface) -> None:
        self._show_hud(screen)
