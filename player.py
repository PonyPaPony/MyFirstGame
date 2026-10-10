import config
from entity import Entity
from combat import try_attack
from buildings import Building

class Player(Entity):
    def __init__(self, image, x, y, stats, unit_type):
        super().__init__(image, x, y, stats, unit_type)

        self.in_combat = False
        self.interaction_target = None
        self.current_location = None
        self.combat_exit_timer = 0

    def update_player(self, direction, dt, mouse_pos, world_rect, enemies, obstacles):
        self.update(dt)
        self.attack(mouse_pos, enemies)
        self.move(direction, dt, world_rect, obstacles=obstacles)
        self.update_player_combat_time(dt, enemies)
        self.object_filter(obstacles)

    def object_filter(self, objects):
        buildings = []
        for obj in objects:
            if isinstance(obj, Building) and not obj.is_interior_obstacle:
                buildings.append(obj)
        self.can_interact_with_build(buildings)


    def can_interact_with_build(self, buildings):
        for build in buildings:
            if build.player_at_threshold(self):
                self.interaction_target = build
                return
        self.interaction_target = None

    def can_exit_building(self, current_space, current_location):
        if current_space == current_location:
            return False

        building = Building(current_space)
        return building.player_at_exit(self)

    def get_target(self, mouse_pos, targets):
        if mouse_pos is None:
            return None

        for target in targets:
            if target.get_rect().collidepoint(mouse_pos):
                return target

        return None

    def attack_target(self, target):
        if target is None:
            return

        try_attack(self, target)

    def attack(self, mouse_pos, targets):
        target = self.get_target(mouse_pos, targets)
        self.attack_target(target)

    def update_player_combat_time(self, dt, enemies):
            active_combat =  any(
                enemy.state in ('chase', 'surround')
                for enemy in enemies
            )
            if active_combat:
                self.in_combat = True
                self.combat_exit_timer = config.COMBAT_EXIT_DELAY
                return

            if not self.in_combat:
                return

            self.combat_exit_timer -= dt

            if self.combat_exit_timer <= 0:
                self.combat_exit_timer = 0
                self.in_combat = False
