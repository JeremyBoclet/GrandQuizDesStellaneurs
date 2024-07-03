import pygame

from Models.ProjectG.Weapon.Projectile.LightningProjectile import LightningProjectile
from Models.ProjectG.Weapon.Weapon import Weapon


class Lightning(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Eclair"

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(100, 100))

        self.original_image = self.image

        self.damage = 10
        self.speed = 10
        self.max_projectile = 1
        self.cooldown = 5000
        self.delete_on_hit = False
        self.max_bounce = 3

        self.wait_for_new_target = False

        self.animation_image_path = [f'..\Assets\ProjectG\Animation\\new_lightning_{i}.png' for i in range(1, 7)]
        self.ico = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/lightning.png").convert_alpha(),
                                          (45, 60))
        self.next_upgrade = "Un arc éléctrique transpercant les ennemis"

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if now - self.last_fire >= self.cooldown and len(self.projectile) < self.max_projectile:
                self.last_fire = 9999999 #Permet de déclencher le cooldown au kill du projectile
                self.projectile.add(
                    LightningProjectile(player.rect.centerx, player.rect.centery, enemy, self, self.max_bounce))
        else:
            self.projectile.empty()

    def update(self, player, enemy):
        self.fire(player, enemy)

        self.projectile.update()

        # check si l'ennemi est mort pour rerouter le projectile
        for projectile in self.projectile:
            if self.wait_for_new_target:
                projectile.reroute(enemy)
                self.wait_for_new_target = False

            if enemy.health <= 0 or projectile.target.health <= 0:
                self.wait_for_new_target = True

    def set_new_level_attribute(self):
        match self.current_level:
            case 2:
                self.speed += 3
            case 3:
                self.damage += 2
                self.cooldown = 700
            case 4:
                self.max_bounce += 2
            case 5:
                self.max_bounce += 2
                self.cooldown = 500
            case 6:
                self.max_bounce += 2
                self.damage += 3

    def set_next_upgrade(self):
        match self.current_level:
            case 1:
                self.next_upgrade = self.configuration.upgrades["PROJECTILE_SPEED_INCREASED"] + "/n"
            case 2:
                self.next_upgrade = (self.configuration.upgrades["DAMAGE_INCREASED"] + "/n" +
                                     self.configuration.upgrades["REDUCE_COOLDOWN"])
            case 3:
                self.next_upgrade = self.configuration.upgrades["BOUNCE_INCREASED"].format("2")
            case 4:
                self.next_upgrade = (self.configuration.upgrades["BOUNCE_INCREASED"].format("2") + "/n" +
                                     self.configuration.upgrades["REDUCE_COOLDOWN"])
            case 5:
                self.next_upgrade = (self.configuration.upgrades["BOUNCE_INCREASED"].format("2") + "/n" +
                                     self.configuration.upgrades["DAMAGE_INCREASED"].format("1") + "/n")
