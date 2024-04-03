import pygame as pg
import zengl

import sys
import struct
import asyncio

from src.game import Game
from src.assets_mgr import Assets
from src.splash_screens import Intro, GameOver, Startup
from src.shader_pipeline import ShaderPipeline


class App:
    def __init__(self):
        self.screen_size = 1200, 800
        self.screen = self.init_screen()
        self.init_pg()
        self.ctx = zengl.context()
        self.assets = Assets(self)        
        self.bg_shader, self.alert_shader, self.screen_shader = self.create_shaders()
        self.clock = pg.time.Clock()
        self.startup = Startup(self)
        self.intro = Intro(self)
        self.game = Game(self)
        self.game_over = GameOver(self)
        self.state = "startup"
        self.mute = False
        self.initialized = False
        self.running = True

    async def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000.0
            self.elapsed_time = pg.time.get_ticks() / 1000.0
            for event in pg.event.get():
                self.handle_events(event)
            self.mouse_pos = pg.mouse.get_pos()
            self.manage_states()
            self.render()
            await asyncio.sleep(0)
    
    def init_pg(self):
        pg.mouse.set_visible(False)
        pg.mouse.set_relative_mode(True)
        pg.font.init()
        pg.mixer.init()
        pg.display.set_caption("Atomic Convection")

    def init_screen(self):
        display_kwargs = {
            "size": self.screen_size, 
            "flags": pg.OPENGL, 
            "vsync": True
        }
        try:
            return pg.display.set_mode(**display_kwargs).convert_alpha()
        except:
            del display_kwargs["vsync"]
            return pg.display.set_mode(**display_kwargs).convert_alpha()
        
    def quit(self):
        self.running = False
        pg.mouse.set_visible(True)
        pg.mouse.set_relative_mode(False)
        pg.quit()
        sys.exit() 

    def set_mute(self):
        self.mute = not self.mute
        if self.mute:
            pg.mixer.music.pause()
            for sfx in self.assets.sfx.values():
                sfx["sound"].set_volume(0)
        else:
            pg.mixer.music.unpause()
            for sfx in self.assets.sfx.values():
                sfx["sound"].set_volume(sfx["volume"])

    def handle_events(self, event: pg.Event):
        any_input = event.type == pg.MOUSEBUTTONDOWN or event.type == pg.KEYDOWN
        
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
            self.quit()

        elif any_input and not self.initialized:
            pg.mixer.music.play(-1)
            self.initialized = True
            self.state = "intro"

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_m:
                self.set_mute()
            if event.key == pg.K_SPACE:
                if self.state == "startup":
                    self.state = "intro"
                elif self.state == "intro":
                    self.state = "game"
                elif self.state == "game_over":
                    self.state = "intro"     

    def manage_states(self):
        if self.state == "startup":
            self.startup.run()
        elif self.state == "intro":
            self.game.reset()
            self.intro.run()
        elif self.state == "game" and self.game.lives >= 0:
            self.game.run()
        elif self.state == "game" and self.game.lives < 0:
            self.state = "game_over"

        if self.state == "game_over":
            self.last_score = self.game.score
            self.last_level = self.game.level
            self.game_over.run()

    def render(self):
        self.ctx.new_frame()
        self.bg_shader.render()
        if self.state == "game":
            self.alert_shader.render()
        self.screen_shader.render(self.screen)
        self.ctx.end_frame() 
        pg.display.flip()

    def create_shaders(self):
        uniforms_map={
            "iTempMode": {
                "value": lambda: struct.pack("f", self.game.curr_temp_mode.value), 
                "glsl_type": "float"
            },
            "iTempValue": {
                "value": lambda: struct.pack("f", self.game.temp_bar.fill), 
                "glsl_type": "float"
            },
            "iTime": {
                "value": lambda: struct.pack("f", self.elapsed_time),
                "glsl_type": "float"
            },
        }
        bg_shader = ShaderPipeline(
            self, 
            uniforms_map=uniforms_map,
            frag_shader_id="background", 
            has_tex=False
        )
        alert_shader = ShaderPipeline(
            self, 
            uniforms_map=uniforms_map,
            frag_shader_id="alert_effects", 
            has_tex=False
        )        
        screen_shader = ShaderPipeline(self, uniforms_map=uniforms_map)

        return bg_shader, alert_shader, screen_shader