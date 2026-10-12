UNITS = {
    'Priscilla': {
        'path': "Images/Models/Priscilla.png",
        'height': 100,
        'unit_type': 'range',
        'hitbox': {
            'x': 0.35,
            'y': 0.8,
            'w': 0.4,
            'h': 0.1
        },
        'stats': {
            'max_health': 10000000,
            'attack': 100,
            'defence': 100,
            'speed': 10,
            'attack_speed': 5,
            'dodge': 0,
            'accuracy': 100,
            'crit_chance': 5,
            'crit_dmg': 50,
        }
    },
    'goblin_swordman': {
        'path': "Images/Enemies/Goblin_swordman.png",
        'height': 100,
        'unit_type': 'melee',
        'hitbox': {
            'x': 0.35,
            'y': 0.8,
            'w': 0.4,
            'h': 0.1
        },
        'stats': {
            'max_health': 180,
            'attack': 70,
            'defence': 50,
            'speed': 10,
            'attack_speed': 3,
            'dodge': 0,
            'accuracy': 100,
            'crit_chance': 5,
            'crit_dmg': 50,
        }
    },
    'goblin_archer': {
        'path': "Images/Enemies/Goblin_archer.png",
        'height': 100,
        'unit_type': 'range',
        'hitbox': {
            'x': 0.35,
            'y': 0.8,
            'w': 0.4,
            'h': 0.1
        },
        'stats': {
            'max_health': 80,
            'attack': 110,
            'defence': 30,
            'speed': 20,
            'attack_speed': 3,
            'dodge': 0,
            'accuracy': 115,
            'crit_chance': 5,
            'crit_dmg': 50,
        }
    }
}

LIMITS = {
    'crit_chance_limit': 75,
    'dodge_limit': 80,
    'accuracy_limit': 200,
    'speed_limit': 50,
    'attack_speed_limit': 0.5,
}
STATE = {
    'current_health': 100,
}

ATTACK_RANGE = {
    'melee': 1,
    "range": 10,
    "mage": 12,
}