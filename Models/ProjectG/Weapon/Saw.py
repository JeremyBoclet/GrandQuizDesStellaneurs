import pygame.sprite

from Models.ProjectG.Weapon.Projectile.Projectile import Projectile
from Models.ProjectG.Weapon.Weapon import Weapon


class Saw(Weapon):
    def __init__(self):
        pygame.sprite.Sprite().__init__()
        super().__init__()
        self.name = "Scie"

        self.speed = 10
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/saw.png").convert_alpha(),
                                            (60, 60))
        self.damage = 2
        self.max_range = 300
        self.cooldown = 200
        self.delete_on_hit = False
        self.rect = self.image.get_rect(center=(100, 100))
        self.angle = 0
        self.rotation_speed = 0.2
        self.original_image = self.image
        self.next_upgrade = "Une scie visant l'ennemi le plus proche et revenant vers vous"
        self.ico = self.image

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if now - self.last_fire >= self.cooldown:
                self.last_fire = pygame.time.get_ticks()
                self.projectile.add(
                    Projectile(player.rect.centerx, player.rect.centery, enemy.rect.centerx, enemy.rect.centery,
                               self, player, can_return=True, delete_outside_screen=False))

    def update(self, player, enemy):
        self.fire(player, enemy)

        self.projectile.update()

    def set_new_level_attribute(self):
        match self.current_level:
            case 2:
                self.max_range += 100
            case 3:
                self.speed += 1.2
                self.max_range += 100

            case 4:
                self.speed += 1.2
            case 5:
                self.cooldown = 1000
            case 6:
                self.damage += 5

    def set_next_upgrade(self):
        match self.current_level:
            case 1:
                    self.next_upgrade = ("Range augmentée")
            case 2:
                self.next_upgrade = ("Range augmentée /n"
                                     "Augmente la vitesse")
            case 3:
                self.next_upgrade = "Augmente la vitesse"
            case 4:
                self.next_upgrade = ("Réduit le cooldown de à 1 seconde")
            case 5:
                self.next_upgrade = "Augmente les dégats%"
