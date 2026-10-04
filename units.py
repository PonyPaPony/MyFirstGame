class Units:
    def __init__(self):
        self.player = None
        self.enemies = []
        self.npc = []

    def get_all(self):
        return [self.player, *self.enemies, *self.npc]

    def add(self, entity, group):
        units_group = getattr(self, group)
        units_group.append(entity)

    def remove(self, entity, group):
        units_group = getattr(self, group)
        units_group.remove(entity)

    def set(self, entity, group):
        setattr(self, group, entity)