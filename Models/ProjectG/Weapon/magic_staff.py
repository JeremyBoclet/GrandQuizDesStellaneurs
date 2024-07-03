import pygame

from Models.ProjectG.Weapon.Projectile.FireBall import FireBall
from Models.ProjectG.Weapon.Weapon import Weapon


class magic_staff(Weapon):
    def __init__(self):
        pygame.sprite.Sprite().__init__()
        super().__init__()
        self.name = "Bâton"
        self.next_upgrade = "Projecte une boule de feu vers l'ennemi le plus proche"

        self.speed = 10
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/fireball.png").convert_alpha(),
                                            (60, 60))
        self.damage = 10
        self.rect = self.image.get_rect(center=(100, 100))
        self.cooldown = 1500
        self.delete_on_hit = False
        self.max_enemy_hit = 1
        self.ico = self.image

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if now - self.last_fire >= self.cooldown:
                self.last_fire = pygame.time.get_ticks()
                self.projectile.add(FireBall(player.rect.centerx, player.rect.centery, enemy, self, player))

    def update(self, player, enemy):
        self.fire(player, enemy)
        self.projectile.update()

    def set_new_level_attribute(self):
        match self.current_level:
            case 2:
                self.max_enemy_hit += 1
            case 3:
                self.speed += 1.2
                self.max_enemy_hit += 1
            case 4:
                self.speed += 1.2
            case 5:
                self.cooldown = 1000
            case 6:
                self.max_enemy_hit += 1
                self.damage += 5

    def set_next_upgrade(self):
        match self.current_level:
            case 1:
                    self.next_upgrade = ("Le projectile traverse un ennemi de plus")
            case 2:
                self.next_upgrade = ("Le projectile traverse un ennemi de plus /n"
                                     "Augmente la vitesse de 20%")
            case 3:
                self.next_upgrade = "Augmente la vitesse de 20%"
            case 4:
                self.next_upgrade = ("Réduit le cooldown de à 1 seconde")
            case 5:
                self.next_upgrade = ("Le projectile traverse un ennemi de plus /n"
                                     "Augmente les dégats de 50%")
