import math
import random

import pygame as pg


class TemperatureBar:
    def __init__(self, pos, size, image: pg.Surface):
        self.pos = pos
        self.size = size
        self.fill = 50
        self.max_fill = 100
        self.fill_color = (255, 55, 55)
        self.background_color = (60, 60, 60, 100)
        self.image = image
        self.image = pg.transform.smoothscale(self.image, size)
        self.rect = pg.Rect(self.pos, self.size)
        self.fill_ratio = self.fill / self.max_fill
        self.fill_rate = 0.01
        self.depletion_rate = 5.0
        self.distance_moved = 0

    def update(self, dt):
        if self.distance_moved > 0:
            self.fill += self.distance_moved * self.fill_rate

        self.fill -= self.depletion_rate * dt

        self.fill_ratio = self.fill / self.max_fill
        self.fill_width = self.fill_ratio * self.size[0]

    def draw(self, screen: pg.Surface):
        rect_coords = (*self.pos, self.fill_width, self.size[1])
        pg.draw.rect(screen, self.fill_color, rect_coords)
        screen.blit(self.image, self.pos)
        # pg.draw.rect(screen, (255, 255, 255), self.rect, 2)


class FallingThing(pg.sprite.Sprite):
    def __init__(
        self, 
        groups: list[pg.sprite.Group], 
        pos: tuple, 
        speed: int, 
        image: pg.Surface, 
        screen_height: int
    ):
        super().__init__(*groups)
        self.image = image
        self.size = self.image.get_size()
        self.rect = self.image.get_rect(topleft=pos)
        self.screen_height = screen_height
        self.pos = pg.Vector2(pos)
        self.speed = speed
        self.sideways_motion = True

    def update(self, dt):
        self.pos.y += self.speed * dt
        self.rect.y = round(self.pos.y)
        if self.sideways_motion:
            self.pos.x += math.sin(self.pos.y / 10) * 200 * dt
            self.rect.x = round(self.pos.x)
        if self.rect.y - self.rect.h > self.screen_height:
            self.kill()

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect.topleft)


class PowerUp(FallingThing):
    def __init__(
        self, 
        groups: list[pg.sprite.Group], 
        pos: tuple, 
        speed: int, 
        image: pg.Surface, 
        screen_height: int,
        effect: str
    ):
        super().__init__(groups, pos, speed, image, screen_height)
        self.effect = effect

    def update(self, dt):
        self.pos.y += self.speed * dt
        self.rect.y = round(self.pos.y)
        if self.rect.y - self.rect.h > self.screen_height:
            self.kill()


class Cursor(pg.sprite.Sprite):
    def __init__(self, groups, size, image):
        super().__init__(*groups)
        self.image = pg.transform.smoothscale(image, size)
        self.rect = self.image.get_rect()

    def update(self, dt):
        self.rect.center = pg.mouse.get_pos()
        