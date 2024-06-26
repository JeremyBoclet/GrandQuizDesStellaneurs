import math

from Models.ProjectG.Weapon.Projectile.Projectile import Projectile


class Projectile_Scythe(Projectile):
    def __init__(self, weapon, player, initial_angle):
        super().__init__(0, 0, 0, 0, weapon, player, delete_outside_screen=False)
        self.dx = 100
        self.dy = 100
        self.angle = initial_angle
        self.player = player

    def update(self):
        # Calculer la position orbitale
        self.angle += self.weapon.speed
        if self.angle >= 360:
            self.angle -= 360
            self.hit_enemies = []

        self.rotation()

        rad_angle = math.radians(self.angle)
        self.rect.centerx = self.player.rect.centerx + self.weapon.radius * math.cos(rad_angle)
        self.rect.centery = self.player.rect.centery + self.weapon.radius * math.sin(rad_angle)

