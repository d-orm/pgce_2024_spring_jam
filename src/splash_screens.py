from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from src.app import App


class Startup:
    def __init__(self, app: "App"):
        self.app = app

    def run(self):
        self.app.screen.fill((0, 0, 0, 255))
        line_1 = "Press any key or click to begin..."
        text = self.app.assets.fonts["roboto_mono"].render(line_1, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.app.screen.get_rect().center)
        self.app.screen.blit(text, text_rect)


class Intro:
    def __init__(self, app: "App"):
        self.app = app
        title_img = self.app.assets.images["title"]
        title_scale = (title_img.get_width() // 2, title_img.get_height() // 2)
        self.title_img = pg.transform.smoothscale(title_img, title_scale)
        icon = self.app.assets.images["player"]
        icon_scale = (icon.get_width() // 4, icon.get_height() // 4)
        self.icon = pg.transform.smoothscale(icon, icon_scale)
        pg_logo = self.app.assets.images["pygame_logo"]
        pg_logo_scale = (pg_logo.get_width() // 16, pg_logo.get_height() // 16)
        self.pg_logo = pg.transform.smoothscale(pg_logo, pg_logo_scale)
        zengl_logo = self.app.assets.images["zengl_logo"]
        zengl_logo_scale = (zengl_logo.get_width() // 16, zengl_logo.get_height() // 16)
        self.zengl_logo = pg.transform.smoothscale(zengl_logo, zengl_logo_scale)

    def run(self):
        self.app.screen.fill((0, 0, 0, 0))
        self.draw_icon()
        self.draw_title()
        self.draw_instructions()
        self.draw_logos()

    def draw_icon(self):
        icon_rect = self.icon.get_rect()
        icon_rect.x = self.app.screen.get_width() // 2 - self.icon.get_width() // 2
        icon_rect.y = self.app.screen.get_height() // 3 - 80
        self.app.screen.blit(self.icon, icon_rect)

    def draw_title(self):
        title_rect = self.title_img.get_rect()
        title_rect.x = self.app.screen.get_width() // 2 - self.title_img.get_width() // 2
        title_rect.y = self.app.screen.get_height() // 4 - self.icon.get_height() // 2 - 80
        self.app.screen.blit(self.title_img, title_rect)

    def draw_instructions(self):
        text_border_rect = pg.Rect(0, 0, self.app.screen.get_width() // 1.25, 180)
        text_border_rect.center = self.app.screen.get_rect().center
        text_border_rect.y = self.app.screen.get_height() // 2 - 30
        pg.draw.rect(self.app.screen, (0, 0, 0, 125), text_border_rect, border_radius=50)
        pg.draw.rect(self.app.screen, (0, 0, 0, 255), text_border_rect, width=5, border_radius=50)
        
        line_1 = "Move the mouse to avoid falling elements & collect power-ups"
        text = self.app.assets.fonts["roboto_mono"].render(line_1, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.app.screen.get_rect().center)
        self.app.screen.blit(text, text_rect)

        line_2 = "Don't move too much or too little, or risk overheat or freeze!"
        text2 = self.app.assets.fonts["roboto_mono"].render(line_2, True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(text_rect.centerx, text_rect.centery + 60))
        self.app.screen.blit(text2, text2_rect)

        line_3 = "The atmospheric temperature will effect the heating/cooling rate"
        text3 = self.app.assets.fonts["roboto_mono"].render(line_3, True, (255, 255, 255))
        text3_rect = text3.get_rect(center=(text_rect.centerx, text_rect.centery + 120))
        self.app.screen.blit(text3, text3_rect)

        line_4 = "Press [SPACE] to start"
        text4 = self.app.assets.fonts["roboto_mono"].render(line_4, True, (255, 255, 255))
        text4_rect = text4.get_rect(center=(text_rect.centerx, text_rect.centery + 240))
        self.app.screen.blit(text4, text4_rect)

        line_5 = "Press [M] to toggle mute, [R] to restart, [Q] to quit"
        text5 = self.app.assets.fonts["roboto_mono"].render(line_5, True, (255, 255, 255))
        text5_rect = text5.get_rect(center=(text_rect.centerx, text_rect.centery + 340))
        self.app.screen.blit(text5, text5_rect)

    def draw_logos(self):
        pg_logo_x_pos = self.app.screen.get_width() - 200
        pg_logo_y_pos = self.app.screen.get_height() - self.pg_logo.get_height() - 12
        pg_logo_rect = self.pg_logo.get_rect(topleft=(pg_logo_x_pos, pg_logo_y_pos))
        self.app.screen.blit(self.pg_logo, pg_logo_rect)

        zgl_logo_x_pos = pg_logo_rect.right + 10
        zgl_logo_y_pos = self.app.screen.get_height() - self.zengl_logo.get_height() - 10
        zengl_logo_rect = self.zengl_logo.get_rect(topleft=(zgl_logo_x_pos, zgl_logo_y_pos))
        self.app.screen.blit(self.zengl_logo, zengl_logo_rect)


class GameOver:
    def __init__(self, app: "App"):
        self.app = app
        icon = self.app.assets.images["player"]
        self.icon = pg.transform.smoothscale(icon, (icon.get_width() // 2, icon.get_height() // 2))

    def run(self):
        self.app.screen.fill((0, 0, 0, 0))
        self.draw_icon()
        self.draw_stats()

    def draw_icon(self):
        icon_rect = self.icon.get_rect()
        icon_rect.x = self.app.screen.get_width() // 2 - self.icon.get_width() // 2
        icon_rect.y = self.app.screen.get_height() // 4 - self.icon.get_height() // 2
        self.app.screen.blit(self.icon, icon_rect)

    def draw_stats(self):
        line_1 = "Game Over!"
        text = self.app.assets.fonts["roboto_mono"].render(line_1, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.app.screen.get_rect().center)
        self.app.screen.blit(text, text_rect)

        line_2 = f"Level Reached: {self.app.last_level}"
        text2 = self.app.assets.fonts["roboto_mono"].render(line_2, True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(text_rect.centerx, text_rect.centery + 60))
        self.app.screen.blit(text2, text2_rect)

        line_3 = f"Score: {self.app.last_score}"
        text3 = self.app.assets.fonts["roboto_mono"].render(line_3, True, (255, 255, 255))
        text3_rect = text3.get_rect(center=(text_rect.centerx, text_rect.centery + 120))
        self.app.screen.blit(text3, text3_rect)

        line_4 = "Press [SPACE] to restart"
        text4 = self.app.assets.fonts["roboto_mono"].render(line_4, True, (255, 255, 255))
        text4_rect = text4.get_rect(center=(text_rect.centerx, text_rect.centery + 240))
        self.app.screen.blit(text4, text4_rect)


class Quitted:
    def __init__(self, app: "App"):
        self.app = app

    def run(self):
        self.app.screen.fill((0, 0, 0, 255))
        line_1 = "Thanks for playing!"
        text = self.app.assets.fonts["roboto_mono"].render(line_1, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.app.screen.get_rect().center)
        self.app.screen.blit(text, text_rect)