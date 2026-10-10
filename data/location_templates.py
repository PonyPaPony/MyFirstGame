LOCATIONS = {
    'start_city': {
        'identity': {
            'type': 'town',
            'name': 'Undershift',
            'description': """
            Это небольшой городок с населением, в основном, из крестьян, ремесленников и бывших авантюристов.
            Городок в основном, выглядит опрятным, а горожане в большинстве своем, добрые и честные люди.
            Однако Катаклизм, Эр'Хаунд Зи'Атре, существенно осложнил жизнь горожан, из-за чего сюда активнее
            стали приходить сомнительные личности, а так же Авантюристы
            """
        },

        'geometry': {
            'height': 1200,
            'collision': (),
            'exits': (),
            'position': (0, 0),
        },

        'spawns': {
            'player_spawn': (), # nearby crutch
            'enemy_spawns': [],
            'npc_spawns': [], #? WHY: really why tuple, if NPC not be one, so need more positions, for example, [(), ()]
        },

        'population_rules': {
            'permitted_enemies': [],
            'permitted_npcs': [
                'citizen',
                'blacksmith',
                'priest',
                'merchant',
                'guard',
                'important',
                'shady character'
            ], #- TODO(next): who exactly is NPC, or better ask how many NPCs will be in the city
        },
        "buildings": [
            'undershift_blacksmith',
            'undershift_market',
            'undershift_guild'
        ],

        'tech_data': {
            'path': 'Images/temp_name/start_city.png',
        },
    }
}

#! NOTE: permitted_npcs, right now it is a list template NPC


BUILDINGS = {
    'undershift_blacksmith': {
        'identity': {
            'type': 'blacksmith',
            'name': 'blacksmith',
            'description': """""",
        },
        'geometry': {
            'height': 700,
            'position': (0, 0),
            'collision': [
                (513, 310), (442, 317), (398, 316), (398, 300), (344, 302), (344, 320), (249, 322), (75, 331),
                (53, 289), (45, 206), (114, 191), (166, 182), (165, 127), (196, 120), (219, 128), (222, 165),
                (321, 134), (326, 95), (342, 92), (359, 101), (359, 118), (401, 101), (461, 129), (469, 161),
                (498, 166), (506, 195), (486, 210), (492, 228), (529, 236)
            ],
            'interior_collision': [
                [
                    (404, 357), (403, 390), (332, 396), (305, 387), (285, 376), (274, 365), (273, 328), (307, 312)
                ],
            ]
        },
        'threshold': {
            'area': [
                (399, 317), (398, 300), (344, 302), (344, 319)
            ],
            'player_pos': {
                'enter': (580, 468),
                'exit': (323, 206)
            }
        },
        'exit': [
            (511, 575),
            (719, 575),
            (721, 640),
            (512, 640)
        ],
        'in_city': [
            'start_city'
        ],
        'tech_data': {
            'path': 'Images/temp_name/blacksmith.png'
        }
    },
    'undershift_market': {
        'identity': {
            'type': 'market',
            'name': "market",
            'description': """"""
        },
        'geometry': {
            'height': 0,
            'position': (0, 0),
            'collision': [
                (837, 319), (877, 319), (896, 305), (943, 261), (987, 226), (955, 210),
                (947, 116), (931, 111), (922, 118), (921, 141), (872, 136), (831, 93),
                (779, 138), (729, 133), (720, 162), (703, 184), (665, 222), (667, 287), (716, 306), (834, 318)
            ],
            'interior_collision': [
                [
                    (0, 0),
                    (0, 1)
                ]
            ]
        },
        'threshold': {
            'area': [
                (683, 294), (723, 299), (719, 312), (683, 310)
            ],
            'player_pos': {
                'enter': (580, 468),
                'exit': (323, 206)
            }
        },
        'exit': [
            (511, 575),
            (719, 575),
            (721, 640),
            (512, 640)
        ],
        'in_city': [
            'start_city'
        ],
        'tech_data': {
            'path': "",
        }
    },
    'undershift_guild': {
        'identity': {
            'type': 'guild',
            'name': 'guild',
            'description': ''
        },
        'geometry': {
            'height': 0,
            'position': (0, 0),
            'collision': [
                (1096, 378),
                (1011, 367),
                (971, 351),
                (1014, 319),
                (1010, 234),
                (1054, 128),
                (1066, 104),
                (1083, 110),
                (1083, 134),
                (1131, 139),
                (1131, 102),
                (1159, 40),
                (1196, 88),
                (1194, 145),
                (1308, 156),
                (1329, 179),
                (1416, 190),
                (1387, 275),
                (1384, 347),
                (1377, 374),
                (1302, 355),
                (1260, 394),
                (1189, 388),
                (1167, 384),
                (1165, 383),
                (1176, 353),
                (1111, 344),
                (1100, 377)
            ],
            'interior_collision': [
                [
                    (0, 0),
                    (0, 1)
                ]
            ]
        },
        'threshold': {
            'area': [
                (1097, 376),
                (1110, 346),
                (1175, 355),
                (1164, 382)
            ],
            'player_pos': {
                'enter': (580, 468),
                'exit': (323, 206)
            }
        },
        'exit': [
            (511, 575),
            (719, 575),
            (721, 640),
            (512, 640)
        ],
        'in_city': [
            'start_city'
        ],
        'tech_data': {
            'path': "",
        }
    },
}