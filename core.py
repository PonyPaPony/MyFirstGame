from player import Player
# from enemy import Enemy
from world_spawn import WorldSpawn
from game_utils import WorldTime
from units import Units
from world_rules import WorldRules


class Core:
    def __init__(self):
        self.current_location = None
        self.current_space = None

        self.image = None
        self.position = None
        self.objects = None
        self.player_position = None
        self.player_name = None

        self.units = None
        self.camp = None

        self.temp_name()

    def temp_name(self):
        #- TODO(linked): future we can use this for save&load logic
        if self.current_location is None:
            self.current_location = 'start_city'
            self.current_space = 'start_city'
        if self.player_position is None:
            self.player_position = (1345, 449)
        if self.player_name is None:
            self.player_name = 'Priscilla'

    def connect(self, world):
        self.camp = world.add_camp()
        return self.camp

    def get_next_location(self):
        target = self.units.player.interaction_target
        if target is not None:
            return target
        return None

    def register_units(self, units):
        self.units = units

    def exit_from(self):
        return self.current_space, self.current_location

    def update(self, world):
        next_location = self.get_next_location()

        if next_location is not None:
            self.image, self.position, self.objects, self.player_position = world.load_space(next_location)
            self.current_space = next_location.id
            self.units.player.position.update(self.player_position['enter'])
            self.units.player.interaction_target = None
        elif self.current_space != self.current_location:
            building = world.load_building(self.current_space)

            self.image, self.position = world.load_location(self.current_location)
            self.objects = world.get_objects(self.current_location)

            self.units.player.position.update(building.player_position['exit'])
            self.current_space = self.current_location
            self.units.player.interaction_target = None

        else:
            self.image, self.position = world.load_location(self.current_location)
            self.objects = world.get_objects(self.current_location)

        return self.image, self.position, self.objects


class WorldInit:
    def __init__(self):
        self.image = None
        self.pos = None
        self.objects = None

        self.core = Core()
        self.world_time = WorldTime()
        self.world_rules = WorldRules(self.world_time)
        self.units = Units()
        self.world_spawn = WorldSpawn(self.units)

        self.core.register_units(self.units)
        self.player_init()
        self.world_update()
        self.camps = self.core.connect(self.world_rules)


    def world_update(self):
        self.image, self.pos, self.objects = self.core.update(self.world_spawn)

    def tick(self, dt, camera_rect):
        self.world_time.update(dt)
        self.world_rules.update()
        self.world_spawn.update(camera_rect)

    def player_init(self):
        self.world_spawn.spawn_player(Player, self.core.player_name, self.core.player_position, speed=50)