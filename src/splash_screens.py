from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import App


class Intro:
    def __init__(self, app: "App"):
        self.app = app

    def run(self):
        self.app.screen.fill((0, 150, 0))
        text = self.app.font.render("Press SPACE to start", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.app.screen.get_rect().center)
        self.app.screen.blit(text, text_rect)


class GameOver:
    def __init__(self, app: "App"):
        self.app = app

    def run(self):
        self.app.screen.fill((150, 0, 0))
        text = self.app.font.render(f"Game Over! Level: {self.app.last_level} Score: {self.app.last_score}", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.app.screen.get_rect().center)
        self.app.screen.blit(text, text_rect)