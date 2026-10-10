from data.location_templates import LOCATIONS
from spawner import resize_image

class Location:
    image_cache = {}

    def __init__(self, location):
        self.data = LOCATIONS[location]
        self.id = location

        self.name = self.data['identity']['name']
        self.location_type = self.data['identity']['type']

        self.position = self.data['geometry']['position']
        self.height = self.data['geometry']['height']
        self.path = self.data['tech_data']['path']

        if self.id not in Location.image_cache:
            Location.image_cache[self.id] = self.resize_location()

        self.image = Location.image_cache[self.id]

    def resize_location(self):
        return resize_image(self.path, self.height)
