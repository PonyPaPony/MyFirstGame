from player import Player
from NPC import AIforNPC
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
        self.world_time.set_time(1250)
        self.last_hour = self.world_time.get_hour()

        self.world_rules = WorldRules(self.world_time)
        self.units = Units()
        self.world_spawn = WorldSpawn(self.units)
        self.npc_ai = AIforNPC(self.world_spawn)

        self.core.register_units(self.units)
        self.player_init()
        self.npc_init()
        self.world_update()
        self.camps = self.core.connect(self.world_rules)

        self.npc_ai.update_npc_states(self.world_time.get_hour())


    def world_update(self):
        self.image, self.pos, self.objects = self.core.update(self.world_spawn)

    def time_update(self):
        current_hour = self.world_time.get_hour()
        if current_hour != self.last_hour:
            self.npc_ai.update_npc_states(current_hour)
            self.last_hour = current_hour

    def tick(self, dt, camera_rect):
        self.world_time.update(dt)
        self.time_update()
        self.world_rules.update()
        self.npc_ai.update(camera_rect, self.core.current_space, dt)
        self.world_spawn.update(camera_rect, self.core.current_space)

    def player_init(self):
        self.world_spawn.spawn_player(Player, self.core.player_name, self.core.player_position, speed=50)

    def npc_init(self): #- TODO(important): need to find "способ" fix next, trouble, NPC not react to time changes, 'cause i don't update time =_=
        self.world_spawn.register_entity(self.core.current_location, 'npc')