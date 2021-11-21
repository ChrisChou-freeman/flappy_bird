import os
from typing import Dict, List

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
        self.game_over_image = image.load(settings.GAME_OVER_IMG_PATH)
        self.ground_image = image.load(settings.GROUND_IMG_PATH)
        self.bird_image = image.load(os.path.join(settings.BIRD_IMG_PATHS, self.metadata['bird']))
        self.pipe_image_bottom = image.load(settings.PIPE_IMG_PATH)
        self.pipe_image_up = pygame.transform.rotate(self.pipe_image_bottom, 180)
        self.ground_x_cycle_width = 24
        self.forword_speed = 2
        self.game_over_pos = Vector2(
            settings.SCREEN_WIDTH / 2 - self.game_over_image.get_width() / 2,
            settings.SCREEN_HEIGHT / 2 - self.game_over_image.get_height()
        )
        # load sound effect
        self.sound_dict = {name: mixer.Sound(sound_path) for name, sound_path in settings.AUDIO_PATHS.items()}
        # start init game
        self.bird_group = sprite.Group()
        self.pipe_groop = sprite.Group()
        self.scored_pipe: List[sprite.Sprite]
        self.game_started: bool
        self.score: float
        self.counter: int
        self.bird_pos: Vector2
        self.groud_pos: Vector2
        self.bird_sprite: Bird
        self._init_game()

    def _init_game(self) -> None:
        self.bird_group.empty()
        self.pipe_groop.empty()
        self.scored_pipe = []
        self.bird_pos = Vector2(
            settings.SCREEN_WIDTH*0.2,
            (settings.SCREEN_HEIGHT - self.bird_image.get_height()) / 2
        )
        self.ground_pos = settings.GOUND_POS
        self.bird_sprite = Bird(self.bird_image, self.metadata, self.bird_pos)
        self.bird_group.add(self.bird_sprite)
        for i in range(3):
            pipe_pos = Pipe.random_pipe(self.pipe_image_up)
            start_pipe_x_pos = settings.SCREEN_WIDTH + 200 + i * (settings.SCREEN_WIDTH / 2 + 50)
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
                if not self.game_started:
                    self.game_started = True
                    self._init_game()
                self.game_started = True
                if not self.bird_sprite.is_dead:
                    self.bird_sprite.setFlapped()
                    self.sound_dict['swoosh'].play()

    def _show_score(self, score: float, screen: surface.Surface) -> None:
        digits = list(str(int(score)))
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
            if pipe.rect is not None and self.bird_sprite.rect is not None:
                if pipe.rect.colliderect(self.bird_sprite.rect):
                    self.bird_sprite.is_dead = True
                    return
                else:
                    pipe.rect.left -= self.forword_speed
            if pipe.rect is not None and self.bird_sprite.rect is not None:
                if pipe not in self.scored_pipe \
                        and pipe.alive() \
                        and pipe.rect.centerx < self.bird_sprite.rect.centerx:
                    self.score += 0.5
                    self.scored_pipe.append(pipe)
                if '.5' in str(self.score):
                    self.sound_dict['point'].play()
        self.scored_pipe = list(filter(lambda pipe: pipe.alive(), self.scored_pipe))

    def _move_forword(self) -> None:
        if not self.bird_sprite.is_dead:
            self.ground_pos.x = -(self.counter%self.ground_x_cycle_width)
            self._move_pipe()
        elif self.bird_sprite.is_dead and self.game_started:
            self.game_started = False
            self.sound_dict['hit'].play()
            self.sound_dict['die'].play()

    def _gen_pipe(self) -> None:
        if len(self.pipe_groop) < 3:
            pipe_pos = Pipe.random_pipe(self.pipe_image_up)
            self.pipe_groop.add(Pipe(self.pipe_image_up, pipe_pos['top']))
            self.pipe_groop.add(Pipe(self.pipe_image_bottom, pipe_pos['bottom']))

    def update(self, dt: float) -> None:
        self.bird_group.update(dt=dt, boundary=[0, self.ground_pos.y])
        if not self.game_started:
            return
        self._gen_pipe()
        self.counter += self.forword_speed
        self.pipe_groop.update(dt=dt, boundary=[0, self.ground_pos.y])
        self._move_forword()

    def draw(self, screen: surface.Surface) -> None:
        screen.blit(self.background_image, (0, 0))
        self.bird_group.draw(screen)
        self.pipe_groop.draw(screen)
        screen.blit(self.ground_image, self.ground_pos)
        self._show_hud(screen)
        if self.bird_sprite.is_dead:
            screen.blit(self.game_over_image, self.game_over_pos)

    def clear(self, screen: surface.Surface) -> None:
        screen.fill(settings.RGB_BLACK)

