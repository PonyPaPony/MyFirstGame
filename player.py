import config
from entity import Entity
from combat import try_attack

class Player(Entity):
    def __init__(self, image, x, y, stats, unit_type):
        super().__init__(image, x, y, stats, unit_type)

        self.in_combat = False
        self.combat_exit_timer = 0

    def update_player(self, direction, dt, mouse_pos, world_rect, enemies):
        self.update(dt)
        self.attack(mouse_pos, enemies)
        self.move(direction, dt, world_rect, obstacles=enemies)
        self.update_player_combat_time(dt, enemies)

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
