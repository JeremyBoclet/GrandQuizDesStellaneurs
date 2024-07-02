import math

from Models.ProjectG.Weapon.Projectile.Projectile import Projectile

WIDTH = 1920
HEIGHT = 1080


class FireBall(Projectile):
    def __init__(self, x, y, target, weapon, player):
        super().__init__(x, y, target.rect.centerx, target.rect.centery, weapon, player, delete_outside_screen=True)
        self.x = x
        self.y = y

    def update(self):
        # Vérifier si le projectile sort de l'écran
        if ((self.rect.right < 0 or self.rect.left > WIDTH or
             self.rect.bottom < 0 or self.rect.top > HEIGHT)) and self.delete_outside_screen and not self.can_bounce:
            self.kill()

        self.rect.x += self.dx
        self.rect.y += self.dy

        if len(self.hit_enemies) == self.weapon.max_enemy_hit:
            self.kill()