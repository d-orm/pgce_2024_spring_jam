from enum import Enum, StrEnum, auto


class TempModes(Enum):
    COLD = auto()
    NORMAL = auto()
    HOT = auto()
    INTRO = auto()


class PowerUpTypes(StrEnum):
    FREEZE = auto()
    BOMB = auto()
    EXTRA_LIFE = auto()
    SCORE = auto()


class LevelData:
    MAX_LEVEL = 10 
    POWER_UP_SPAWN_RATE = {
        "Level_1": 15, 
        "Level_2": 12, 
        "Level_3": 10, 
        "Level_4": 8, 
        "Level_5": 6, 
        "Level_6": 5, 
        "Level_7": 5, 
        "Level_8": 5, 
        "Level_9": 5, 
        "Level_10": 5
    }
    TEMP_CHANGE_FREQ = {
        "Level_1": 15, 
        "Level_2": 12, 
        "Level_3": 10, 
        "Level_4": 8, 
        "Level_5": 6, 
        "Level_6": 5, 
        "Level_7": 5, 
        "Level_8": 5, 
        "Level_9": 5, 
        "Level_10": 5
    }
    FALLER_SPAWN_RATE = {
        "Level_1": 0.3, 
        "Level_2": 0.2, 
        "Level_3": 0.1, 
        "Level_4": 0.05, 
        "Level_5": 0.04, 
        "Level_6": 0.03, 
        "Level_7": 0.025, 
        "Level_8": 0.0225, 
        "Level_9": 0.02, 
        "Level_10": 0.0175
    }
    MIN_FALLER_SIZE = {
        "Level_1": 20, 
        "Level_2": 21, 
        "Level_3": 22, 
        "Level_4": 23, 
        "Level_5": 24, 
        "Level_6": 25, 
        "Level_7": 26, 
        "Level_8": 27, 
        "Level_9": 28, 
        "Level_10": 29
    }
    MAX_FALLER_SIZE = {
        "Level_1": 30, 
        "Level_2": 31, 
        "Level_3": 32, 
        "Level_4": 33, 
        "Level_5": 34, 
        "Level_6": 35, 
        "Level_7": 36, 
        "Level_8": 37, 
        "Level_9": 38, 
        "Level_10": 39
    }
    MIN_FALLER_SPEED = {
        "Level_1": 80, 
        "Level_2": 100, 
        "Level_3": 120, 
        "Level_4": 140, 
        "Level_5": 160, 
        "Level_6": 180, 
        "Level_7": 200, 
        "Level_8": 220, 
        "Level_9": 240, 
        "Level_10": 260
    }
    MAX_FALLER_SPEED = {
        "Level_1": 200, 
        "Level_2": 220, 
        "Level_3": 240, 
        "Level_4": 260, 
        "Level_5": 280, 
        "Level_6": 300, 
        "Level_7": 320, 
        "Level_8": 330, 
        "Level_9": 340, 
        "Level_10": 350
    }
