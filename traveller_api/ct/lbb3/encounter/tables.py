'''tables.py'''

# TERRAIN_TYPES_DM: {
#   terrain: {'Terrain': terrain_type, 'Type DM': DM, 'Size DM': DM}, ...
# }
TERRAIN_TYPES_DM = {
    'Clear': {'Terrain': 'other', 'Type DM': +3, 'Size DM': 0},
    'Prairie': {'Terrain': 'other', 'Type DM': +4, 'Size DM': 0},
    'Rough': {'Terrain': 'other', 'Type DM': 0, 'Size DM': 0},
    'Broken': {'Terrain': 'other', 'Type DM': -3, 'Size DM': -3},
    'Mountain': {'Terrain': 'other', 'Type DM': 0, 'Size DM': 0},
    'Forest': {'Terrain': 'other', 'Type DM': -4, 'Size DM': -4},
    'Jungle': {'Terrain': 'other', 'Type DM': -3, 'Size DM': -2},
    'River': {'Terrain': 'river', 'Type DM': +1, 'Size DM': +1},
    'Swamp': {'Terrain': 'swamp', 'Type DM': -2, 'Size DM': +4},
    'Marsh': {'Terrain': 'marsh', 'Type DM': 0, 'Size DM': -1},
    'Desert': {'Terrain': 'other', 'Type DM': +3, 'Size DM': -3},
    'Beach': {'Terrain': 'beach', 'Type DM': +3, 'Size DM': +2},
    'Surface': {'Terrain': 'sea', 'Type DM': +2, 'Size DM': +3},
    'Shallows': {'Terrain': 'sea', 'Type DM': +2, 'Size DM': +2},
    'Depths': {'Terrain': 'sea', 'Type DM': +2, 'Size DM': +4},
    'Bottom': {'Terrain': 'sea', 'Type DM': -4, 'Size DM': 0},
    'Sea Cave': {'Terrain': 'sea', 'Type DM': -2, 'Size DM': 0},
    'Sargasso': {'Terrain': 'sea', 'Type DM': -4, 'Size DM': -2},
    'Ruins': {'Terrain': 'other', 'Type DM': -3, 'Size DM': 0},
    'Cave': {'Terrain': 'other', 'Type DM': -4, 'Size DM': +1},
    'Chasm': {'Terrain': 'other', 'Type DM': -1, 'Size DM': -3},
    'Crater': {'Terrain': 'other', 'Type DM': 0, 'Size DM': -1}
}

# ANIMAL_TYPES_TABLE: qty indicates number of dice for # animals (0 => single)
ANIMAL_TYPES_TABLE = [
    {   # 0
        'Herbivore': {'type': 'Filter', 'qty': 1},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Siren', 'qty': 0},
        'Scavenger': {'type': 'Carrion-eater', 'qty': 1}
    },
    {   # 1
        'Herbivore': {'type': 'Filter', 'qty': 0},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Pouncer', 'qty': 0},
        'Scavenger': {'type': 'Carrion-eater', 'qty': 2}
    },
    {   # 2
        'Herbivore': {'type': 'Filter', 'qty': 0},
        'Omnivore': {'type': 'Eater', 'qty': 0},
        'Carnivore': {'type': 'Siren', 'qty': 0},
        'Scavenger': {'type': 'Reducer', 'qty': 1}
    },
    {   # 3
        'Herbivore': {'type': 'Intermittent', 'qty': 0},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Pouncer', 'qty': 0},
        'Scavenger': {'type': 'Hijacker', 'qty': 1}
    },
    {   # 4
        'Herbivore': {'type': 'Intermittent', 'qty': 0},
        'Omnivore': {'type': 'Eater', 'qty': 2},
        'Carnivore': {'type': 'Killer', 'qty': 1},
        'Scavenger': {'type': 'Carrion-eater', 'qty': 2}
    },
    {   # 5
        'Herbivore': {'type': 'Intermittent', 'qty': 1},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Trapper', 'qty': 0},
        'Scavenger': {'type': 'Intimidator', 'qty': 1}
    },
    {   # 6
        'Herbivore': {'type': 'Intermittent', 'qty': 0},
        'Omnivore': {'type': 'Hunter', 'qty': 0},
        'Carnivore': {'type': 'Pouncer', 'qty': 0},
        'Scavenger': {'type': 'Reducer', 'qty': 0}
    },
    {   # 7
        'Herbivore': {'type': 'Filter', 'qty': 0},
        'Omnivore': {'type': 'Hunter', 'qty': 1},
        'Carnivore': {'type': 'Chaser', 'qty': 0},
        'Scavenger': {'type': 'Carrion-eater', 'qty': 1}
    },
    {   # 8
        'Herbivore': {'type': 'Grazer', 'qty': 1},
        'Omnivore': {'type': 'Hunter', 'qty': 0},
        'Carnivore': {'type': 'Chaser', 'qty': 3},
        'Scavenger': {'type': 'Reducer', 'qty': 3}
    },
    {   # 9
        'Herbivore': {'type': 'Grazer', 'qty': 2},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Chaser', 'qty': 0},
        'Scavenger': {'type': 'Hijacker', 'qty': 0}
    },
    {   # 10
        'Herbivore': {'type': 'Grazer', 'qty': 3},
        'Omnivore': {'type': 'Eater', 'qty': 1},
        'Carnivore': {'type': 'Killer', 'qty': 0},
        'Scavenger': {'type': 'Intimidator', 'qty': 2}
    },
    {   # 11
        'Herbivore': {'type': 'Grazer', 'qty': 2},
        'Omnivore': {'type': 'Hunter', 'qty': 1},
        'Carnivore': {'type': 'Chaser', 'qty': 2},
        'Scavenger': {'type': 'Reducer', 'qty': 1}
    },
    {   # 12
        'Herbivore': {'type': 'Grazer', 'qty': 4},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Siren', 'qty': 0},
        'Scavenger': {'type': 'Hijacker', 'qty': 0}
    },
    {   # 13
        'Herbivore': {'type': 'Grazer', 'qty': 5},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Chaser', 'qty': 1},
        'Scavenger': {'type': 'Intimidator', 'qty': 1}
    }
]

# ANIMAL_ATTRIBUTE_TABLE: terrain_type: (locomotion, size DM)
ANIMAL_ATTRIBUTE_TABLE = [
    {   # 2
        'beach': ('Swimming', 1),
        'marsh': ('Swimming', -6),
        'river': ('Swimming', 1),
        'sea': ('Swimming', 2),
        'swamp': ('Swimming', -3),
        'other': ('', 0)
    },
    {   # 3
        'beach': ('Amphibian', 2),
        'marsh': ('Amphibian', 2),
        'river': ('Amphibian', 1),
        'sea': ('Swimming', 2),
        'swamp': ('Amphibian', 1),
        'other': ('', 0)
    },
    {   # 4
        'beach': ('Amphibian', 2),
        'marsh': ('Amphibian', 1),
        'river': ('', 0),
        'sea': ('Swimming', 2),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 5
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Amphibian', 2),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 6
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Amphibian', 0),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 7
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Swimming', 1),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 8
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Swimming', -1),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 9
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Triphibian', -7),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 10
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Triphibian', -6),
        'swamp': ('', 0),
        'other': ('Flying', -6)
    },
    {   # 11
        'beach': ('Flying', -6),
        'marsh': ('Flying', -6),
        'river': ('Flying', -6),
        'sea': ('Flying', -6),
        'swamp': ('Flying', -6),
        'other': ('Flying', -5)
    },
    {   # 12
        'beach': ('Flying', -5),
        'marsh': ('Flying', -5),
        'river': ('Flying', -5),
        'sea': ('Flying', -5),
        'swamp': ('Flying', -5),
        'other': ('Flying', -3)
    },
]

# SIZE_WEAPONRY_TABLE: {'weight', 'hits', 'wounds', 'weapons', 'armor'}
SIZE_WEAPONRY_TABLE = [
    # 1
    {'weight': 1, 'hits': (1, 0), 'wounds': '-2D',
     'weapons': 'hooves and horns', 'armor': '+6'},
    # 2
    {'weight': 3, 'hits': (1, 1), 'wounds': '-2D',
     'weapons': 'horns', 'armor': 'none'},
    # 3
    {'weight': 6, 'hits': (1, 2), 'wounds': '-1D',
     'weapons': 'hooves and teeth', 'armor': 'none'},
    # 4
    {'weight': 12, 'hits': (2, 2), 'wounds': '',
     'weapons': 'hooves', 'armor': 'jack'},
    # 5
    {'weight': 25, 'hits': (3, 2), 'wounds': '',
     'weapons': 'horns and teeth', 'armor': 'none'},
    # 6
    {'weight': 50, 'hits': (4, 2), 'wounds': '',
     'weapons': 'thrasher', 'armor': 'none'},
    # 7
    {'weight': 100, 'hits': (5, 2), 'wounds': '',
     'weapons': 'claws and teeth', 'armor': 'none'},
    # 8
    {'weight': 200, 'hits': (5, 3), 'wounds': '+1D',
     'weapons': 'teeth', 'armor': 'none'},
    # 9
    {'weight': 400, 'hits': (6, 3), 'wounds': '+2D',
     'weapons': 'claws', 'armor': 'none'},
    # 10
    {'weight': 800, 'hits': (7, 3), 'wounds': '+3D',
     'weapons': 'claws', 'armor': 'jack'},
    # 11
    {'weight': 1600, 'hits': (8, 3), 'wounds': '+4D',
     'weapons': 'thrasher', 'armor': 'none'},
    # 12
    {'weight': 3200, 'hits': (8, 4), 'wounds': '+5D',
     'weapons': 'claws and teeth', 'armor': '+6'},
    # 13
    {'weight': '+6', 'hits': '+6', 'wounds': '+6',
     'weapons': '+6', 'armor': '+6'},
    # 14
    {'weight': 6000, 'hits': (9, 4), 'wounds': 'x2',
     'weapons': 'stinger', 'armor': 'cloth+1'},
    # 15
    {'weight': 12000, 'hits': (10, 5), 'wounds': 'x2',
     'weapons': 'claws+1 and teeth+1', 'armor': 'mesh'},
    # 16
    {'weight': 24000, 'hits': (12, 6), 'wounds': 'x3',
     'weapons': 'teeth+1', 'armor': 'cloth'},
    # 17
    {'weight': 30000, 'hits': (14, 7), 'wounds': 'x4',
     'weapons': 'as blade', 'armor': 'battle+4'},
    # 18
    {'weight': 36000, 'hits': (15, 7), 'wounds': 'x4',
     'weapons': 'as pike', 'armor': 'reflec'},
    # 19
    {'weight': 40000, 'hits': (16, 8), 'wounds': 'x5',
     'weapons': 'as broadsword', 'armor': 'ablat'},
    # 20
    {'weight': 44000, 'hits': (17, 9), 'wounds': 'x6',
     'weapons': 'as body pistol', 'armor': 'battle'}
]

# WEAPONS_TABLE: {'weapon': D6, ...}
WEAPONS_TABLE = {
    'hands': 1, 'claws': 1, 'teeth': 2, 'horns': 2,
    'hooves': 2, 'stinger': 3, 'thrasher': 2, 'club': 2,
    'as blade': 2, 'as pike': 3, 'as broadsword': 4,
    'as body pistol': 3,
    'hooves and horns': 2, 'hooves and teeth': 2,
    'claws and teeth': 2, 'horns and teeth': 2
}

# SUPERTYPE_DM_TABLE: {'supertype': {'weaponry': DM, 'armor': DM}, ...}
SUPERTYPE_DM_TABLE = {
    'Carnivore': {'weaponry': +8, 'armor': -1},
    'Omnivore': {'weaponry': +4, 'armor': 0},
    'Herbivore': {'weaponry': -3, 'armor': +2},
    'Scavenger': {'weaponry': 0, 'armor': +1}
}
