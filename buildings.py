import pygame
from spawner import resize_image
from data.location_templates import BUILDINGS


class Building:
    def __init__(self, building):
        self.data = BUILDINGS[building]

        self.name = self.data['identity']['name']
        self.position = self.data['geometry']['position']

        self.building_type = self.data['identity']['type']
        self.polygon = self.data['geometry']['collision']
        self.threshold = self.data['threshold']['area']

        self.path = self.data['tech_data']['path']
        self.height = self.data['geometry']['height']

        self.image = self.resize_image_build()

    def resize_image_build(self):
        return resize_image(self.path, self.height)

    def get_polygon(self):
        return self.polygon

    def get_threshold(self):
        return self.threshold

    def get_edges(self):
        for i in range(len(self.polygon)):
            yield self.polygon[i], self.polygon[(i + 1) % len(self.polygon)]

    def sides(self):
        xs = []
        ys = []

        for x, y in self.threshold:
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
        left, right, top, bottom = self.sides()
        rect = pygame.Rect(left, top, right - left, bottom - top)
        return rect.colliderect(player.get_hitbox())
