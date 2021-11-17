import sys
from typing import Optional

import pygame
from pygame import event, surface

from . import settings
from .game_start import GameStart
from .lib import GameManager

class MainGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = self._create_screen()
        self.game_metadata = {
            'bird': '',
            'game_mode': 'game_start'
        }
        self.game_mode = {
            'game_start': GameStart
        }
        self.score = 0
        self.game_manager: Optional[GameManager] = None

    def _create_screen(self) -> surface.Surface:
        screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        return screen

    def _handle_input(self, key_event: event.Event) -> None:
        if key_event.type == pygame.QUIT \
                or (key_event.type == pygame.KEYDOWN and key_event.key == pygame.KSCAN_ESCAPE):
                self._quit()
        if self.game_manager is not None:
            self.game_manager.handle_input(key_event)

    def _draw(self) -> None:
        if self.game_manager is not None:
            self.game_manager.draw(self.screen)

    def _update(self, dt: float) -> None:
        if self.game_manager is not None:
            self.game_manager.update(dt)
        pygame.display.update()

    def _quit(self) -> None:
        pygame.quit()
        sys.exit()

    def run(self) -> None:
        clock = pygame.time.Clock()
        is_game_running = True
        while is_game_running:
            switch_mode = self.game_metadata['game_mode']
            if not isinstance(self.game_manager, self.game_mode[switch_mode]):
                self.game_manager = self.game_mode[switch_mode](self.game_metadata)
            for key_event in event.get():
                self._handle_input(key_event)
            self._draw()
            self._update(float(clock.get_time()/1000))
            clock.tick(settings.FPS)

