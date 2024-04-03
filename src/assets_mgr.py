from typing import TYPE_CHECKING
import random

import pygame as pg

if TYPE_CHECKING:
    from src.app import App


class Assets:
    def __init__(self, app: "App"):
        self.app = app
        self.fonts = {
            "roboto_mono": pg.font.Font("assets/fonts/RobotoMono-Bold.ttf", 24),
        }    

        self.images: dict[str, pg.Surface] = {
            "title": pg.image.load("assets/images/title.png").convert_alpha(),
            "thermometer": pg.image.load("assets/images/thermometer.png").convert_alpha(),
            "player": pg.image.load("assets/images/player.png").convert_alpha(),
            "power_up": pg.image.load("assets/images/power_up.png").convert_alpha(),
            "lose_life": self.create_info_text("-1 Life", (255, 0, 0)),
            "score": self.create_info_text("+250 Score", (255, 255, 255)),
            "extra_life": self.create_info_text("+1 Life", (0, 255, 0)),
            "freeze": self.create_info_text("Freeze!", (150, 200, 255)),
            "bomb": self.create_info_text("Explosion!", (255, 255, 0)),
            "too_hot": self.create_info_text("Overheating, slow down!", (200, 0, 0)),
            "too_cold": self.create_info_text("Overcooling, move around!", (0, 255, 255)),
            "atmo_hot": self.create_info_text("ATMOSPHERIC TEMPERATURE: HIGH", (150, 0, 0)),
            "atmo_cold": self.create_info_text("ATMOSPHERIC TEMPERATURE: LOW", (0, 150, 150)),
            "atmo_normal": self.create_info_text("ATMOSPHERIC TEMPERATURE: MEDIUM", (0, 125, 0)),
            "falling_things": self.create_random_fallers(),
            "pygame_logo": pg.image.load("assets/images/pygame_logo.png").convert_alpha(),
            "zengl_logo": pg.image.load("assets/images/zengl_logo.png").convert_alpha(),
        }
        self.sfx: dict[str, dict[str, pg.mixer.Sound | float]] = {
            "gain_life": {"sound": pg.mixer.Sound("assets/sfx/gain_life.ogg"), "volume": 0.1},
            "lose_life": {"sound": pg.mixer.Sound("assets/sfx/lose_life.ogg"), "volume": 0.1},
            "bomb": {"sound": pg.mixer.Sound("assets/sfx/bomb.ogg"), "volume": 0.1},
            "score_up": {"sound": pg.mixer.Sound("assets/sfx/score_up.ogg"), "volume": 0.1},
            "slow": {"sound": pg.mixer.Sound("assets/sfx/slow.ogg"), "volume": 0.05},
            "temp_alert": {"sound": pg.mixer.Sound("assets/sfx/temp_alert.ogg"), "volume": 0.05},
            "temp_change": {"sound": pg.mixer.Sound("assets/sfx/temp_change.ogg"), "volume": 0.025},
        }

        for sfx_data in self.sfx.values():
            sfx_data["sound"].set_volume(sfx_data["volume"])

        pg.mixer.music.load("assets/music/moonlight_sonata.ogg")
    
    def create_random_fallers(self) -> list[pg.Surface]:
        imgs = []
        rots = [random.randint(0, 360) for _ in range(20)]
        for _ in range(len(rots)):
            img = pg.image.load("assets/images/falling_thing.png").convert_alpha()
            rotation = random.choice(rots)
            img = pg.transform.rotate(img, rotation)
            imgs.append(img)

        return imgs
    
    def create_info_text(self, text: str, color: tuple[int]) -> pg.Surface:
        return self.fonts["roboto_mono"].render(text, True, color).convert_alpha()
