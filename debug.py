import config
import pygame

class DebugRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.enabled = False
        self.show_targets = False
        self.to_enemy = False
        self.camera = pygame.Vector2(0, 0)

    def set_camera(self, camera_rect):
        self.camera.update(
            camera_rect.x,
            camera_rect.y
        )

    def world_to_screen(self, pos):
        return pygame.Vector2(pos) - self.camera

    def draw(self, key, color, *args, **kwargs):
        if not self.enabled:
            return

        draw_func = config.DRAW[key]
        return draw_func(self.screen, color, *args, **kwargs)

    def hitbox(self, subject):
        rect = subject.get_hitbox().copy()

        rect.x -= round(self.camera.x)
        rect.y -= round(self.camera.y)

        return rect

    def center(self, subject):
        return self.hitbox(subject).center

    def grid(self, tile_size, color='gray', width=1):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        offset_x = -int(self.camera.x) % tile_size
        offset_y = -int(self.camera.y) % tile_size

        # вертикальные линии
        for x in range(offset_x, screen_width, tile_size):
            self.draw(
                'line',
                color,
                (x, 0),
                (x, screen_height),
                width=width
            )

        # горизонтальные линии
        for y in range(offset_y, screen_height, tile_size):
            self.draw(
                'line',
                color,
                (0, y),
                (screen_width, y),
                width=width
            )

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
            func = obj.get_polygon if arg == 'polygon' else obj.get_threshold
            self.draw(
                'polygon',
                color,
                func(),
                width=2
            )