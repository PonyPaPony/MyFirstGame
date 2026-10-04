import config
from spawner import spawn_creature
from combat import is_alive

class WorldSpawn:
    def __init__(self, units):
        self.units = units

        self.active_rect = None
        self.despawn_rect = None
        self.despawn_margin = config.MARGINS['despawn']
        self.active_margin = config.MARGINS['active']

        self.records = []

    @staticmethod
    def get_margin(camera, target):
        margin_x = round(camera.width * target)
        margin_y = round(camera.height * target)

        return margin_x, margin_y

    def spawn_player(self, entity_class, player_name, player_pos, **kwargs):
        player = spawn_creature(entity_class, player_name, player_pos, **kwargs)
        self.units.set(player, "player")
        return player

    def get_active_rect(self, camera_rect):
        self.active_rect = camera_rect.copy()

        margin_x, margin_y = self.get_margin(camera_rect, self.active_margin)

        self.active_rect.inflate_ip(margin_x * 2, margin_y * 2)

        return self.active_rect

    def get_despawn_rect(self, camera_rect):
        self.despawn_rect = camera_rect.copy()

        margin_x, margin_y = self.get_margin(camera_rect, self.despawn_margin)

        self.despawn_rect.inflate_ip(margin_x * 2, margin_y * 2)

        return self.despawn_rect

    def update(self, camera_rect):
        self.get_active_rect(camera_rect)
        self.get_despawn_rect(camera_rect)

        for record in self.records:
            if record.entity is None:
                if record.alive and self.is_active(record.pos):
                    self.activate_record(record)
            else:
                if not is_alive(record.entity.stats):
                    self.kill_record(record)

                elif self.should_despawn(record.entity.feet()):
                    self.deactivate_record(record)

    def is_active(self, pos):
        return self.active_rect.collidepoint(pos) if self.active_rect is not None else False

    def should_despawn(self, pos):
        return not self.despawn_rect.collidepoint(pos) if self.despawn_rect is not None else False

    def add_record(self, entity_class, name, pos, group, **kwargs):
        record = SpawnRecord(entity_class, name, pos, group, **kwargs)
        self.records.append(record)
        return record

    def remove_record(self, record):
        self.records.remove(record)

    def activate_record(self, record):
        if not record.alive:
            return None

        if record.entity is not None:
            return record.entity

        record.entity = spawn_creature(record.entity_class, record.name, record.pos, **record.kwargs)

        self.units.add(record.entity, record.group)

        return record.entity

    def deactivate_record(self, record):
        if record.entity is None:
            return

        self.units.remove(record.entity, record.group)
        record.entity = None

    def kill_record(self, record):
        if record.entity is None:
            return

        self.units.remove(record.entity, record.group)
        record.entity = None
        record.alive = False


class SpawnRecord:
    def __init__(self, entity_class, name, pos, group, **kwargs):
        self.entity_class = entity_class
        self.name = name
        self.pos = pos
        self.group = group
        self.kwargs = kwargs
        self.entity = None
        self.alive = True