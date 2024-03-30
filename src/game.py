from typing import TYPE_CHECKING
import math
import random

import pygame as pg

from src.entities import Cursor, FallingThing, PowerUp, TemperatureBar
from src.level_data import LevelData, PowerUpTypes, TempModes

if TYPE_CHECKING:
    from src.app import App


class Game:
    def __init__(self, app: "App"):
        self.app = app
        self.temp_bar = self.create_temp_bar() 
        self.all_sprites = pg.sprite.Group()
        self.fallers_group = pg.sprite.Group()
        self.power_ups_group = pg.sprite.Group()
        self.temp_modes = [TempModes.COLD, TempModes.NORMAL, TempModes.HOT]
        self.level_inc_freq = 30
        self.depletion_rates = {
            TempModes.COLD: 7.0,
            TempModes.NORMAL: 5.0,
            TempModes.HOT: 3.0
        }
        self.fill_rates = {
            TempModes.COLD: 0.01,
            TempModes.NORMAL: 0.02,
            TempModes.HOT: 0.05
        }
        self.faller_colors = [(255, 255, 255), (255, 255, 0), (0, 255, 0), (0, 0, 255)]
        self.reset()

    def create_temp_bar(self):
        temp_bar_x = (self.app.screen_size[0] - self.app.screen_size[0] // 2) // 2
        temp_bar_y = self.app.screen_size[1] // 16
        temp_bar_w = self.app.screen_size[0] // 2
        temp_bar_h = self.app.screen_size[1] // 10
        image = self.app.assets.images["thermometer"]
        return TemperatureBar((temp_bar_x, temp_bar_y), (temp_bar_w, temp_bar_h), image) 

    def increment_level(self):
        if self.time_elapsed - self.last_level_up_time >= self.level_inc_freq:
            if self.level < LevelData.MAX_LEVEL:
                self.level += 1
                self.set_level_metrics()
            self.last_level_up_time = self.time_elapsed

    def update(self, dt):
        self.increment_level()
        self.increment_timers(dt)
        self.spawn_fallers()
        self.spawn_power_ups()
        self.all_sprites.update(dt)
        self.temp_bar.update(dt)
        self.cursor_collision_logic()
        self.temp_mode_logic()
        self.temp_bar_logic()

    def increment_timers(self, dt):
        current_time = pg.time.get_ticks()
        self.time_elapsed = (current_time - self.game_start_time) / 1000.0
        self.score = int(self.time_elapsed) * 15
        self.time_since_last_move += dt
        self.time_since_last_faller += dt
        self.time_since_last_temp_change += dt
        self.time_since_last_power_up += dt

    def draw(self, screen: pg.Surface):
        screen.fill((0, 0, 0, 0))
        self.all_sprites.draw(screen)
        self.temp_bar.draw(screen)
        self.draw_hud_text(screen)

    def draw_hud_text(self, screen: pg.Surface):
        level_text = self.app.font.render(f"Level: {self.level}", True, (255, 255, 255))
        score_text = self.app.font.render(f"Score: {self.score:.0f}", True, (255, 255, 255))
        lives_text = self.app.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(level_text, (10, 10))
        screen.blit(score_text, (10, 40))
        screen.blit(lives_text, (10, 70))

    def run(self):
        self.update(self.app.dt)
        self.draw(self.app.screen)

    def temp_mode_logic(self):
        if self.time_since_last_temp_change >= self.temp_change_freq:
            self.curr_temp_mode = random.choice([temp for temp in self.temp_modes if temp != self.curr_temp_mode])
            print(f"{self.time_elapsed} Temp mode changed to {self.curr_temp_mode}")
            self.temp_bar.depletion_rate = self.depletion_rates[self.curr_temp_mode]
            self.temp_bar.fill_rate = self.fill_rates[self.curr_temp_mode]
            self.time_since_last_temp_change = 0

    def temp_bar_logic(self):
        if self.time_since_last_move >= 0.01:
            x_dist = self.app.mouse_pos[0] - self.last_mouse_pos[0]
            y_dist = self.app.mouse_pos[1] - self.last_mouse_pos[1]
            self.temp_bar.distance_moved = math.sqrt(x_dist ** 2 + y_dist ** 2)
            self.last_mouse_pos = self.app.mouse_pos
            self.time_since_last_move = 0
        else:
            self.temp_bar.distance_moved = 0

        if self.temp_bar.fill > self.temp_bar.max_fill:
            print("Overheated!")
            self.temp_bar.fill = 50
            self.lives -= 1
            self.app.assets.sfx["lose_life"]["sound"].play()

        if self.temp_bar.fill < 0:
            print("Frozen!")
            self.temp_bar.fill = 50
            self.lives -= 1
            self.app.assets.sfx["lose_life"]["sound"].play()

        if self.temp_bar.fill < 20 or self.temp_bar.fill > 80:
            if not self.temp_alert_played:
                self.app.assets.sfx["temp_alert"]["sound"].play()
                self.temp_alert_played = True
        else:
            self.temp_alert_played = False

    def cursor_collision_logic(self):
        if pg.sprite.spritecollide(self.cursor, self.fallers_group, True):
            print("Hit!")
            self.lives -= 1
            self.app.assets.sfx["lose_life"]["sound"].play()
        if power_up := pg.sprite.spritecollide(self.cursor, self.power_ups_group, True):
            print(power_up[0].effect)
            self.power_up_callbacks(power_up[0].effect)

    def spawn_power_ups(self):
        if self.time_since_last_power_up >= self.power_up_spawn_rate:
            min_x = self.app.screen_size[0] // 3
            max_x = self.app.screen_size[0] // 3 + self.app.screen_size[0] // 3
            x_pos = random.randint(min_x, max_x)
            w = 20
            h = 20
            speed = 100
            color = (0, 0, 0)
            image = pg.Surface((w, h), pg.SRCALPHA)
            image.fill(color)
            effect = random.choice(list(PowerUpTypes.__members__.values()))
            PowerUp(
                [self.all_sprites, self.power_ups_group], 
                (x_pos, h*2), 
                speed, 
                image,
                self.app.screen_size[1],
                effect,
            )
            self.time_since_last_power_up = 0
    
    def power_up_callbacks(self, effect: PowerUpTypes):
        def extra_life():
            self.app.assets.sfx["gain_life"]["sound"].play()
            self.lives += 1

        def slow_fallers():
            self.app.assets.sfx["slow"]["sound"].play()
            for faller in self.fallers_group:
                faller.speed /= 2
                faller.sideways_motion = False
            self.time_since_last_faller = -5
        
        def extra_score():
            self.app.assets.sfx["score_up"]["sound"].play()
            self.score += 500

        def bomb():
            self.app.assets.sfx["bomb"]["sound"].play()
            for faller in self.fallers_group:
                faller.kill()
                self.all_sprites.remove(faller)

        callbacks = {
            PowerUpTypes.EXTRA_LIFE: extra_life,
            PowerUpTypes.SLOW: slow_fallers,
            PowerUpTypes.SCORE: extra_score,
            PowerUpTypes.BOMB: bomb,
        }

        return callbacks[effect]()

    def spawn_fallers(self):
        if self.time_since_last_faller >= self.faller_spawn_rate:
            x_pos = random.randint(0, self.app.screen_size[0])
            w = random.randint(self.min_faller_size, self.max_faller_size)
            h = random.randint(self.min_faller_size, self.max_faller_size)
            speed = random.randint(self.min_faller_speed, self.max_faller_speed)
            image = random.choice(self.app.assets.images["falling_things"])
            image = pg.transform.smoothscale(image, (w, h))
            FallingThing(
                [self.all_sprites, self.fallers_group], 
                (x_pos, h*2), 
                speed, 
                image,
                self.app.screen_size[1]
            )
            self.time_since_last_faller = 0
            
    def reset(self):
        self.time_elapsed = 0
        self.last_level_up_time = 0
        self.game_start_time = pg.time.get_ticks() 
        self.level = 1
        self.score = 0
        self.lives = 3
        self.temp_bar.fill = 50
        self.time_since_last_move = 0
        self.time_since_last_faller = 0
        self.time_since_last_temp_change = 0
        self.time_since_last_power_up = 0
        self.set_level_metrics()
        self.curr_temp_mode = TempModes.NORMAL
        self.all_sprites.empty()
        self.fallers_group.empty() 
        self.power_ups_group.empty() 
        self.cursor = Cursor([self.all_sprites], (30, 30), self.app.assets.images["player"])
        pg.mouse.set_pos((self.app.screen_size[0]//2, self.app.screen_size[1]//2))
        self.last_mouse_pos = self.app.screen_size[0] // 2, self.app.screen_size[1] // 2
        self.temp_alert_played = False

    def set_level_metrics(self):
        self.power_up_spawn_rate = LevelData.POWER_UP_SPAWN_RATE[f"Level_{self.level}"]
        self.temp_change_freq = LevelData.TEMP_CHANGE_FREQ[f"Level_{self.level}"]
        self.faller_spawn_rate = LevelData.FALLER_SPAWN_RATE[f"Level_{self.level}"]
        self.min_faller_size = LevelData.MIN_FALLER_SIZE[f"Level_{self.level}"]
        self.max_faller_size = LevelData.MAX_FALLER_SIZE[f"Level_{self.level}"]
        self.min_faller_speed = LevelData.MIN_FALLER_SPEED[f"Level_{self.level}"]
        self.max_faller_speed = LevelData.MAX_FALLER_SPEED[f"Level_{self.level}"]