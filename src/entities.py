import math

import pygame as pg


class TemperatureBar:
    def __init__(
            self, 
            pos: tuple, 
            size: tuple, 
            image: pg.Surface
        ):
        self.pos = pos
        self.size = size
        self.fill = 50
        self.max_fill = 100
        self.fill_color = (225, 55, 55)
        self.image = image
        self.image = pg.transform.smoothscale(self.image, size)
        self.image_rect = self.image.get_rect(topleft=pos)
        self.fill_rect = pg.Rect(*pos, self.fill, size[1] // 4)
        self.fill_rect.y = pos[1] + size[1] // 2 - self.fill_rect.h // 2
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
        self.fill_rect.w = self.fill_width
        pg.draw.rect(screen, self.fill_color, self.fill_rect)
        screen.blit(self.image, self.pos)


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
    def __init__(self, *args, effect: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.effect = effect
        self.sideways_motion = False


class Cursor(pg.sprite.Sprite):
    def __init__(
            self, 
            groups: list[pg.sprite.Group], 
            size: tuple, 
            image: pg.Surface
        ):
        super().__init__(*groups)
        self.image = pg.transform.smoothscale(image, size)
        self.display_rect = self.image.get_rect()
        self.rect = self.display_rect.inflate(-30, -30)

    def update(self, dt):
        self.display_rect.center = pg.mouse.get_pos()
        self.rect.center = self.display_rect.center

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.display_rect)
        

class InfoText(pg.sprite.Sprite):
    def __init__(
            self, 
            groups: list[pg.sprite.Group], 
            pos: tuple, 
            dist_to_live: int, 
            fade_speed: int, 
            image: pg.Surface
        ):
        super().__init__(*groups)
        self.pos = pos
        self.dist_to_live = dist_to_live
        self.fade_speed = fade_speed
        self.image = image
        self.rect = self.image.get_rect(midbottom=pos)
        self.alpha = 255

    def update(self, dt):
        self.rect.y -= 50 * dt
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)
        if self.rect.y < (self.pos[1] - self.dist_to_live):
            self.kill()

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect.topleft)
