from typing import TYPE_CHECKING
import math
import random
import time

import pygame as pg

from src.entities import Cursor, InfoText, FallingThing, PowerUp, TemperatureBar
from src.level_data import LevelData, PowerUpTypes, TempModes

if TYPE_CHECKING:
    from src.app import App


class Game:
    def __init__(self, app: "App"):
        self.app = app
        self.temp_bar = self.create_temp_bar() 
        self.all_sprites = pg.sprite.Group()
        self.fallers_group: pg.sprite.Group["FallingThing"] = pg.sprite.Group()
        self.power_ups_group: pg.sprite.Group["PowerUp"] = pg.sprite.Group()
        self.temp_modes = [TempModes.COLD, TempModes.NORMAL, TempModes.HOT]
        self.curr_temp_mode = TempModes.INTRO
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
        self.reset()

    def create_temp_bar(self):
        x = (self.app.screen_size[0] - self.app.screen_size[0] // 3) // 2
        y = self.app.screen_size[1] // 16
        w = self.app.screen_size[0] // 3
        h = self.app.screen_size[1] // 8
        image = self.app.assets.images["thermometer"]
        return TemperatureBar((x, y), (w, h), image) 

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
        self.cycle_temp_mode()
        self.temp_bar_logic()

    def increment_timers(self, dt):
        current_time = pg.time.get_ticks()
        self.time_elapsed = (current_time - self.game_start_time) / 1000.0
        self.score = (int(self.time_elapsed) * 15) + self.power_ups_score
        self.time_since_last_move += dt
        self.time_since_last_faller += dt
        self.time_since_last_temp_change += dt
        self.time_since_last_power_up += dt

    def draw(self, screen: pg.Surface):
        screen.fill((0, 0, 0, 0))
        for spr in self.all_sprites:
            spr.draw(screen)
        self.temp_bar.draw(screen)
        self.draw_hud_text(screen)

    def draw_hud_text(self, screen: pg.Surface):
        font = self.app.assets.fonts["roboto_mono"]
        max_lvl = "(max)" if self.level == LevelData.MAX_LEVEL else ""
        level_text = font.render(f"Level: {self.level}{max_lvl}", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.score:.0f}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(level_text, (10, 10))
        screen.blit(score_text, (10, 40))
        screen.blit(lives_text, (10, 70))

        atmo_text = self.app.assets.images[f"atmo_{self.curr_temp_mode.name.lower()}"]
        x_pos = self.app.screen_size[0] // 2 - atmo_text.get_width() // 2
        y_pos = self.app.screen_size[1] - atmo_text.get_height() * 2
        screen.blit(atmo_text, (x_pos, y_pos))

    def run(self):
        self.update(self.app.dt)
        self.draw(self.app.screen)

    def cycle_temp_mode(self):
        if self.curr_temp_mode == TempModes.INTRO:
            self.curr_temp_mode = TempModes.NORMAL

        if self.time_since_last_temp_change >= self.temp_change_freq:
            self.app.assets.sfx["temp_change"]["sound"].play()
            temp_modes = [t for t in self.temp_modes if t != self.curr_temp_mode]
            self.curr_temp_mode = random.choice(temp_modes)
            self.temp_bar.depletion_rate = self.depletion_rates[self.curr_temp_mode]
            self.temp_bar.fill_rate = self.fill_rates[self.curr_temp_mode]
            self.time_since_last_temp_change = 0

    def temp_bar_logic(self):
        self.heat_up_from_mouse()
        self.lose_life_from_temp()
        self.temp_alerts()

    def heat_up_from_mouse(self):
        if self.time_since_last_move >= 0.01:
            x_dist = self.app.mouse_pos[0] - self.last_mouse_pos[0]
            y_dist = self.app.mouse_pos[1] - self.last_mouse_pos[1]
            self.temp_bar.distance_moved = math.sqrt(x_dist ** 2 + y_dist ** 2)
            self.last_mouse_pos = self.app.mouse_pos
            self.time_since_last_move = 0
        else:
            self.temp_bar.distance_moved = 0

    def lose_life_from_temp(self):
        lose_life_img = self.app.assets.images["lose_life"]
        lose_life_snd = self.app.assets.sfx["lose_life"]["sound"]
        pos = self.cursor.rect.midtop

        if self.temp_bar.fill > self.temp_bar.max_fill:
            self.temp_bar.fill = 50
            InfoText([self.all_sprites], pos, 100, 100, lose_life_img)
            self.lives -= 1
            lose_life_snd.play()

        if self.temp_bar.fill < 0:
            self.temp_bar.fill = 50
            InfoText([self.all_sprites], pos, 100, 100, lose_life_img)
            self.lives -= 1
            lose_life_snd.play()

    def temp_alerts(self):
        if self.temp_bar.fill < 20 or self.temp_bar.fill > 80:
            if not self.temp_alert_played:
                self.app.assets.sfx["temp_alert"]["sound"].play()
                if self.temp_bar.fill < 20: 
                    img = self.app.assets.images["too_cold"]
                else:
                    img = self.app.assets.images["too_hot"]
                InfoText([self.all_sprites], self.cursor.rect.midtop, 300, 75, img)
                self.temp_alert_played = True
        else:
            self.temp_alert_played = False

    def cursor_collision_logic(self):
        pos = self.cursor.rect.midtop
        if pg.sprite.spritecollide(self.cursor, self.fallers_group, True):
            lose_life_img = self.app.assets.images["lose_life"]
            InfoText([self.all_sprites], pos, 100, 100, lose_life_img)
            self.lives -= 1
            self.app.assets.sfx["lose_life"]["sound"].play()
        if power_up := pg.sprite.spritecollide(self.cursor, self.power_ups_group, True):
            effect = power_up[0].effect
            pu_img = self.app.assets.images[effect]
            InfoText([self.all_sprites], pos, 100, 100, pu_img)
            self.power_up_callbacks(effect)

    def spawn_power_ups(self):
        if self.time_since_last_power_up >= self.power_up_spawn_rate:
            min_x = self.app.screen_size[0] // 3
            max_x = (self.app.screen_size[0] // 3) * 2
            x_pos = random.randint(min_x, max_x)
            w, h = 30, 30
            speed = 100
            image = self.app.assets.images["power_up"]
            image = pg.transform.smoothscale(image, (w, h))
            effect = random.choice(list(PowerUpTypes.__members__.values()))
            PowerUp(
                [self.all_sprites, self.power_ups_group], 
                (x_pos, h*2), 
                speed, 
                image,
                self.app.screen_size[1],
                effect=effect,
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
            self.power_ups_score += 250

        def bomb():
            self.app.assets.sfx["bomb"]["sound"].play()
            for faller in self.fallers_group:
                faller.kill()
                self.all_sprites.remove(faller)

        callbacks = {
            PowerUpTypes.EXTRA_LIFE: extra_life,
            PowerUpTypes.FREEZE: slow_fallers,
            PowerUpTypes.SCORE: extra_score,
            PowerUpTypes.BOMB: bomb,
        }

        return callbacks[effect]()

    def spawn_fallers(self):
        if self.time_since_last_faller >= self.faller_spawn_rate:
            x_pos = random.randint(0, self.app.screen_size[0])
            size = random.randint(self.min_faller_size, self.max_faller_size)
            speed = random.randint(self.min_faller_speed, self.max_faller_speed)
            image = random.choice(self.app.assets.images["falling_things"])
            image = pg.transform.smoothscale(image, (size, size))
            FallingThing(
                [self.all_sprites, self.fallers_group], 
                (x_pos, -size*2), 
                speed, 
                image,
                self.app.screen_size[1]
            )
            self.time_since_last_faller = 0
            
    def reset(self):
        random.seed(time.time())
        self.time_elapsed = 0
        self.last_level_up_time = 0
        self.game_start_time = pg.time.get_ticks() 
        self.level = 1
        self.score = 0
        self.power_ups_score = 0
        self.lives = 3
        self.temp_bar.fill = 50
        self.time_since_last_move = 0
        self.time_since_last_faller = 0
        self.time_since_last_temp_change = 0
        self.time_since_last_power_up = 0
        self.temp_alert_played = False
        self.curr_temp_mode = TempModes.INTRO
        self.all_sprites.empty()
        self.fallers_group.empty() 
        self.power_ups_group.empty() 
        self.cursor = Cursor([self.all_sprites], (50, 50), self.app.assets.images["player"])
        pg.mouse.set_pos((self.app.screen_size[0]//2, self.app.screen_size[1]//2))
        self.last_mouse_pos = self.app.screen_size[0] // 2, self.app.screen_size[1] // 2
        self.set_level_metrics()

    def set_level_metrics(self):
        self.power_up_spawn_rate = LevelData.POWER_UP_SPAWN_RATE[f"Level_{self.level}"]
        self.temp_change_freq = LevelData.TEMP_CHANGE_FREQ[f"Level_{self.level}"]
        self.faller_spawn_rate = LevelData.FALLER_SPAWN_RATE[f"Level_{self.level}"]
        self.min_faller_size = LevelData.MIN_FALLER_SIZE[f"Level_{self.level}"]
        self.max_faller_size = LevelData.MAX_FALLER_SIZE[f"Level_{self.level}"]
        self.min_faller_speed = LevelData.MIN_FALLER_SPEED[f"Level_{self.level}"]
        self.max_faller_speed = LevelData.MAX_FALLER_SPEED[f"Level_{self.level}"]
