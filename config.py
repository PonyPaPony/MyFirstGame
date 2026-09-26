import pygame


GAME_NAME = 'Maybe Later'

FPS = 60

BACKGROUND_COLOR = (0, 0, 0)

WIDTH = 1024
HEIGHT = 720
CAMERA = [0, 0, WIDTH, HEIGHT]

SCREEN_SETTINGS = {
    'Window': {
        'size': (1024, 720),
        'method': pygame.RESIZABLE
    },
    'Border': {
        'size': (0, 0),
        'method': pygame.NOFRAME
    },
    "Full Screen": {
        'size': (0, 0),
        'method': pygame.FULLSCREEN
    }
}

MOVEMENT = {
    pygame.K_w: (0, -1),  # Вверх
    pygame.K_s: (0, 1),   # Вниз
    pygame.K_a: (-1, 0),  # Влево
    pygame.K_d: (1, 0),   # Вправо
}

TILE_SIZE = 64
SPEED_POINTS_PER_TILE = 10

SURW = 100 * TILE_SIZE
SURH = 60 * TILE_SIZE

DRAW = {
    'rect': pygame.draw.rect,
    'circle': pygame.draw.circle,
    'line': pygame.draw.line,
}

ARGO = {
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

AGGRO_COOLDOWN = 15