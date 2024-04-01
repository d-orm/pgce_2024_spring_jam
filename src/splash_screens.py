from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from src.app import App


class Intro:
    def __init__(self, app: "App"):
        self.app = app
        title_img = self.app.assets.images["title"]
        self.title_img = pg.transform.smoothscale(title_img, (title_img.get_width() // 2, title_img.get_height() // 2))
        icon = self.app.assets.images["player"]
        self.icon = pg.transform.smoothscale(icon, (icon.get_width() // 4, icon.get_height() // 4))
        pg_logo = self.app.assets.images["pygame_logo"]
        self.pg_logo = pg.transform.smoothscale(pg_logo, (pg_logo.get_width() // 16, pg_logo.get_height() // 16))
        zengl_logo = self.app.assets.images["zengl_logo"]
        self.zengl_logo = pg.transform.smoothscale(zengl_logo, (zengl_logo.get_width() // 16, zengl_logo.get_height() // 16))

    def run(self):
        self.app.screen.fill((0, 0, 0, 0))
        self.draw_icon()
        self.draw_title()
        self.draw_instructions()
        self.draw_logos()

    def draw_icon(self):
        icon_rect = self.icon.get_rect()
        icon_rect.x = self.app.screen.get_width() // 2 - self.icon.get_width() // 2
        icon_rect.y = self.app.screen.get_height() // 3 - 40
        self.app.screen.blit(self.icon, icon_rect)

    def draw_title(self):
        title_rect = self.title_img.get_rect()
        title_rect.x = self.app.screen.get_width() // 2 - self.title_img.get_width() // 2
        title_rect.y = self.app.screen.get_height() // 4 - self.icon.get_height() // 2 - 40
        self.app.screen.blit(self.title_img, title_rect)

    def draw_instructions(self):
        text = self.app.assets.fonts["roboto_mono"].render("Move the mouse to avoid falling elements & collect power-ups", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.app.screen.get_rect().center)
        self.app.screen.blit(text, text_rect)

        text2 = self.app.assets.fonts["roboto_mono"].render("Don't move too much or too little, or risk overheat or freeze!", True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(text_rect.centerx, text_rect.centery + 60))
        self.app.screen.blit(text2, text2_rect)

        text3 = self.app.assets.fonts["roboto_mono"].render("The atmospheric temperature will effect the heating/cooling rate", True, (255, 255, 255))
        text3_rect = text3.get_rect(center=(text_rect.centerx, text_rect.centery + 120))
        self.app.screen.blit(text3, text3_rect)

        text4 = self.app.assets.fonts["roboto_mono"].render("Press [SPACE] to start", True, (255, 255, 255))
        text4_rect = text4.get_rect(center=(text_rect.centerx, text_rect.centery + 240))
        self.app.screen.blit(text4, text4_rect)

        text5 = self.app.assets.fonts["roboto_mono"].render("Press [M] to toggle mute", True, (255, 255, 255))
        text5_rect = text5.get_rect(center=(text_rect.centerx, text_rect.centery + 340))
        self.app.screen.blit(text5, text5_rect)

    def draw_logos(self):
        pg_logo_rect = self.pg_logo.get_rect(topleft=(self.app.screen.get_width() - 200, self.app.screen.get_height() - self.pg_logo.get_height() - 12))
        self.app.screen.blit(self.pg_logo, pg_logo_rect)
        zengl_logo_rect = self.zengl_logo.get_rect(topleft=(pg_logo_rect.right + 10, self.app.screen.get_height() - self.zengl_logo.get_height() - 10))
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
        text = self.app.assets.fonts["roboto_mono"].render(f"Game Over!", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.app.screen.get_rect().center)
        self.app.screen.blit(text, text_rect)

        text2 = self.app.assets.fonts["roboto_mono"].render(f"Level Reached: {self.app.last_level}", True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(text_rect.centerx, text_rect.centery + 60))
        self.app.screen.blit(text2, text2_rect)

        text3 = self.app.assets.fonts["roboto_mono"].render(f"Score: {self.app.last_score}", True, (255, 255, 255))
        text3_rect = text3.get_rect(center=(text_rect.centerx, text_rect.centery + 120))
        self.app.screen.blit(text3, text3_rect)

        text4 = self.app.assets.fonts["roboto_mono"].render("Press [SPACE] to restart", True, (255, 255, 255))
        text4_rect = text4.get_rect(center=(text_rect.centerx, text_rect.centery + 240))
        self.app.screen.blit(text4, text4_rect)
