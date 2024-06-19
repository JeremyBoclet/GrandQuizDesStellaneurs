from pygame import *

import pygame

from Models.ProjectG.Inventory import Inventory
from Models.ProjectG.Weapon.magic_staff import magic_staff


class ProjectGPlayer(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.pos = [200, 200]
        self.image = pygame.image.load("../Assets/ProjectG/Mage.png")
        self.image = pygame.transform.scale(self.image, (48, 54)).convert_alpha()

        self.sprite_left = pygame.transform.flip(self.image, True, False)
        self.sprite_right = self.image

        self.rect = self.image.get_rect(center=(200, 200))
        self.speed = 7

        self.last_fire = 0

        self.inventory = Inventory(self,screen)

    def movement(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT]:
            self.pos[0] -= self.speed
            self.image = self.sprite_left
        if key_pressed[K_RIGHT]:
            self.pos[0] += self.speed
            self.image = self.sprite_right
        if key_pressed[K_UP]:
            self.pos[1] -= self.speed
        if key_pressed[K_DOWN]:
            self.pos[1] += self.speed

        # check pour ne pas sortir de l'écran
        if self.pos[0] <= 0:
            self.pos[0] = 0
        if self.pos[0] >= self.screen.get_width() - 48:
            self.pos[0] = self.screen.get_width() - 48
        if self.pos[1] <= 0:
            self.pos[1] = 0
        if self.pos[1] >= self.screen.get_height() - 54:
            self.pos[1] = self.screen.get_height() - 54

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def update(self):
        self.movement()
        self.inventory.update()


        # for bullet in self.weapon_bullet:
        #    bullet.fire()
        #    self.screen.blit(bullet.sprite, bullet.sprite_rect)
