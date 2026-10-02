from entity import Entity
from combat import try_attack

class Player(Entity):
    def __init__(self, image, x, y, stats, unit_type):
        super().__init__(image, x, y, stats, unit_type)

    def update_player(self, direction, dt, mouse_pos, world_rect, enemies):
        self.update(dt)
        self.attack(mouse_pos, enemies)
        self.move(direction, dt, world_rect, obstacles=enemies)

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
