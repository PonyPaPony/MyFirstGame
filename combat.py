import random
import config

def try_to_hit(attacker, defender):
    accuracy = min(attacker['accuracy'], attacker['accuracy_limit'])
    dodge = min(defender['dodge'], defender['dodge_limit'])

    if accuracy <= 100:
        hit_chance = accuracy - dodge
    else:
        bonus_accuracy = (accuracy - 100) / 2
        hit_chance = 100 - dodge + bonus_accuracy

    hit_chance = max(0, min(100, hit_chance))

    roll = random.randint(1, 100)
    return roll <= hit_chance


def attack(attacker, defender):
    if defender['current_health'] <= 0:
        return 0, 0

    if attacker['current_health'] < 1:
        return 0, defender['current_health']

    if not try_to_hit(attacker, defender):
        return 0, defender['current_health']

    atk = max(1, attacker['attack'])
    dff = defender['defence']

    return deal_damage(atk, dff, attacker, defender)


def effective_defence(defence, pen):
    ef_defence = defence * (1 - pen)
    return max(0, ef_defence)


def penetration(atk):
    pen = atk / (atk + 100)
    return min(0.5, pen)


def get_crit_result(attacker):
    chance = min(attacker['crit_chance'], attacker['crit_chance_limit'])
    roll = random.randint(1, 100)
    return roll <= chance


def deal_damage(atk, dff, attacker, defender):
    pen = penetration(atk)
    edef = effective_defence(dff, pen)

    damage = atk * 100 / (100 + edef)

    if get_crit_result(attacker):
        damage = damage * (1 + attacker['crit_dmg'] / 100)

    damage = max(1, round(damage))
    defender['current_health'] = max(0, defender['current_health'] - damage)

    return damage, defender['current_health']


def can_attack(attacker, defender):
    distance = (
        defender.feet() - attacker.feet()
    ).length()

    attack_range = (
        attacker.stats['attack_range'] * config.TILE_SIZE / 2
    )

    return distance <= attack_range

def try_attack(attacker, defender):
    if not can_attack(attacker, defender):
        return False

    if attacker.attack_timer <= 0:
        attack(attacker.stats, defender.stats)

        attacker.attack_timer = max(
            attacker.stats['attack_speed'],
            attacker.stats['attack_speed_limit']
        )

    return True