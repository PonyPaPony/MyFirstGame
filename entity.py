import pygame
import config


class Entity:
    def __init__(self, image, x, y, stats, unit_type):
        self.image = image
        self.pos = pygame.Vector2(x, y)
        self.stats = stats
        self.unit_type = unit_type

        self.attack_timer = 0

        # Коэфициенты Хитбоксов
        self.hitbox_offset_x = 0.3
        self.hitbox_offset_y = 0.8
        self.hitbox_width = 0.4
        self.hitbox_height = 0.2

        self.spawn_pos = self.feet()

    @staticmethod
    def clamp(value, minimum, maximum):
        return max(minimum, min(value, maximum))

    def get_real_speed(self):
        stat_speed = int(self.get_stat_speed())
        return (stat_speed / config.SPEED_POINTS_PER_TILE) * config.TILE_SIZE

    def get_stat_speed(self):
        return int(min(self.stats['speed'], self.stats['speed_limit']))

    def get_image(self, horizontal=False):
        return self.image.get_width() if horizontal else self.image.get_height()

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def get_rect(self): # КВАДРАТ, КВАДРАТ, КВАДРАТ, (это рофл я знаю это прямоугольник)
        return self.image.get_rect(topleft=self.pos)

    def get_hitbox(self, pos=None): # Ну это то на что ты в CSочке жалуешься
        if pos is None:
            pos = self.pos

        width = self.image.get_width()
        height = self.image.get_height()

        return pygame.Rect(
            round(pos.x + width * self.hitbox_offset_x),
            round(pos.y + height * self.hitbox_offset_y),
            round(width * self.hitbox_width),
            round(height * self.hitbox_height),
        )

    def feet(self): # Футфетишисты вошли в зал
        return pygame.Vector2(self.get_hitbox().center)

    def get_candidate(self, pos, axis):
        if axis == 'x':
            return pygame.Vector2(pos, self.pos.y)

        elif axis == 'y':
            return pygame.Vector2(self.pos.x, pos)

        raise ValueError("axis must be 'x' or 'y'")

    def can_move(self, candidate, obstacles):
        current = self.get_hitbox()
        future = self.get_hitbox(candidate)

        for obstacle in obstacles:
            other = obstacle.get_hitbox()

            if not future.colliderect(other):
                continue

            current_overlap = current.clip(other)
            future_overlap = future.clip(other)

            current_area = (
                current_overlap.width * current_overlap.height
            )
            future_area = (
                future_overlap.width * future_overlap.height
            )

            if future_area >= current_area:
                return False

        return True

    def move(
            self,
            direction,
            dt,
            bounds,
            obstacles=(),
            speed_multiplier=1
    ):
        old_pos = self.pos.copy()

        if direction.length_squared() == 0:
            return False

        direction = direction.normalize()  # нормализуем направление, чтобы диагональ не была быстрее
        real_speed = self.get_real_speed() * speed_multiplier

        if real_speed == 0:
            return False

        delta = direction * real_speed * dt  # насколько сдвинемся за этот кадр

        new_x = self.clamp(
            self.pos.x + delta.x,
            bounds.left,
            bounds.right - self.image.get_width()
        )

        new_y = self.clamp(
            self.pos.y + delta.y,
            bounds.top,
            bounds.bottom - self.image.get_height()
        )

        candidate = self.get_candidate(new_x, 'x')  # где окажемся, если разрешим этот сдвиг

        if self.can_move(candidate, obstacles):
            self.pos.x = new_x

        candidate = self.get_candidate(new_y, 'y')

        if self.can_move(candidate, obstacles):
            self.pos.y = new_y

        return self.pos != old_pos

    def move_to(
            self,
            target_pos,
            dt,
            bounds,
            obstacles=(),
            stop_distance=5,
            speed_multiplier=1
    ):
        direction = target_pos - self.feet()
        distance = direction.length()

        if distance <= stop_distance:
            return False

        remaining = distance - stop_distance
        real_speed = self.get_real_speed() * speed_multiplier

        if real_speed == 0:
            return False

        step_dt = min(dt, remaining / real_speed)

        return self.move(
            direction,
            step_dt,
            bounds,
            obstacles=obstacles,
            speed_multiplier=speed_multiplier
        )

    def update(self, dt):
        if self.attack_timer > 0:
            self.attack_timer = max(0, self.attack_timer - dt)