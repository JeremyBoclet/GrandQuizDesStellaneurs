import math
import time
import random
import pygame
import copy

from Models.ProjectG.Enemies.Blob import Blob
from Models.ProjectG.Menu import Options
from Models.ProjectG.Menu.InventoryDisplay import InventoryDisplay
from Models.ProjectG.Menu.LevelUpMenu import LevelUpMenu
from Models.ProjectG.ProjectGPlayer import ProjectGPlayer
from Models.ProjectG.Weapon.Bomb import Bomb
from Models.ProjectG.Weapon.FallingStar import FallingStar
from Models.ProjectG.Weapon.Lightning import Lightning
from Models.ProjectG.Weapon.Projectile.BombProjectile import BombProjectile
from Models.ProjectG.Weapon.Projectile.FallingStarProjectile import FallingStarProjectile
from Models.ProjectG.Weapon.Projectile.LightningProjectile import LightningProjectile
from Models.ProjectG.Menu.Options import Options
from Models.ProjectG.Weapon.Saw import Saw
from Models.ProjectG.Weapon.Scythe import Scythe
from Models.ProjectG.Weapon.Weapon import Weapon
from Models.ProjectG.Weapon.magic_staff import magic_staff

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
                                                 (5000, 5000))



        self.all_enemies = pygame.sprite.Group()

        self.all_loots = pygame.sprite.Group()
        self.all_animation_sprite = pygame.sprite.Group()

        # Chronomètre pour l'apparition des ennemis
        self.enemy_spawn_time = 0
        self.enemy_spawn_interval = 0.2  # Apparition d'un ennemi toutes les 3 secondes

        # Limite d'ennemis à l'écran
        self.MAX_ENEMIES = 1
        self.hit_enemies_set = set()

        self.pause = False
        self.level_up_menu = None

        self.player = ProjectGPlayer(self.screen)
        self.player.inventory.add_weapon(Lightning())

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)


        self.Options = Options(self.player.inventory.weapons)
        self.clock = pygame.time.Clock()

        self.InventoryDisplay = InventoryDisplay(self.screen, self.player.inventory)


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

        self.clock.tick(60)
        # print(f"fps : {self.clock.get_fps()}")

        for event in pygame.event.get():
            if self.pause:
                choice = self.level_up_menu.handle_event(event)
                if choice and choice.attribute == "weapon":
                    has_weapon = False
                    for weapon in self.player.inventory.weapons:
                        if weapon.name == choice.name:
                            has_weapon = True
                            weapon.level_up()
                            # Pour les tooltips
                            self.Options.set_next_upgrade(choice.name)
                            if not weapon.can_level_up():
                                self.Options.remove_option(choice.name)
                            break

                    if not has_weapon:
                        self.player.inventory.add_weapon(copy.copy(choice))
                        self.Options.set_next_upgrade(choice.name)

                    self.pause = False
                elif choice and choice.attribute == "loot":
                    choice.gain_loot(self.player)
                    self.pause = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.cancel_rect.collidepoint(event.pos):
                        pygame.quit()

        if self.pause:
            self.level_up_menu.draw()
        else:
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
            self.player.attract_loots(self.all_loots)

            loots = pygame.sprite.spritecollide(self.player, self.all_loots, True)
            for loot in loots:
                player_level = self.player.level
                loot.gain_loot(self.player)
                if player_level < self.player.level:
                    options = random.sample(self.Options.option_available, min(3, len(self.Options.option_available)))
                    self.level_up_menu = LevelUpMenu(self.screen, options)
                    self.pause = True

            # Collision projectile / ennemies
            for weapon in self.player.inventory.weapons:
                collision = pygame.sprite.groupcollide(weapon.projectile, self.all_enemies, weapon.delete_on_hit, False)
                for projectile, hit_enemies in collision.items():
                    # self.hit_enemies_set.clear()
                    for enemy in hit_enemies:
                        if projectile.can_damage(enemy) and weapon.damage_on_hit:
                            enemy.take_damage(weapon.damage)
                            projectile.mark_enemy_hit(enemy)
                            self.hit_enemies_set.add(enemy)  # Ajouter l'ennemi touché à l'ensemble
                            if isinstance(projectile, LightningProjectile):
                                projectile.trigger_electric_animation(enemy.rect.center, self.all_animation_sprite)
                                projectile.bounce(self.all_enemies)

                        # permet de reset le hit si le projectile sort de la collision ennemi
                        for not_hit_enemies in self.all_enemies:
                            if not_hit_enemies not in hit_enemies:
                                projectile.clear_enemy_hit(not_hit_enemies)

                for projectile in weapon.projectile:
                    # Cas bombe
                    if isinstance(projectile, BombProjectile):
                        projectile.draw(self.screen)
                        if projectile.explosion_started:
                            projectile.trigger_detonation_animation(projectile.end_position,self.all_animation_sprite)
                        if projectile.is_exploding:
                            projectile.explode(self.all_enemies)
                            projectile.trigger_explosion_animation(projectile.end_position,self.all_animation_sprite)
                    if isinstance(projectile,FallingStarProjectile):
                        # Cas étoile filante
                        if not projectile.falling:
                            projectile.explode_damage(self.all_enemies)
                            projectile.trigger_animation(projectile.position, self.all_animation_sprite)
                        projectile.inflict_persistent_damage(self.all_enemies)
                        projectile.draw(self.screen)

            all_enemies_set = set(self.all_enemies)
            # Obtenir la liste des ennemis non touchés
            non_hit_enemies = list(all_enemies_set - self.hit_enemies_set)
            for enemy in non_hit_enemies:
                enemy.is_targeted = False

            for enemy in self.all_enemies:
                if isinstance(enemy,Blob):
                    if pygame.sprite.collide_rect(enemy, self.player):
                        self.player.take_damage(enemy.damage)

            #************************************************************
            #*************************** DRAW ***************************
            #************************************************************
            self.screen.fill('#71ddee')
            self.screen.blit(self.background, (self.player.background_x, self.player.background_y))

            move_all_sprite = self.all_loots.copy()
            move_all_sprite.add(self.all_enemies.copy())
            move_all_sprite.add(self.all_animation_sprite.copy())

            self.player.additional_update(move_all_sprite)

            # Inventaire
            self.InventoryDisplay.draw_inventory()

            # xp
            self.all_loots.update()
            self.all_loots.draw(self.screen)

            # Animation
            self.all_animation_sprite.update()
            self.all_animation_sprite.draw(self.screen)

            # enemies
            self.all_enemies.update(self.all_enemies)
            self.all_enemies.draw(self.screen)

            # sprite
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)

            self.player.draw_health_bar(self.screen)

            for enemy in self.all_enemies:
                enemy.draw_health_bar(self.screen)
                if enemy.health <= 0:
                    # Loot + kill ennemi
                    loot = enemy.spawn_loots()
                    if loot is not None:
                        self.all_loots.add(loot)
                        self.all_sprites.add(loot)
                    self.all_enemies.remove(enemy)

            self.player.draw_experience_bar(self.screen)

            # Bouton annuler
            self.screen.blit(self.cancel_image,
                             (20, self.screen.get_height() - self.cancel_image.get_height()))

            self.cancel_rect = pygame.Rect(20, self.screen.get_height() - self.cancel_image.get_height(), 200, 65)

