BASE_STATS = {
    'max_health': 100,
    'attack': 100,
    'defence': 100,
    'speed': 10,
    'attack_speed': 5,
    'dodge': 0,
    'accuracy': 100,
    'crit_chance': 5,
    'crit_dmg': 50,
}
LIMITS = {
    'crit_chance_limit': 75,
    'dodge_limit': 80,
    'accuracy_limit': 200,
    'speed_limit': 50,
}
STATE = {
    'current_health': 100,
}

def build_stats(custom_stats=None):
    if custom_stats is None:
        custom_stats = {}

    default_stats = {**BASE_STATS, **LIMITS, **STATE}
    stats = {**default_stats, **custom_stats}

    if 'max_health' in custom_stats and 'current_health' not in custom_stats:
        stats['current_health'] = stats['max_health']

    return stats