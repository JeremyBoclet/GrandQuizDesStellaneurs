import pygame
import random

from Models.ProjectG.ProjectGEnemy import Enemy


class Boss(Enemy):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Remplacez par l'image du boss si nécessaire
        self.image.fill((255, 0, 0))  # Remplacez par la couleur du boss
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.speed = 2
        self.is_aggro = False
        self.aggro_radius = 200
        self.attack_cooldown = 120  # Cooldown entre les attaques en frames
        self.attack_timer = 0
        self.player = player
        self.health = 1000
        self.base_health = 1000
        self.charge_distance = 500  # Distance maximale de charge
        self.charge_speed = 10 # Vitesse de charge
        self.charge_direction = None
        self.charge_target = None  # Position cible de la charge (derrière le joueur)
        self.max_charge_duration = 60  # Durée maximale de la charge en frames
        self.charge_duration = 0  # Durée actuelle de la charge en frames

        # Charger l'image de la destination
        self.charge_destination_image =  pygame.transform.scale(
            pygame.image.load("../Assets/ProjectG/cible.png").convert_alpha(),
            (60,60))
        self.charge_destination_rect = self.charge_destination_image.get_rect()

        # Ajout d'un délai avant la charge
        self.charge_delay = 60  # Délai en frames avant la charge
        self.charge_delay_timer = 0
        self.is_charging = False
        self.arrow_color = (255, 0, 0)  # Couleur de la flèche

    def update(self, all_enemies):
        if not self.is_aggro:
            self.move_sideways()
            if self.detect_player():
                self.is_aggro = True
        else:
            self.attack_timer -= 1
            if self.attack_timer <= 0 and self.detect_player():
                self.attack()
                self.attack_timer = self.attack_cooldown

            if self.charge_delay_timer > 0:
                self.charge_delay_timer -= 1
                if self.charge_delay_timer == 0:
                    self.is_charging = True
                    self.charge_duration = self.max_charge_duration

            if self.is_charging and self.charge_duration > 0:
                self.update_charge()

    def move_sideways(self):
        self.rect.x += self.speed
        if self.rect.right > 1980 or self.rect.left < 0:
            self.speed = -self.speed
            self.rect.x += self.speed

    def detect_player(self):
        # Vérifie si le joueur est à portée d'aggro
        distance_to_player = ((self.rect.centerx - self.player.rect.centerx) ** 2 +
                              (self.rect.centery - self.player.rect.centery) ** 2) ** 0.5
        return distance_to_player < self.aggro_radius

    def calculate_behind_player(self):
        # Calculer la position derrière le joueur
        direction_to_player = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)
        direction_to_player.normalize()
        distance_behind = -1.1  # Distance derrière le joueur (à ajuster selon vos besoins)
        charge_position = pygame.math.Vector2(self.player.rect.center) - direction_to_player * distance_behind
        return charge_position

    def attack(self):
        # Choix aléatoire entre charge et saut
        attack_choice = random.choice(["charge"])
        if attack_choice == "charge":
            self.charge_attack()
        elif attack_choice == "jump":
            self.jump_attack()

    def charge_attack(self):
        # Définir la direction de la charge (vers le joueur ou une direction prédéterminée)
        self.charge_target = self.calculate_behind_player()
        self.charge_direction = (
                    pygame.math.Vector2(self.charge_target) - pygame.math.Vector2(self.rect.center)).normalize()
        self.charge_delay_timer = self.charge_delay
        self.charge_destination_rect.center = self.charge_target

    def update_charge(self):
        if self.charge_duration > 0:
            self.rect.center += self.charge_direction * self.charge_speed
            self.charge_duration -= 1
            if self.charge_duration <= 0:
                self.is_charging = False
                self.charge_target = None

    def draw_arrow(self, screen):
        if self.charge_delay_timer > 0:
            start_pos = self.rect.center
            end_pos = self.charge_target
            progress = 1 - self.charge_delay_timer / self.charge_delay
            current_end_pos = (pygame.math.Vector2(start_pos) + (
                        pygame.math.Vector2(end_pos) - pygame.math.Vector2(start_pos)) * progress).xy
            pygame.draw.line(screen, self.arrow_color, start_pos, current_end_pos, 5)
            arrow_head_size = 10
            arrow_direction = (pygame.math.Vector2(end_pos) - pygame.math.Vector2(start_pos)).normalize()
            perpendicular_direction = pygame.math.Vector2(-arrow_direction.y, arrow_direction.x)
            left_arrow_head = current_end_pos - arrow_direction * arrow_head_size + perpendicular_direction * arrow_head_size
            right_arrow_head = current_end_pos - arrow_direction * arrow_head_size - perpendicular_direction * arrow_head_size
            pygame.draw.polygon(screen, self.arrow_color, [current_end_pos, left_arrow_head, right_arrow_head])

    def jump_attack(self):
        # Implémentez la logique de l'attaque de saut
        pass  # À remplir avec la logique appropriée