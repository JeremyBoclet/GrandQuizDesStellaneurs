class Weapon():
    def __init__(self):
        self.name = "ARME"

        self.max_range = 10000
        self.delete_on_hit = True
        self.speed = 1
        self.damage = 1
        self.cooldown = 1
        self.last_fire = 0
        self.rotation_speed = 0
        self.max_bounce = 0
        self.current_level = 1
        self.max_level = 6

    def level_up(self):
        if self.can_level_up:
            self.current_level += 1
            self.set_new_level_attribute()

    def set_new_level_attribute(self):
        print("ajuster les niveaux de l'arme")

    def can_level_up(self):
        return self.current_level < self.max_level
