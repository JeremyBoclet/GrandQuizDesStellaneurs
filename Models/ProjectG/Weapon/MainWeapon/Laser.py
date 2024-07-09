import pygame

from Models.ProjectG.Weapon.Projectile.LaserProjectile import LaserProjectile
from Models.ProjectG.Weapon.MainWeapon.Weapon import Weapon


class Laser(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Laser"
        self.current_length = 0
        self.damage = 10
        self.max_length = 200
        self.growth_rate = 3
        self.width = 10
        self.image = pygame.Surface((self.current_length, self.width), pygame.SRCALPHA)
        self.original_image = self.image
        self.delete_on_hit = False
        self.cooldown = 2000
        self.max_projectile = 1
        self.rotation_speed = 0.05
        self.max_turn = 0
        self.next_upgrade = "Un laser grandit vers l'ennemi le plus proche"
        self.ico = self.image

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if (now - self.last_fire >= self.cooldown and len(self.projectile) < self.max_projectile) or self.last_fire == 0:
                self.last_fire = pygame.time.get_ticks()
                self.projectile.add(
                    LaserProjectile(player.rect.centerx, player.rect.centery, enemy, self, player))

    def update(self, player, enemy):
        self.fire(player, enemy)

        self.projectile.update()

    def set_new_level_attribute(self):
        match self.current_level:
            case 2:
                self.cooldown -= 200
            case 3:
                self.growth_rate += 2
            case 4:
                self.damage += 5
            case 5:
                self.max_turn = 4
                self.cooldown = 1000
            case 6:
                self.max_turn += 1
                self.cooldown = 600
                self.rotation_speed *= 2

    def set_next_upgrade(self):
        match self.current_level:
            case 1:
                self.next_upgrade = ("Réduit le cooldown")
            case 2:
                self.next_upgrade = ("Augmente la vitesse")
            case 3:
                self.next_upgrade = "Augmente les dégats"
            case 4:
                self.next_upgrade = ("Le laser tourne désormait autour du joueur /n"
                                     "Augmente le cooldown")
            case 5:
                self.next_upgrade = ("Le laser tourne un tour de plus /n"
                                     "Réduit le cooldown /n"
                                     "Augmente la vitesse de rotation")