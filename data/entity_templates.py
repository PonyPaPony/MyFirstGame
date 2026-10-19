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
        },
        'position': (1345, 449),
        'group': 'player', #! NOTE: she is player temporary, 'cause she is NPC
        'space_id': 'start_city'
    },
    'Oliver': {
        'path': "Images/Models/Oliver.png",
        'height': 100,
        'unit_type': 'melee',
        'hitbox': {
            'x': 0.35,
            'y': 0.8,
            'w': 0.4,
            'h': 0.1
        },
        'stats': {
            'max_health': 10000000,
            'attack': 0,
            'defence': 0,
            'speed': 20,
            'attack_speed': 5,
            'dodge': 0,
            'accuracy': 100,
            'crit_chance': 5,
            'crit_dmg': 50,
        },
        'position': (582, 154),
        'group': 'npc',
        'space_id': 'undershift_blacksmith',
        'schedule': {
            'work': {
                'position': (582, 154),
                'space_id': 'undershift_blacksmith',
                'route': {
                    'start_city': [
                        (481, 781), (623, 773), (819, 673), (704, 588), (606, 482), (523, 418), (439, 369)
                    ],
                    'undershift_blacksmith': [
                        (620, 548), (694, 413), (769, 281), (765, 228), (614, 187), (582, 154)
                    ],
                }
            },
            'home': {
                'position': (429.966, 697.2),
                'space_id': 'start_city',
                'route': {
                    'undershift_blacksmith': [
                        (634, 239), (573, 235), (514, 257), (511, 318), (576, 381),
                        (612, 446), (611, 511), (612, 575), (612, 626)
                    ],
                    'start_city': [
                        (432, 364), (511, 422), (640, 422), (767, 387), (906, 422), (946, 371),
                        (946, 371), (971, 422), (1205, 467), (1420, 500), (1656, 588), (1663, 590),
                        (1655, 664), (1593, 722), (1468, 804), (1316, 773),
                        (1198, 800), (1059, 781), (955, 734), (837, 735), (772, 765), (674, 803), (569, 817), (469, 782)
                    ],
                }
            }
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
        },
        'position': (500, 500),
        'group': 'enemies',
        'space_id': 'start_city'
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
        },
        'position': (500, 500),
        'group': 'enemies',
        'space_id': 'start_city'
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