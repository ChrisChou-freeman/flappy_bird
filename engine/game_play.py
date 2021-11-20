import os
from typing import Dict

import pygame
from pygame import surface, event, image, sprite, Vector2, mixer

from .lib import GameManager, pygame_load_images_list
from .sprites import Bird, Pipe
from . import settings

class GamePlay(GameManager):
    def __init__(self, metadata: Dict[str, str]) -> None:
        super().__init__(metadata)
        self.metadata = metadata
        # load images
        self.number_images = pygame_load_images_list(settings.NUMBER_IMG_PATH)
        self.background_image = image.load(os.path.join(settings.BACKGROUND_IMG_PATH, self.metadata['day_night']))
        self.ground_image = image.load(settings.GROUND_IMG_PATH)
        self.bird_image = image.load(os.path.join(settings.BIRD_IMG_PATHS, self.metadata['bird']))
        self.pipe_image_bottom = image.load(settings.PIPE_IMG_PATH)
        self.pipe_image_up = pygame.transform.rotate(self.pipe_image_bottom, 180)
        self.ground_x_cycle_width = 24
        self.forword_speed = 2
        # load sound effect
        self.sound_dict = {name: mixer.Sound(sound_path) for name, sound_path in settings.AUDIO_PATHS.items()}
        # start init game
        self.bird_group = sprite.Group()
        self.pipe_groop = sprite.Group()
        self.game_started: bool
        self.score: int
        self.counter: int
        self.bird_pos: Vector2
        self.groud_pos: Vector2
        self.bird_sprite: Bird
        self._init_game()

    def _init_game(self) -> None:
        self.bird_group.empty()
        self.pipe_groop.empty()
        self.bird_pos = Vector2(
            settings.SCREEN_WIDTH*0.2,
            (settings.SCREEN_HEIGHT-self.bird_image.get_height())/2
        )
        self.ground_pos = settings.GOUND_POS
        self.bird_sprite = Bird(self.bird_image, self.metadata, self.bird_pos)
        self.bird_group.add(self.bird_sprite)
        pipe_pos = Pipe.random_pipe(self.pipe_image_up)
        for i in range(2):
            start_pipe_x_pos = settings.SCREEN_WIDTH+200+i*settings.SCREEN_WIDTH/2
            self.pipe_groop.add(
                Pipe(
                    image=self.pipe_image_up,
                    position=Vector2(start_pipe_x_pos, pipe_pos['top'][-1])
                )
            )
            self.pipe_groop.add(
                Pipe(
                    image=self.pipe_image_bottom,
                    position=Vector2(start_pipe_x_pos, pipe_pos['bottom'][-1])
                )
            )
        self.game_started = True
        self.score = 0
        self.counter = 0

    def handle_input(self, key_event: event.Event) -> None:
        if key_event.type == pygame.KEYDOWN:
            if key_event.key == pygame.K_BACKSPACE:
                self.metadata['game_mode'] = 'game_start'
            if key_event.key == pygame.K_SPACE or key_event.key == pygame.K_UP:
                self.game_started = True
                if not self.bird_sprite.is_dead:
                    self.bird_sprite.setFlapped()
                    self.sound_dict['swoosh'].play()

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

    def _move_pipe(self) -> None:
        for pipe in self.pipe_groop:
            if pipe.rect is not None:
                pipe.rect.left -= self.forword_speed

    def _move_forword(self) -> None:
        if not self.bird_sprite.is_dead:
            self.ground_pos.x = -(self.counter%self.ground_x_cycle_width)
            self._move_pipe()
        elif self.bird_sprite.is_dead and self.game_started:
            self.game_started = False
            self.sound_dict['hit'].play()
            self.sound_dict['die'].play()

    def update(self, dt: float) -> None:
        if not self.game_started:
            return
        self.counter += self.forword_speed
        self.bird_group.update(dt=dt, boundary=[0, self.ground_pos.y])
        self.pipe_groop.update(dt=dt, boundary=[0, self.ground_pos.y])
        self._move_forword()

    def draw(self, screen: surface.Surface) -> None:
        screen.blit(self.background_image, (0, 0))
        self._show_hud(screen)
        self.pipe_groop.draw(screen)
        screen.blit(self.ground_image, self.ground_pos)
        self.bird_group.draw(screen)

    def clear(self, screen: surface.Surface) -> None:
        screen.fill(settings.RGB_BLACK)

