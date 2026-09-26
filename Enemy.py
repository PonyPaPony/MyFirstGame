import math
import config
import pygame
from entity import Entity

class Enemy(Entity):
    def __init__(self, image, x, y, stats, unit_type):
        super().__init__(image, x, y, stats, unit_type)

        self.state = "idle"
        self.surround_slot = None
        self.aggro_cooldown = 0

        self.states = {
            'idle': self.idle,
            'chase': self.chase,
            'surround': self.surround,
            'comeback': self.comeback
        }

    def get_distance(self, target):
        return (target - self.feet()).length()

    def get_surround_point(self, target, slot, radius_x, radius_y):
        angle = 2 * math.pi *slot / config.SLOTS[self.unit_type]

        x = radius_x * math.cos(angle)
        y = radius_y * math.sin(angle)

        center = target.feet()

        return pygame.Vector2(center.x + x, center.y + y)

    def assign_surround_slot(self, target, radius_x, radius_y, enemies):
        occupied_slots = [
            enemy.surround_slot
            for enemy in enemies
            if enemy.surround_slot is not None
        ]
        empty_slots = []

        best_slot = None
        best_distance = None

        for i in range(config.SLOTS[self.unit_type]):
            if i in occupied_slots:
                continue
            empty_slots.append(i)

        for slot in empty_slots:
            target_point = self.get_surround_point(target, slot, radius_x, radius_y)
            distance = self.get_distance(target_point)

            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_slot = slot

        self.surround_slot = best_slot

    def idle(self, target, distance, dt, bounds, obstacles, enemies):
        if distance <= config.ARGO[self.unit_type] and self.aggro_cooldown == 0:
            print(
                'BACK TO WORK!',
                'Cooldown:', self.aggro_cooldown
            )
            self.state = 'chase'

    def chase(self, target, distance, dt, bounds, obstacles, enemies):
        if distance > config.LEASH[self.unit_type]:
            self.state = 'comeback'
        elif distance <= config.ARGO[self.unit_type] / 2:
            self.state = 'surround'
        else:
            self.move_to(
                target.feet(),
                dt,
                bounds,
                obstacles
            )

    def comeback(self, target, distance, dt, bounds, obstacles, enemies):
        self.move_to(
            self.spawn_pos,
            dt,
            bounds,
            obstacles,
            stop_distance=0,
            speed_multiplier=2
        )
        home_distance = self.get_distance(self.spawn_pos)
        if home_distance <= 1:
            self.state = 'idle'
            self.surround_slot = None

    def surround(self, target, distance, dt, bounds, obstacles, enemies):
        if distance > config.LEASH[self.unit_type]:
            self.state = 'comeback'
            return

        x = config.ZONE[self.unit_type]['x']
        y = config.ZONE[self.unit_type]['y']

        formation_enemy = [enemy for enemy in enemies if enemy.unit_type == self.unit_type]

        if self.surround_slot is None:
            self.assign_surround_slot(target, x, y, formation_enemy)

        if self.surround_slot is None:
            self.aggro_cooldown = config.AGGRO_COOLDOWN
            print('FUCK THIS JOB!')
            self.state = 'comeback'
            return

        target_point = self.get_surround_point(target, self.surround_slot, x, y)
        self.move_to(target_point, dt, bounds, obstacles)

    def update_ai(self, target, dt, bounds, enemies, obstacles=()):
        distance = self.get_distance(target.feet())

        if self.aggro_cooldown > 0:
            self.aggro_cooldown = max(
                0,
                self.aggro_cooldown - dt
            )

        harry_potter = self.states[self.state]
        harry_potter(target, distance, dt, bounds, obstacles, enemies)