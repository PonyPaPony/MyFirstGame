from player import Player
from enemy import Enemy

class Core:
    def __init__(self):
        self.current_location = None
        self.current_space = None #! NOTE: this is a space where player is located

        self.units = None

        self.player_pos = None
        self.player_name = None

        self.camp = None

        self.image = None
        self.position = None

        self.objects = None

        self.temp_name()

    def temp_name(self):
        #- TODO(linked): future we can use this for save&load logic
        if self.current_location is None:
            self.current_location = 'start_city'
            self.current_space = 'start_city'
        if self.player_pos is None:
            self.player_pos = (773, 260)
        if self.player_name is None:
            self.player_name = 'priscilla'

    def connect(self, world):
        self.camp = world.add_camp()
        return self.camp

    def update(self, world):
        next_location = self.get_next_location()

        if next_location is not None:
            self.image, self.position, self.objects, self.player_pos = world.load_space(next_location)
            self.current_space = next_location.id
            self.units.player.pos.update(self.player_pos['enter'])
            self.units.player.interaction_target = None

        elif self.current_space != self.current_location:
            building = world.load_building(self.current_space)

            self.image, self.position = world.load_location(self.current_location)
            self.objects = world.get_objects(self.current_location)

            self.units.player.pos.update(building.player_pos['exit'])
            self.current_space = self.current_location
            self.units.player.interaction_target = None

        else:
            self.image, self.position = world.load_location(self.current_location)
            self.objects = world.get_objects(self.current_location)

        return self.image, self.position, self.objects

    def get_next_location(self):
        target = self.units.player.interaction_target
        if target is not None:
            return target
        return None


    def init_units(self, world):
        #- TODO(linked): in my opinion same here we should spawn all units not logic just spawn
        world.spawn_player(Player, self.player_name, self.player_pos, speed=50)

    def register_units(self, units):
        self.units = units

    def exit_from(self):
        return self.current_space, self.current_location