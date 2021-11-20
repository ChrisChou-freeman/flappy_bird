import sys
from typing import Optional, Type, Dict

import pygame
from pygame import event, surface

from . import settings
from .lib import GameManager
from .game_start import GameStart
from .game_play import GamePlay

class MainGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        self.screen = self._create_screen()
        self.game_metadata = {
            'bird': '',
            'day_night': '',
            'game_mode': 'game_start'
        }
        self.game_mode: Dict[str, Type[GameManager]] = {
            'game_start': GameStart,
            'game_play': GamePlay
        }
        self.score = 0
        self.game_manager: Optional[GameManager] = None

    def _create_screen(self) -> surface.Surface:
        screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        return screen

    def _handle_input(self, key_event: event.Event) -> None:
        if key_event.type == pygame.QUIT \
                or (key_event.type == pygame.KEYDOWN and key_event.key == pygame.K_ESCAPE):
                self._quit()
                print('0')
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
        while True:
            switch_mode = self.game_metadata['game_mode']
            if not isinstance(self.game_manager, self.game_mode[switch_mode]):
                if self.game_manager is not None:
                   self.game_manager.clear(self.screen)
                self.game_manager = self.game_mode[switch_mode](self.game_metadata)
            for key_event in event.get():
                self._handle_input(key_event)
            self._draw()
            self._update(float(clock.get_time()/1000))
            clock.tick(settings.FPS)

