import random
import config


class Combat:
    def __init__(self):

        self.threshold = 100

        self.accuracy = 'accuracy'
        self.dodge = 'dodge'
        self.current_health = 'current_health'
        self.crit_chance = 'crit_chance'
        self.attack_stat = 'attack'
        self.attack_speed = 'attack_speed'
        self.attack_range = 'attack_range'
        self.defence = 'defence'

        self.limit = "_limit"

    def roll(self):
        return random.randint(1, self.threshold)

    def try_to_hit(self, attacker, defender):
        accuracy = min(attacker[self.accuracy], attacker[self.accuracy + self.limit])
        dodge = min(defender[self.dodge], defender[self.dodge + self.limit])

        if accuracy <= self.threshold:
            hit_chance = accuracy - dodge
        else:
            bonus_accuracy = (accuracy - self.threshold) / 2
            hit_chance = self.threshold - dodge + bonus_accuracy

        hit_chance = max(0, min(self.threshold, hit_chance))

        roll = self.roll()

        return roll <= hit_chance

    @staticmethod
    def effective_defence(defence, pen):
        eff_defence = defence * (1 - pen)
        return max(0, eff_defence)

    def penetration(self, atk):
        pen = atk / (atk + self.threshold)
        return min(0.5, pen)

    def crit_result(self, attacker):
        chance = min(attacker[self.crit_chance], attacker[self.crit_chance + self.limit])
        roll = self.roll()
        return roll <= chance

    def is_alive(self, unit):
        return unit[self.current_health] > 0

    def deal_damage(self, attack, defence, attacker, defender):
        pen = self.penetration(attack)
        eff_defence = self.effective_defence(defence, pen)

        damage = attack * self.threshold / (self.threshold + eff_defence)

        if self.crit_result(attacker):
            damage = damage * (1 + attacker['crit_dmg'] / self.threshold)

        damage = max(1, round(damage))
        defender[self.current_health] = max(0, defender[self.current_health] - damage)

        return damage, defender[self.current_health]

    def can_attack(self, attacker, defender):
        distance = (defender.feet() - attacker.feet()).length()

        attack_range = (attacker.stats[self.attack_range] * config.TILE_SIZE / 2)

        return distance <= attack_range

    def try_attack(self, attacker, defender):
        if not self.can_attack(attacker, defender):
            return False

        if attacker.attack_timer <= 0:
            self.attack(attacker.stats, defender.stats)

            attacker.attack_timer = max(
                attacker.stats[self.attack_speed],
                attacker.stats[self.attack_speed + self.limit]
            )

        return True

    def attack(self, attacker, defender):
        if defender[self.current_health] <= 0:
            return 0, 0

        if attacker[self.current_health] < 1:
            return 0, defender[self.current_health]

        if not self.try_to_hit(attacker, defender):
            return 0, defender[self.current_health]

        attack = max(1, attacker[self.attack_stat])
        defence = defender[self.defence]

        return self.deal_damage(attack, defence, attacker, defender)