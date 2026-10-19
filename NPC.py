import pygame
from entity import Entity
from data.entity_templates import UNITS

class NPC(Entity):
    def __init__(self, name, image, x, y, stats, unit_type):
        super().__init__(name, image, x, y, stats, unit_type)

        self.states = {
            'work': "temporary_empty",
            'going': "temporary_empty",
            'home': "temporary_empty"
        }

        self.current_state = None

    # ! NOTE: Let's think about how the NPC should work.
    # ! NOTE: I think the NPC should have a function to change its state based on the situation.
    # ! NOTE: The NPC should be immortal. We also need to decide how it should move: by teleporting or walking.

    # ! NOTE: NPC should have a access to own mechanic from this class but it should be linked with situation
    # ! NOTE: On top of that, a hearth mechanic should be have own file


class AIforNPC:
    def __init__(self, world_spawn):
        self.world_spawn = world_spawn

    def update_npc_states(self, world_hour):
        for record in self.world_spawn.records:
            if record.group != 'npc':
                continue

            new_state = 'work' if 6 <= world_hour <= 20 else 'home'

            if record.current_state != new_state and record.target_state != new_state:
                self.to_go(record, new_state)

    @staticmethod
    def to_go(record, target):
        schedule = UNITS[record.name].get('schedule')

        if not schedule or target not in schedule:
            return

        record.target_state = target
        record.current_state = 'going'
        record.path_index = 0

    def finish_npc_route(self, record):
        if record.target_state is None:
            return

        destination = UNITS[record.name]['schedule'][record.target_state]

        record.pos = destination['position']
        record.space_id = destination['space_id']

        if record.entity is not None:
            self.world_spawn.deactivate_record(record)

        record.current_state = record.target_state
        record.target_state = None

    def update(self, camera_rect, space_id, dt):
        for record in self.world_spawn.records:
            if record.group != 'npc' or record.current_state != 'going':
                continue

            is_visible = (
                    record.space_id == space_id
                    and camera_rect.collidepoint(record.pos)
            )

            destination = UNITS[record.name]['schedule'][record.target_state]
            routes = destination['route']

            if not is_visible:
                if destination['space_id'] == space_id and record.space_id != space_id:
                    self.teleport_to_route(record, space_id, routes)
                else:
                    self.finish_npc_route(record)

                continue

            route = routes.get(record.space_id)
            if route:
                self.follow_path(record, route, dt)

    def follow_path(self, record, route, dt, bounds=None, obstacles=()):
        npc = record.entity

        if npc is None or record.path_index >= len(route):
            return

        target = pygame.Vector2(route[record.path_index])
        npc.move_to(target, dt, bounds, obstacles)
        record.pos = tuple(npc.position)

        if npc.feet().distance_to(target) <= 5:
            record.path_index += 1

        if record.path_index >= len(route):
            routes = UNITS[record.name]['schedule'][record.target_state]['route']
            self.next_route(record, routes)

    def next_route(self, record, routes):
        spaces = list(routes)

        current_index = spaces.index(record.space_id)

        if current_index + 1 >= len(spaces):
            self.finish_npc_route(record)
            return

        next_space = spaces[current_index + 1]

        self.world_spawn.deactivate_record(record)

        record.space_id = next_space
        record.pos = routes[next_space][0]
        record.path_index = 1

    def teleport_to_route(self, record, space_id, routes):
        route = routes.get(space_id)

        if not route:
            self.finish_npc_route(record)
            return

        if record.entity is not None:
            self.world_spawn.deactivate_record(record)

        record.space_id = space_id
        record.pos = pygame.Vector2(route[0]) - record.feet_offset
        record.path_index = 1