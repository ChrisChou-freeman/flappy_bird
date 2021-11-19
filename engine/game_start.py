import os
import random
from typing import Dict

import pygame
from pygame import surface, event, Vector2

from .lib import listdir_clean, GameManager, Animation
from . import settings

class GameStart(GameManager):
    def __init__(self, metadata: Dict[str, str]) -> None:
        super().__init__(metadata)
        self.bird: str = random.choice(listdir_clean(settings.BIRD_IMG_PATHS))
        self.day_night: str = random.choice(listdir_clean(settings.BACKGROUND_IMG_PATH))
        self.metadata['bird'] = self.bird
        self.metadata['day_night'] = self.day_night
        self.bird_image = pygame.image.load(os.path.join(settings.BIRD_IMG_PATHS, self.bird))
        self.background_image = pygame.image.load(os.path.join(settings.BACKGROUND_IMG_PATH, self.day_night))
        self.ground_image = pygame.image.load(settings.GROUND_IMG_PATH)
        self.start_image = pygame.image.load(settings.GAME_START_IMG_PATH)
        self.ground_pos = settings.GOUND_POS
        self.start_pos = Vector2(
            (settings.SCREEN_WIDTH-self.start_image.get_width())/2,
            settings.SCREEN_HEIGHT*0.12
        )
        self.bird_pos = Vector2(
            settings.SCREEN_WIDTH*0.2,
            (settings.SCREEN_HEIGHT-self.bird_image.get_height())/2
        )
        self.bird_animation = Animation(
            os.path.join(settings.BIRD_IMG_PATHS, self.bird),
            self.bird_pos,
            34
        )
        self.bird_y_wave_height = 8
        self.ground_x_cycle_width = 24
        self.offset_value = -1
        self.animation_frequency = 2
        self.bird_y_offset_value = 0
        self.counter = 0

    def handle_input(self, key_event: event.Event) -> None:
        if key_event.type == pygame.KEYDOWN:
            if key_event.key == pygame.K_SPACE or key_event.key == pygame.K_UP:
                self.metadata['game_mode'] = 'game_play'

    def _bird_wave(self) -> None:
        self.bird_y_offset_value += self.offset_value
        if self.bird_y_offset_value % self.animation_frequency == 0:
            self.bird_animation.location.y += self.offset_value
            if self.bird_y_offset_value >= self.bird_y_wave_height and self.offset_value == 1:
                self.offset_value = -1
            elif self.bird_y_offset_value <= self.bird_y_wave_height * -1 * 2 and self.offset_value == -1:
                self.offset_value = 1

    def _ground_move(self) -> None:
        self.ground_pos.x = -(self.counter%self.ground_x_cycle_width)

    def update(self, _) -> None:
        self.counter += 1
        self._bird_wave()
        self._ground_move()
        self.bird_animation.update()

    def draw(self, screen: surface.Surface) -> None:
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.ground_image, self.ground_pos)
        screen.blit(self.start_image, self.start_pos)
        self.bird_animation.draw(screen)

    def clear(self, screen: surface.Surface) -> None:
        screen.fill(settings.RGB_BLACK)

