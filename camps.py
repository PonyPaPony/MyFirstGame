import config

class Camps:
    def __init__(self, world_time):
        self.records = []

        self.world_time = world_time
        self.respawn_delay = config.RESPAWN_TIME['local']
        self.respawn_at = None
        self.global_respawn_pending = True

    def add_record(self, *records):
        self.records.extend(records)

    def is_cleared(self):
        return all(not record.alive for record in self.records)

    def set_respawn_time(self):
        if self.is_cleared():
            self.respawn_at = self.world_time.total_minutes + self.respawn_delay

    def can_respawn(self):
        if self.respawn_at is None:
            return False

        if self.is_fight():
            return False

        return self.respawn_at <= self.world_time.total_minutes

    def respawn(self):
        for record in self.records:
            record.alive = True

        self.respawn_at = None

    def is_fight(self):
        for record in self.records:
            if record.entity is None:
                continue

            if record.entity.state in ("chase", "comeback", "surround"):
                return True

        return False