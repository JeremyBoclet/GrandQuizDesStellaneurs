import pygame

from Models.ProjectG.Weapon.Projectile.BombProjectile import BombProjectile
from Models.ProjectG.Weapon.MainWeapon.Weapon import Weapon

WIDTH = 1980
HEIGHT = 1080


class Bomb(Weapon):
    def __init__(self):
        super().__init__()

        self.name = "Bomb"
        self.delete_on_hit = False
        self.damage_on_hit = False
        self.size = (60, 60)
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/bomb.png").convert_alpha(),
                                            self.size)
        self.rect = self.image.get_rect()

        self.original_image = self.image.copy()

        # Indicateur de position cible
        self.target_indicator_image = pygame.transform.scale(
            pygame.image.load("../Assets/ProjectG/cible.png").convert_alpha(),
            self.size)

        self.target_indicator_rect = self.target_indicator_image.get_rect()

        self.detonation_animation_image_path = [f'..\Assets\ProjectG\Animation\\bomb_{i}.png' for i in range(1, 9)]
        self.explosion_animation_image_path = [f'..\Assets\ProjectG\Animation\\explosion_bomb_{i}.png' for i in
                                               range(1, 57)]
        self.ico = self.image.copy()
        self.show_image = False
        self.cooldown = 2000
        self.travel_time = 2.0  # Durée de trajet en secondes
        self.explosion_radius = 100
        self.explosion_delay = 2
        self.damage = 20
        self.next_upgrade = "Lance une bombe qui explose après un court moment"
        self.max_level = 2
    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if (now - self.last_fire >= self.cooldown or self.last_fire == 0) and len(self.projectile) == 0:
                self.last_fire = 9999999
                for i in range(0, self.max_projectile):
                    self.projectile.add(
                        BombProjectile(player, self))

    def update(self, player, enemy):
        self.fire(player, enemy)
        self.projectile.update()

    def set_new_level_attribute(self):
        match self.current_level:
            case 2:
                self.explosion_radius += 20
            case 3:
                self.cooldown -= 500
                self.explosion_radius += 20

            case 4:
                self.cooldown -= 500
                self.travel_time -= 1
            case 5:
                self.explosion_radius += 50
                self.damage += 20
            case 6:
                self.explosion_delay -= 1
                self.damage += 20

    def set_next_upgrade(self):
        match self.current_level:
            case 1:
                self.next_upgrade = ("Augmente la taille de l'explosion")
            case 2:
                self.next_upgrade = ("Augmente la taille de l'explosion /n"
                                     "Réduit le temps de recharge")
            case 3:
                self.next_upgrade = ("Augmente la vitesse de pose de la bombe /n"
                                     "Réduit le temps de recharge")
            case 4:
                self.next_upgrade = ("Augmente la taille de l'explosion /n"
                                     "Augmente les dégats")
            case 5:
                self.next_upgrade = ("Réduit le temps d'explosion /n"
                                     "Augmente les dégats%")
