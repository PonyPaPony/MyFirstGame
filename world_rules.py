from camps import Camps

class WorldRules:
    def __init__(self, world_time):
        self.world_time = world_time
        self.last_day = self.world_time.get_day()

        self.camps = []

    def update_day(self):
        current_day = self.world_time.get_day()

        if current_day != self.last_day:
            self.last_day = current_day
            self.mark_camps_for_respawn()

    def add_camp(self):
        camp = Camps(self.world_time)
        self.camps.append(camp)
        return camp

    def update_camps(self):
        for camp in self.camps:
            if self.cleared_camps(camp):
                continue

            self.global_cleared_camps(camp)

    @staticmethod
    def cleared_camps(camp):
        if not camp.is_cleared():
            return False

        camp.global_respawn_pending = False

        if camp.respawn_at is None:
            camp.set_respawn_time()

        if camp.can_respawn():
            camp.respawn()

        return True

    @staticmethod
    def global_cleared_camps(camp):
        if camp.global_respawn_pending and not camp.is_fight():
            camp.respawn()
            camp.global_respawn_pending = False


    def mark_camps_for_respawn(self):
        for camp in self.camps:
            camp.global_respawn_pending = True

    def update(self):
        self.update_day()
        self.update_camps()