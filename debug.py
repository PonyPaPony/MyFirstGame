import pygame
import config
from buildings import Building


class DebugRenderer:
    def __init__(self, screen):
        self.screen = screen

        self.enabled = False
        self.polygon_editor = False
        self.show_polygon = False
        self.show_surround = False

        self.points = []
        self.polygons = []

        self.camera = pygame.Vector2(0, 0)
        self.scale = 1
        self.offset = pygame.Vector2(0, 0)
        self.render_size = pygame.Vector2(0, 0)

    def set_camera(self, camera, scale, offset, size):
        self.camera.update(camera.topleft)
        self.scale = scale
        self.offset.update(offset)
        self.render_size.update(size)

    def world_to_screen(self, pos):
        return (pygame.Vector2(pos) - self.camera) * self.scale + self.offset

    def draw(self, key, color, *args, **kwargs):
        if not self.enabled:
            return None

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

    def debug_draw(self, *units, line_from=None, player=None, enemies=None):
        for index, unit in enumerate(units):
            rect_color = 'green' if index == 0 else 'red'
            center_color = 'blue' if index == 0 else 'yellow'

            self.draw('rect', rect_color, self.hitbox(unit), width=2)
            self.draw('circle', center_color, self.center(unit), radius=5)

            if line_from is not None:
                self.draw('line', 'white', self.center(line_from), self.center(unit), width=3)

        if player is not None and enemies is not None:
            self.draw_surround_targets(player, enemies)

        self.grid()


    #! NOTE: Методы Отрисовки
    def grid(self, color='gray', width=1):
        tile = config.TILE_SIZE * self.scale

        left, top = self.offset.x, self.offset.y
        right, bottom = left + self.render_size.x, top + self.render_size.y

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
            x+= tile

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

    def draw_surround_targets(self, player, enemies):
        if not self.show_surround:
            return

        for enemy in enemies:
            if enemy.state != 'surround':
                continue

            if enemy.surround_slot is None:
                continue

            zone = config.ZONE.get(enemy.unit_type)

            if zone is None:
                continue

            target = enemy.get_surround_slot(player, enemy.surround_slot, zone['x'], zone['y'])
            start = self.world_to_screen(enemy.feet())
            end = self.world_to_screen(target)

            self.draw('line', 'orange', start, end, width=2)
            self.draw('circle', 'cyan', end, radius=5)

    def draw_attack_status(self, enemies, target):
        if not self.enabled:
            return

        for enemy in enemies:
            can_attack = enemy.combat.can_attack(enemy, target)

            color = 'green' if can_attack else 'red'

            center = self.center(enemy)

            self.draw(
                'circle',
                color,
                center,
                radius=12,
                width=2
            )

    #! NOTE: PolygonEditor
    def handle_event(self, event, mouse_pos):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and mouse_pos is not None:
                    point = (
                        round(mouse_pos.x),
                        round(mouse_pos.y)
                    )
                    self.points.append(point)

            case pygame.KEYDOWN:
                # Отменить последнюю точку
                if event.key == pygame.K_BACKSPACE:
                    if self.points:
                        self.points.pop()

                # Завершить полигон
                elif event.key == pygame.K_RETURN:
                    if len(self.points) >= 3:
                        self.polygons.append(self.points.copy())
                        self.points.clear()

                # Вывести координаты
                elif event.key == pygame.K_c:
                    print("=== POLYGONS ===")
                    for polygon in self.polygons:
                        print(f"{polygon},")

                # Очистить незавершённый полигон
                elif event.key == pygame.K_DELETE:
                    self.points.clear()

    def polygon_editor_draw(self, mouse_pos):
        if not self.polygon_editor or not self.enabled:
            return

        for polygon in self.polygons:
            points = [self.world_to_screen(p) for p in polygon]
            self.draw('polygon', 'red', points, width=2)

        points = [self.world_to_screen(p) for p in self.points]

        for point in points:
            self.draw('circle', 'yellow', point, radius=4)

        if len(points) >= 2:
            self.draw('lines', 'cyan', False, points, width=2)

        if points and mouse_pos is not None:
            cursor = self.world_to_screen(mouse_pos)
            self.draw('line', 'orange', points[-1], cursor, width=1)

    def draw_building(self, objects, color='red', arg='polygon'):
        if not self.show_polygon:
            return

        for obj in objects:
            if arg == 'threshold':
                if not isinstance(obj, Building) or obj.is_interior_obstacle:
                    continue

            points = []
            func = obj.get_polygon if arg == 'polygon' else obj.get_threshold

            for point in func():
                points.append(self.world_to_screen(point))

            if len(points) >= 3:
                self.draw('polygon', color, points, width=2)