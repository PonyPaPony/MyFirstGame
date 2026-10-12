import pygame


#! NOTE: Настройки игры
TILE_SIZE = 64
SPEED_POINTS_PER_TILE = 10
AGGRO_COOLDOWN = 15
COMBAT_EXIT_DELAY = 3

CALENDAR = {
    'year': 360,
    'month': 30
}
TIMES = {
    'day': 1440,
    'hour': 60
}

MARGINS = {
    'active': 0.2,
    'despawn': 0.3
}

RESPAWN_TIME = {
    'local': 180,
    'global': 1440
}

AGGRO = {
    'melee': 3 * TILE_SIZE,
    'range': 5 * TILE_SIZE,
    'mage': 5 * TILE_SIZE,
}

LEASH = {
    'melee': 5 * TILE_SIZE,
    'range': 7 * TILE_SIZE,
    'mage': 6 * TILE_SIZE
}

ZONE = {
    'melee': {
        'x': 100,
        'y': 60
    },
    'range': {
        'x': 300,
        'y': 180
    }
}

SLOTS = {
    'melee':  8,
    'range':  8,
    'mage':  8,
}


#! NOTE: Настройки экрана

GAME_NAME = 'Maybe Later'

SCREEN_SETTINGS = {
    'window': {
        'size': (1280, 720),
        'method': pygame.RESIZABLE,
        'camera': (1280, 720)
    },
    'border': {
        'size': (0, 0),
        'method': pygame.NOFRAME,
        'camera': None
    },
    'fullscreen': {
        'size': (0, 0),
        'method': pygame.FULLSCREEN,
        'camera': None
    }
}

SURFACE = (100 * TILE_SIZE, 60 * TILE_SIZE)
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)

#! NOTE: Настройки управления
MOVEMENT_KEYS = {
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0)
}

#! NOTE: Имена для косоли
#- TODO(linked): Перенести в будущем в иное место
NAMES = {
    'sword': 'goblin_swordman',
    'archer': 'goblin_archer',
}

DRAW = {
    'rect': pygame.draw.rect,
    'circle': pygame.draw.circle,
    'line': pygame.draw.line,
    'lines': pygame.draw.lines,
    'polygon': pygame.draw.polygon,
}