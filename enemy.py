import math
import config
import pygame
from entity import Entity
from combat import try_attack

class Enemy(Entity):
    def __init__(self, image, x, y, stats, unit_type):
        super().__init__(image, x, y, stats, unit_type)

        self.state = "idle"
        self.surround_slot = None

        self.aggro_cooldown = 0
        self.is_charging = False

        self.states = {
            'idle': self.idle,
            'chase': self.chase,
            'surround': self.surround,
            'comeback': self.comeback
        }

        self.unit = {
            'slots': config.SLOTS[unit_type],
            'aggro': config.AGGRO[unit_type],
            'leash': config.LEASH[unit_type],
            'zone': config.ZONE[unit_type]
        }

    def get_distance(self, target):
        return (target - self.feet()).length()

    def get_surround_point(self, target, slot, radius_x, radius_y):
        angle = 2 * math.pi * slot / self.unit['slots']

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

        for i in range(self.unit['slots']):
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
        if target.stats['current_health'] <= 0:
            return

        if distance <= self.unit['aggro'] and self.aggro_cooldown == 0:
            self.state = 'chase'

    def chase(self, target, distance, dt, bounds, obstacles, enemies):
        if target.stats['current_health'] <= 0:
            self.state = 'comeback'
            return

        if distance > self.unit['leash']:
            self.state = 'comeback'
        elif distance <= self.unit['aggro'] / 2:
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
            self.stats['current_health'] = self.stats['max_health']
            self.surround_slot = None
            self.is_charging = False

    def check_surround_status(self, target, x, y, formation_enemy):
        if self.surround_slot is None:
            self.assign_surround_slot(
                target, x, y, formation_enemy
            )

        if self.surround_slot is None:
            self.aggro_cooldown = config.AGGRO_COOLDOWN
            self.state = 'comeback'
            return False

        return True

    def surround(self, target, distance, dt, bounds, obstacles, enemies):
        if target.stats['current_health'] <= 0 or distance > self.unit['leash']:
            self.is_charging = False
            self.state = 'comeback'
            return

        x = self.unit['zone']['x']
        y = self.unit['zone']['y']

        formation_enemy = [enemy for enemy in enemies if enemy.unit_type == self.unit_type]

        if not self.check_surround_status(target, x, y, formation_enemy):
            return

        target_point = self.get_surround_point(target, self.surround_slot, x, y)

        if try_attack(self, target):
            self.is_charging = True
            return

        if self.to_charge(target_point, dt, bounds, obstacles, target):
            return

        moved = self.move_to(target_point, dt, bounds, obstacles)

        remaining = self.get_distance(target_point)
        if not moved and remaining > 5:
            print("Stuck!", self.surround_slot)

    def update_ai(self, target, dt, bounds, enemies, obstacles=()):
        distance = self.get_distance(target.feet())

        if self.aggro_cooldown > 0:
            self.aggro_cooldown = max(0, self.aggro_cooldown - dt)

        self.update(dt)

        harry_potter = self.states[self.state]
        harry_potter(target, distance, dt, bounds, obstacles, enemies)


    def to_charge(self, target_point, dt, bounds, obstacles, target):
        if self.is_charging or self.get_distance(target_point) <= 5:
            self.is_charging = True

            self.move_to(
                target.feet(),
                dt,
                bounds,
                obstacles,
                stop_distance=self.stats['attack_range'] * config.TILE_SIZE / 2
            )
            return True

        return False