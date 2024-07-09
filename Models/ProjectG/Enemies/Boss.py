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
        self.charge_speed = 7 # Vitesse de charge
        self.charge_direction = None
        self.charge_target = None  # Position cible de la charge (derrière le joueur)
        self.max_charge_duration = 120  # Durée maximale de la charge en frames
        self.charge_duration = 0  # Durée actuelle de la charge en frames

    def update(self, all_enemies):
        if not self.is_aggro:
            self.move_sideways()
            if self.detect_player():
                self.is_aggro = True
        else:
            #self.move_towards(self.player)
            self.attack_timer -= 1
            if self.attack_timer <= 0 and self.detect_player():
                self.attack()
                self.attack_timer = self.attack_cooldown

        if self.charge_direction:
            self.charge()

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
        self.charge_direction = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(self.charge_target)
        if self.charge_direction.length() > 0:
            self.charge_direction.normalize()

    def charge(self):
        # Déplacer le boss dans la direction de la charge

        self.rect.x += self.charge_speed
        self.rect.y +=  self.charge_speed

        if self.rect.x == self.charge_direction.x:
            self.charge_direction = None

        # Vérifier si le boss a atteint la distance maximale de charge
        distance_traveled = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(
            (self.rect.x + self.rect.width) // 2, (self.rect.y + self.rect.height) // 2)

        # Incrémenter le compteur de durée de la charge
        # self.charge_duration += 1
        # # Vérifier si le temps de charge maximum est écoulé
        # if self.charge_duration >= self.max_charge_duration:
        #     self.charge_target = None  # Arrêter la charge
        print(distance_traveled.length())
        if distance_traveled.length() > self.charge_distance:
            print("stop charge")
            self.charge_direction = None  # Arrêter la charge

    def jump_attack(self):
        # Implémentez la logique de l'attaque de saut
        pass  # À remplir avec la logique appropriée
