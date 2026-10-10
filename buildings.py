import pygame
from spawner import resize_image
from data.location_templates import BUILDINGS


class Building:
    image_cache = {}

    def __init__(self, building, polygon=None):
        self.data = BUILDINGS[building]
        self.id = building

        self.name = self.data['identity']['name']
        self.position = self.data['geometry']['position']

        self.player_pos = self.data['threshold']['player_pos']

        self.building_type = self.data['identity']['type']
        self.polygon = (
            polygon if polygon is not None else
            self.data['geometry']['collision']
        )
        self.is_interior_obstacle = polygon is not None
        self.threshold = self.data['threshold']['area']
        self.exit = self.data['exit']

        self.path = self.data['tech_data']['path']
        self.height = self.data['geometry']['height']

        if self.id not in Building.image_cache:
            Building.image_cache[self.id] = self.resize_image_build()

        self.image = Building.image_cache[self.id]

    def resize_image_build(self):
        if self.path == '':
            return None
        return resize_image(self.path, self.height)

    def get_polygon(self):
        return self.polygon

    def get_threshold(self):
        return self.threshold

    def get_edges(self):
        for i in range(len(self.polygon)):
            yield self.polygon[i], self.polygon[(i + 1) % len(self.polygon)]

    def sides(self, area):
        xs = []
        ys = []

        for x, y in area:
            xs.append(x)
            ys.append(y)

        left = min(xs)
        right = max(xs)
        top = min(ys)
        bottom = max(ys)

        return left, right, top, bottom

    def collides_with(self, rect):
        for start, end in self.get_edges():
            if rect.clipline(start, end):
                return True

        return False

    def player_at_threshold(self, player):
        left, right, top, bottom = self.sides(self.threshold)
        rect = pygame.Rect(left, top, right - left, bottom - top)
        return rect.colliderect(player.get_hitbox())

    def player_at_exit(self, player):
        left, right, top, bottom = self.sides(self.exit)
        rect = pygame.Rect(left, top, right - left, bottom - top)
        return rect.colliderect(player.get_hitbox())