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
            'height': 400,
            'position': (0, 0),
            'collision': [
                (433, 310),
                (373, 317),
                (336, 316),
                (336, 300),
                (290, 302),
                (290, 320),
                (210, 322),
                (63, 331),
                (45, 289),
                (38, 206),
                (96, 191),
                (140, 182),
                (139, 127),
                (165, 120),
                (185, 128),
                (187, 165),
                (271, 134),
                (275, 95),
                (289, 92),
                (303, 101),
                (303, 118),
                (338, 101),
                (389, 129),
                (396, 161),
                (420, 166),
                (427, 195),
                (410, 210),
                (415, 228),
                (446, 236),
            ],
        },

        'threshold': {
            'area': [
                (337, 317),
                (336, 300),
                (290, 302),
                (290, 319),
            ]
        },
        'tech_data': {
            'path': 'Images/temp_name/blacksmith.png'
        }
    }
}