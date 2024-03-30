from typing import TYPE_CHECKING
import random

import pygame as pg

if TYPE_CHECKING:
    from src.app import App


class Assets:
    def __init__(self, app: "App"):
        self.app = app
        self.images = {
            "thermometer": pg.image.load("assets/images/thermometer.png").convert_alpha(),
            "player": pg.image.load("assets/images/player.png").convert_alpha(),
            "falling_things": self.create_random_fallers(),
        }
        self.sfx = {
            "gain_life": {"sound": pg.mixer.Sound("assets/sfx/gain_life.ogg"), "volume": 0.1},
            "lose_life": {"sound": pg.mixer.Sound("assets/sfx/lose_life.ogg"), "volume": 0.1},
            "bomb": {"sound": pg.mixer.Sound("assets/sfx/bomb.ogg"), "volume": 0.1},
            "score_up": {"sound": pg.mixer.Sound("assets/sfx/score_up.ogg"), "volume": 0.1},
            "slow": {"sound": pg.mixer.Sound("assets/sfx/slow.ogg"), "volume": 0.05},
            "temp_alert": {"sound": pg.mixer.Sound("assets/sfx/temp_alert.ogg"), "volume": 0.05},
        }
        self.music = {
            "bg": pg.mixer.music.load("assets/music/moonlight_sonata.ogg"),
        }
        for sfx_data in self.sfx.values():
            sfx_data["sound"].set_volume(sfx_data["volume"])

    def create_random_fallers(self):
        imgs = []
        for _ in range(10):
            img = pg.image.load("assets/images/falling_thing.png").convert_alpha()
            rotation = random.choice([0, 90, 180, 270])
            img = pg.transform.rotate(img, rotation)
            imgs.append(img)

        return imgs
