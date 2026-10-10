import config
import pygame

class DebugRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.enabled = False
        self.show_targets = False
        self.to_enemy = False
        self.scale = 1
        self.offset = pygame.Vector2(0, 0)
        self.camera = pygame.Vector2(0, 0)
        self.render_size = pygame.Vector2(0, 0)

    def set_camera(self, camera_rect, scale=1, offset=(0, 0), render_size=(0, 0)):
        self.camera.update(camera_rect.x, camera_rect.y)
        self.scale = scale
        self.offset.update(offset)
        self.render_size.update(render_size)

    def world_to_screen(self, pos):
        pos = pygame.Vector2(pos) - self.camera
        return pos * self.scale + self.offset

    def draw(self, key, color, *args, **kwargs):
        if not self.enabled:
            return

        draw_func = config.DRAW[key]
        return draw_func(self.screen, color, *args, **kwargs)

    def hitbox(self, subject):
        world_rect = subject.get_hitbox()

        pos = self.world_to_screen(world_rect.topleft)

        return pygame.Rect(
            round(pos.x),
            round(pos.y),
            round(world_rect.width * self.scale),
            round(world_rect.height * self.scale)
        )

    def center(self, subject):
        return self.hitbox(subject).center

    def grid(self, tile_size, color='gray', width=1):
        tile = tile_size * self.scale

        left = self.offset.x
        top = self.offset.y
        right = left + self.render_size.x
        bottom = top + self.render_size.y

        offset_x = (-self.camera.x * self.scale) % tile
        offset_y = (-self.camera.y * self.scale) % tile

        x = left + offset_x
        while x <= right:
            self.draw(
                'line',
                color,
                (x, top),
                (x, bottom),
                width=width
            )
            x += tile

        y = top + offset_y
        while y <= bottom:
            self.draw(
                'line',
                color,
                (left, y),
                (right, y),
                width=width
            )
            y += tile

    def mega_draw(self, *units, line_from=None, world=False):
        for index, unit in enumerate(units):

            rect_color = 'green' if index == 0 else 'red'
            center_color = 'blue' if index == 0 else 'yellow'

            self.draw(
                'rect',
                rect_color,
                self.hitbox(unit),
                width=2
            )

            self.draw(
                'circle',
                center_color,
                self.center(unit),
                radius=5
            )

            if line_from is not None and self.to_enemy:
                self.draw(
                    'line',
                    'white',
                    self.center(line_from),
                    self.center(unit),
                    width=3
                )

        if world:
            self.grid(config.TILE_SIZE)

    def draw_surround_targets(self, player, enemies):
        if not self.enabled or not self.show_targets:
            return

        for enemy in enemies:
            if enemy.state != 'surround':
                continue

            if enemy.surround_slot is None:
                continue

            zone = config.ZONE.get(enemy.unit_type)

            if zone is None:
                continue

            target = enemy.get_surround_point(
                player,
                enemy.surround_slot,
                zone['x'],
                zone['y']
            )

            start = self.world_to_screen(enemy.feet())
            end = self.world_to_screen(target)

            self.draw(
                'line',
                'orange',
                start,
                end,
                width=2
            )

            self.draw(
                'circle',
                'cyan',
                end,
                radius=5
            )

    def draw_buildings(self, objects, color='red', arg='polygon'):
        for obj in objects:
            if arg == 'threshold' and obj.is_interior_obstacle:
                continue

            points = []
            func = obj.get_polygon if arg == 'polygon' else obj.get_threshold

            for point in func():
                points.append(self.world_to_screen(point))

            self.draw(
                'polygon',
                color,
                points,
                width=2
            )