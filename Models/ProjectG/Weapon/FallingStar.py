import random

import pygame

from Models.ProjectG.Weapon.Projectile.FallingStarProjectile import FallingStarProjectile
from Models.ProjectG.Weapon.Weapon import Weapon

WIDTH = 1920
HEIGHT = 1080

class FallingStar(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "VoidBomb"
        self.image = pygame.image.load("../Assets/ProjectG/voidbomb.png")

        self.ico = pygame.transform.scale(self.image.copy().convert_alpha(),(60,60))

        self.image = pygame.transform.scale(self.image.convert_alpha(),(20,20))
        self.original_image = self.image.copy()

        self.rect = self.image.get_rect()
        self.cooldown = 1000
        self.speed = 7
        self.damage = 5
        self.delete_on_hit = False
        self.damage_on_hit = False
        self.show_image = False
        self.max_projectile = 1
        #self.animation_image_path = [f'..\Assets\ProjectG\Animation\\fallingstar\\fallingstar_{i}.png' for i in range(1, 57)]
        self.animation_image_path = [f'..\Assets\ProjectG\Animation\\voidbomb\\voidbomb_{i}.png' for i in range(1, 73)]
        self.explosion_radius = 80
        self.attraction_force = 2
        self.persistent_damage = 1
        self.persistent_duration = 2
        self.next_upgrade = "Une étoile tombe du ciel faisant des dégats à l'impact puis persiste pendant un certain temps sur le sol"
        self.rotation_speed = 0.5
        self.angle_rotation = 1

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if (now - self.last_fire >= self.cooldown or self.last_fire == 0) and len(self.projectile) < self.max_projectile:
                self.last_fire = pygame.time.get_ticks()
                for i in range(0, self.max_projectile):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    self.projectile.add(
                       FallingStarProjectile(x, y, self))

    def update(self, player, enemy):
        self.fire(player, enemy)
        self.projectile.update()

    def set_new_level_attribute(self):
        match self.current_level:
            case 2:
                self.speed += 5
                self.persistent_damage += 2
            case 3:
                self.damage += 5
                self.explosion_radius += 20
                self.max_projectile += 1
            case 4:
                self.cooldown -= 200
            case 5:
                self.explosion_radius += 20
                self.damage += 20
            case 6:
                self.max_projectile += 1

    def set_next_upgrade(self):
        match self.current_level:
            case 1:
                self.next_upgrade = ("Augmente la vitesse de chute de l'étoile /n Augmente les dégats au sol")
            case 2:
                self.next_upgrade = ("Augmente la taille de l'explosion /n"
                                     "Augmente le nombre de projectile /n"
                                     "Augmente les dégats à l'impact")
            case 3:
                self.next_upgrade = "Réduit le temps de recharge"
            case 4:
                self.next_upgrade = ("Augmente la taille de l'explosion /n"
                                     "Augmente les dégats")
            case 5:
                self.next_upgrade = ("Augmente le nombre de projectile")
