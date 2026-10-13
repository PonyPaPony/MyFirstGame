import pygame
import config
from combat import Combat
from data.entity_templates import UNITS, ATTACK_RANGE, STATE, LIMITS
from foo_name import resize_image
from buildings import Obstacle


class Entity:
    def __init__(self, name, image, x, y, stats, unit_type):
        self.combat = Combat()

        self.name = name
        self.image = image
        self.position = pygame.Vector2(x, y)
        self.stats = stats
        self.unit_type = unit_type

        self.attack_timer = 0

        self.hitbox = UNITS[self.name]['hitbox']
        self.spawn_pos = self.feet()

    @staticmethod
    def clamp(value, minimum, maximum):
        return max(minimum, min(value, maximum))

    def feet(self):
        return pygame.Vector2(self.get_hitbox().center)

    def get_rect(self):
        return self.image.get_rect(topleft=self.position)

    def get_hitbox(self, pos=None):
        if pos is None:
            pos = self.position

        width = self.image.get_width()
        height = self.image.get_height()

        return pygame.Rect(
            round(pos.x + width * self.hitbox['x']),
            round(pos.y + height * self.hitbox['y']),
            round(width * self.hitbox['w']),
            round(height * self.hitbox['h'])
        )

    def get_collision_circle(self, pos=None):
        hitbox = self.get_hitbox(pos)
        return pygame.Vector2(hitbox.center), 5

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def get_speed(self):
        stat_speed = int(min(self.stats['speed'], self.stats['speed_limit']))
        return (stat_speed / config.SPEED_POINTS_PER_TILE) * config.TILE_SIZE

    def get_candidate(self, pos, axis):
        if axis == 'x':
            return pygame.Vector2(pos, self.position.y)
        elif axis == 'y':
            return pygame.Vector2(self.position.x, pos)
        raise ValueError('Invalid axis')

    def collides_with(self, rect):
        return rect.colliderect(self.get_hitbox())

    def update(self, dt):
        if self.attack_timer > 0:
            self.attack_timer = max(0, self.attack_timer - dt)

    #- TODO(core): Improve circle collision sliding along angled walls
    def collision_with_obstacle(self, candidate, obstacle):
        if isinstance(obstacle, Obstacle):
            center, radius = self.get_collision_circle(candidate)
            return obstacle.collides_with_circle(center, radius)

        return False

    @staticmethod
    def collision_with_entity(current, future, obstacle):
        other = obstacle.get_hitbox()

        current_lap = current.clip(other)
        future_lab = future.clip(other)

        current_area = (current_lap.width * current_lap.height)
        future_area = (future_lab.width * future_lab.height)

        if future_area >= current_area:
            return True
        return False

    def can_move(self, candidate, obstacles):
        current = self.get_hitbox()
        future = self.get_hitbox(candidate)

        for obstacle in obstacles:
            if isinstance(obstacle, Obstacle):
                if self.collision_with_obstacle(candidate, obstacle):
                    return False
                continue

            if not obstacle.collides_with(future):
                continue

            if isinstance(obstacle, Entity):
                if self.collision_with_entity(current, future, obstacle):
                    return False
            else:
                return False
        return True

    def move(self, direction, dt, bounds, obstacles=(), speed_multiplayer=1):
        old_pos = self.position.copy()

        if direction.length_squared() == 0:
            return False #? WHY: Если стоим ничего не делаем

        direction = direction.normalize()
        speed = self.get_speed() * speed_multiplayer

        if speed == 0:
            return False #? WHY: Если скорость равна нулю, ничего не делаем

        delta = direction * speed * dt  # на сколько сдвинемся за 1 кадр

        new_x = self.clamp(
            self.position.x + delta.x,
            bounds.left,
            bounds.right - self.image.get_width()
        )
        new_y = self.clamp(
            self.position.y + delta.y,
            bounds.top,
            bounds.bottom - self.image.get_height()
        )

        candidate = self.get_candidate(new_x, 'x')

        if self.can_move(candidate, obstacles):
            self.position.x = new_x

        candidate = self.get_candidate(new_y, 'y')

        if self.can_move(candidate, obstacles):
            self.position.y = new_y

        return self.position != old_pos

    def move_to(
            self,
            target_position,
            dt,
            bounds,
            obstacles=(),
            stop_distance=5,
            speed_multiplayer=1
    ):
        direction = target_position - self.feet()
        distance = direction.length()

        if distance <= stop_distance:
            return False

        remaining = distance - stop_distance
        speed = self.get_speed() * speed_multiplayer

        if speed == 0:
            return False

        step_delta = min(dt, remaining / speed)

        return self.move(direction, step_delta, bounds, obstacles=obstacles, speed_multiplayer=speed_multiplayer)



#! NOTE: Maybe need to move
class Spawner:
    def spawn_creature(self, entity_class, name, pos, **kwargs):
        x, y = pos
        configure = UNITS[name]
        unit_type = configure['unit_type']

        image = resize_image(configure['path'], int(configure['height']))

        stats = self.build_stats(name, unit_type, kwargs)

        x = entity_class.clamp(x, 0, config.SURFACE[0] - image.get_width())
        y = entity_class.clamp(y, 0, config.SURFACE[1] - image.get_height())

        return entity_class(name, image, x, y, stats, unit_type)

    @staticmethod
    def build_stats(name, unit_type, custom_stats=None):
        if custom_stats is None:
            custom_stats = {}

        stats = {
            **UNITS[name]['stats'],
            **LIMITS,
            **STATE,
            'attack_range': ATTACK_RANGE[unit_type],
            **custom_stats,
        }

        if 'current_health' not in custom_stats:
            stats['current_health'] = stats['max_health']

        return stats