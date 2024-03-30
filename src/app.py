import pygame as pg
import zengl

import sys
import struct
import asyncio

from src.game import Game
from src.assets_mgr import Assets
from src.splash_screens import Intro, GameOver
from src.shader_pipeline import ShaderPipeline


class App:
    def __init__(self):
        self.screen_size = 1200, 800
        self.screen = pg.display.set_mode(self.screen_size, pg.OPENGL | pg.DOUBLEBUF, vsync=True).convert_alpha()
        pg.mouse.set_visible(False)
        pg.mouse.set_relative_mode(True)
        pg.font.init()
        pg.mixer.init()
        pg.display.set_caption("Temperature Game")
        self.assets = Assets(self)        
        self.ctx = zengl.context()
        uniforms_map={
            "iTempMode": {"value": lambda: struct.pack("f", self.game.curr_temp_mode.value), "glsl_type": "float"},
            "iTempValue": {"value": lambda: struct.pack("f", self.game.temp_bar.fill), "glsl_type": "float"},
            "iTime": {"value": lambda: struct.pack("f", self.elapsed_time), "glsl_type": "float"},
        }
        self.bg_shader = ShaderPipeline(
            self, 
            uniforms_map=uniforms_map,
            frag_shader_id="background", 
            has_tex=False
        )
        self.alert_effects_shader = ShaderPipeline(
            self, 
            uniforms_map=uniforms_map,
            frag_shader_id="alert_effects", 
            has_tex=False
        )        
        self.screen_shader = ShaderPipeline(self, uniforms_map=uniforms_map)
        self.clock = pg.time.Clock()

        self.font = pg.font.Font(None, 24)
        self.intro = Intro(self)
        self.game = Game(self)
        self.game_over = GameOver(self)
        self.state = "intro"

    async def run(self):
        pg.mixer.music.play(-1)
        while True:
            self.dt = self.clock.tick(60) / 1000.0
            self.elapsed_time = pg.time.get_ticks() / 1000.0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit() 

            self.keys = pg.key.get_pressed()
            self.mouse_pos = pg.mouse.get_pos()

            if self.keys[pg.K_ESCAPE]:
                pg.quit()
                sys.exit()

            elif self.keys[pg.K_SPACE] and self.state == "intro":
                self.state = "game"
            elif self.keys[pg.K_SPACE] and self.state == "game_over":
                self.game.reset()
                self.state = "game"

            if self.state == "intro":
                self.intro.run()
            elif self.state == "game" and self.game.lives >= 0:
                self.game.run()
            elif self.state == "game" and self.game.lives < 0:
                self.state = "game_over"
            elif self.state == "game_over":
                self.last_score = self.game.score
                self.last_level = self.game.level
                self.game_over.run()

           
            self.ctx.new_frame()
            self.bg_shader.render()
            self.alert_effects_shader.render()
            self.screen_shader.render(self.screen)
            self.ctx.end_frame() 

            # pg.display.set_caption(f"Temperature Game - FPS: {self.clock.get_fps():.2f}")
            pg.display.flip()
            await asyncio.sleep(0)
