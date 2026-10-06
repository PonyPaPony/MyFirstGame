from data.location_templates import LOCATIONS
from spawner import resize_image

class Location:
    def __init__(self, location):
        self.data = LOCATIONS[location]

        self.name = self.data['identity']['name']
        self.location_type = self.data['identity']['type']

        self.position = self.data['geometry']['position']
        self.height = self.data['geometry']['height']
        self.path = self.data['tech_data']['path']

        self.image = self.resize_location()
        self.size = self.image.get_size()

    def resize_location(self):
        return resize_image(self.path, self.height)
