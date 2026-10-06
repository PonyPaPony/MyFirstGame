import random
import pygame
import config
from data.unit_templates import UNITS
from stats import build_stats


def resize_image(path, target_height:int=96): # 96px средний рост
    image = pygame.image.load(path).convert_alpha() # Show yourself
    rect = image.get_bounding_rect() # Who is behind you?

    if rect.width == 0 or rect.height == 0:
        raise ValueError(f"Image is Empty {path}")

    image = image.subsurface(rect).copy() # Clear image and copy for safe
    scale = target_height / image.get_height() # Coef

    nw = round(image.get_width() * scale)
    nh = round(image.get_height() * scale)

    image = pygame.transform.smoothscale(image, (nw, nh)) # we use smooth 'cause it's not pixel art

    return image


def spawn_creature(entity, name, pos, **kwargs):
    x, y = pos
    configure = UNITS[name]
    unit_type = configure['unit_type']
    image = resize_image(configure["path"], int(configure['height']))

    stats = build_stats(unit_type, kwargs)

    x = entity.clamp(x, 0, config.SURW - image.get_width())
    y = entity.clamp(y, 0, config.SURH - image.get_height())

    return entity(image, x, y, stats, unit_type)


def multi_spawn(entity, count, name, **kwargs):
    enemies = []

    while len(enemies) < count:
        candidate = spawn_creature(entity, name, (0, 0), **kwargs)

        x = random.randint(0, config.SURW - candidate.get_image(True))
        y = random.randint(0, config.SURH - candidate.get_image(False))

        candidate.pos.update(x, y)
        candidate.spawn_pos = candidate.feet()

        if not any(
            candidate.get_rect().colliderect(enemy.get_rect()) for enemy in enemies
        ):
            enemies.append(candidate)

    return enemies