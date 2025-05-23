import random
import pygame

from Models.ProjectG.Weapon.Projectile.Projectile import Projectile
from Models.ProjectG.Weapon.MainWeapon.Weapon import Weapon

WIDTH = 1920
HEIGHT = 1080


class Star(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Etoiles"

        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/star.png").convert_alpha(),
                                            (45, 45))
        self.damage = 10
        self.max_bounce = 3
        self.cooldown = 4000
        self.speed = 7
        self.delete_on_hit = False
        self.rect = self.image.get_rect(center=(100, 100))
        self.angle = 0
        self.rotation_speed = 0
        self.original_image = self.image
        self.max_projectile = 1
        self.next_upgrade = "Créé une étoile qui rebondit sur les bords"
        self.ico = self.image

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if (now - self.last_fire >= self.cooldown or self.last_fire == 0) and len(self.projectile) == 0:

                for i in range(0, self.max_projectile):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    self.projectile.add(
                        Projectile(player.rect.centerx, player.rect.centery, x, y,
                                   self, player, can_bounce=True))

    def update(self, player, enemy):
        self.fire(player, enemy)
        self.projectile.update()

    def set_new_level_attribute(self):
        match self.current_level:
            case 2:
                self.max_projectile += 1
            case 3:
                self.speed += 1
                self.cooldown = 3000
            case 4:
                self.speed += 2
            case 5:
                self.max_bounce += 2
                self.cooldown = 1500
            case 6:
                self.max_bounce += 2
                self.max_projectile += 1
                self.damage += 5
                self.speed += 5

        self.projectile.empty()

    def set_next_upgrade(self):
        match self.current_level:
            case 2:
                self.next_upgrade = (self.configuration.upgrades["PROJECTILE_SPEED_INCREASED"] + "/n" +
                                     self.configuration.upgrades["REDUCE_COOLDOWN"])
            case 3:
                self.next_upgrade = self.configuration.upgrades["PROJECTILE_SPEED_INCREASED"]
            case 4:
                self.next_upgrade = (self.configuration.upgrades["BOUNCE_INCREASED"].format("2") + "/n" +
                                     self.configuration.upgrades["REDUCE_COOLDOWN"])
            case 5:
                self.next_upgrade = (self.configuration.upgrades["BOUNCE_INCREASED"].format("2") + "/n" +
                                     self.configuration.upgrades["ADD_PROJECTILE"].format("1") + "/n" +
                                     self.configuration.upgrades["DAMAGE_INCREASED"] + "/n" +
                                     self.configuration.upgrades["PROJECTILE_SPEED_INCREASED"])
