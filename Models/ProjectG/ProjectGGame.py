import math
import time
import random

import pygame

from Models.ProjectG.Enemies.Blob import Blob
from Models.ProjectG.ProjectGPlayer import ProjectGPlayer
from Models.ProjectG.Weapon.LightningProjectile import LightningProjectile

WIDTH = 1920
HEIGHT = 1080


class ProjectGGame:
    def __init__(self, screen):
        self.game_mode_id = 1400

        self.cancel_image = pygame.image.load("../Assets/Cancel.png")
        self.cancel_image = pygame.transform.scale(self.cancel_image,
                                                   (200, 65)).convert_alpha()
        self.cancel_rect = self.cancel_image.get_rect()

        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/background.png").convert_alpha(),
                                                 (screen.get_width(), screen.get_height()))

        self.player = ProjectGPlayer(self.screen)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.all_enemies = pygame.sprite.Group()

        #blob = Blob(20, 20, self.player)
        #self.all_enemies.add(blob)

        self.all_shards = pygame.sprite.Group()
        #self.player.inventory.set_enemy(blob)

        # Chronomètre pour l'apparition des ennemis
        self.enemy_spawn_time = 0
        self.enemy_spawn_interval = 2  # Apparition d'un ennemi toutes les 3 secondes

        # Limite d'ennemis à l'écran
        self.MAX_ENEMIES = 10
        self.hit_enemies_set = set()

    def generate_random_position(self):
        """Génère une position aléatoire pour les ennemis sans chevauchement."""
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            new_blob = Blob(x, y, self.player)
            if not pygame.sprite.spritecollideany(new_blob, self.all_enemies):
                return x, y

    def get_closest_enemy(self):
        closest_enemy = None
        min_distance = float('inf')  # Initialiser avec une grande valeur

        player_x, player_y = self.player.rect.center

        for enemy in self.all_enemies:
            enemy_x, enemy_y = enemy.rect.center
            distance = math.hypot(enemy_x - player_x, enemy_y - player_y)

            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def update(self):
        self.screen.blit(self.background, (0, 0))

        # Gestion de l'apparition des ennemis
        if time.time() - self.enemy_spawn_time > self.enemy_spawn_interval:
            if len(self.all_enemies) < self.MAX_ENEMIES:
                x, y = self.generate_random_position()
                new_blob = Blob(x, y, self.player)
                self.all_enemies.add(new_blob)
                self.enemy_spawn_time = time.time()

        # for enemy in self.all_enemies:
        #     enemy.is_targeted = False

        self.player.inventory.set_enemy(self.get_closest_enemy())

        # Collision joueur / shard
        shards = pygame.sprite.spritecollide(self.player, self.all_shards, True)
        for shard in shards:
            self.player.gain_experience(shard.experience_gain)

        # Collision projectile / ennemies
        for weapon in self.player.inventory.weapons:
            collision = pygame.sprite.groupcollide(weapon.projectile, self.all_enemies, weapon.delete_on_hit, False)
            for projectile, hit_enemies in collision.items():
                # self.hit_enemies_set.clear()
                for enemy in hit_enemies:
                    if projectile.can_damage(enemy):
                        enemy.take_damage(weapon.damage)
                        projectile.mark_enemy_hit(enemy)
                        self.hit_enemies_set.add(enemy)  # Ajouter l'ennemi touché à l'ensemble
                        if isinstance(projectile, LightningProjectile):
                            projectile.bounce(self.all_enemies)

        all_enemies_set = set(self.all_enemies)
        # Obtenir la liste des ennemis non touchés
        non_hit_enemies = list(all_enemies_set - self.hit_enemies_set)
        for enemy in non_hit_enemies:
            enemy.is_targeted = False

        # sprite
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)

        # enemies
        self.all_enemies.update(self.all_enemies)
        self.all_enemies.draw(self.screen)
        for enemy in self.all_enemies:
            enemy.draw_health_bar(self.screen)
            if enemy.health <= 0:
                self.all_shards.add(enemy.spawn_shard())
                self.all_enemies.remove(enemy)

        # xp
        self.all_shards.update()
        self.all_shards.draw(self.screen)

        self.player.draw_experience_bar(self.screen)

        # Bouton annuler
        self.screen.blit(self.cancel_image,
                         (20, self.screen.get_height() - self.cancel_image.get_height()))

        self.cancel_rect = pygame.Rect(20, self.screen.get_height() - self.cancel_image.get_height(), 200, 65)
