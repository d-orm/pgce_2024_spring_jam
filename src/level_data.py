from enum import Enum, StrEnum, auto


class TempModes(Enum):
    COLD = auto()
    NORMAL = auto()
    HOT = auto()


class PowerUpTypes(StrEnum):
    SLOW = auto()
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
        "Level_6": 4, 
        "Level_7": 3, 
        "Level_8": 2, 
        "Level_9": 1, 
        "Level_10": 0.5
    }
    TEMP_CHANGE_FREQ = {
        "Level_1": 15, 
        "Level_2": 12, 
        "Level_3": 10, 
        "Level_4": 8, 
        "Level_5": 6, 
        "Level_6": 4, 
        "Level_7": 3, 
        "Level_8": 2, 
        "Level_9": 1, 
        "Level_10": 0.5
    }
    FALLER_SPAWN_RATE = {
        "Level_1": 0.3, 
        "Level_2": 0.2, 
        "Level_3": 0.1, 
        "Level_4": 0.05, 
        "Level_5": 0.04, 
        "Level_6": 0.03, 
        "Level_7": 0.02, 
        "Level_8": 0.01, 
        "Level_9": 0.005, 
        "Level_10": 0.0025
    }
    MIN_FALLER_SIZE = {
        "Level_1": 8, 
        "Level_2": 9, 
        "Level_3": 10, 
        "Level_4": 11, 
        "Level_5": 12, 
        "Level_6": 13, 
        "Level_7": 14, 
        "Level_8": 15, 
        "Level_9": 16, 
        "Level_10": 17
    }
    MAX_FALLER_SIZE = {
        "Level_1": 20, 
        "Level_2": 22, 
        "Level_3": 24, 
        "Level_4": 26, 
        "Level_5": 26, 
        "Level_6": 28, 
        "Level_7": 30, 
        "Level_8": 32, 
        "Level_9": 34, 
        "Level_10": 36
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
        "Level_8": 340, 
        "Level_9": 360, 
        "Level_10": 380
    }
