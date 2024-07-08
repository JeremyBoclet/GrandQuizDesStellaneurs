import pygame


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Limiter le défilement à la taille de la carte
        x = min(0, x)  # Ne pas dépasser le bord gauche
        y = min(0, y)  # Ne pas dépasser le bord supérieur
        x = max(-(self.camera.width - self.width), x)  # Ne pas dépasser le bord droit
        y = max(-(self.camera.height - self.height), y)  # Ne pas dépasser le bord inférieur

        self.camera = pygame.Rect(x, y, self.width, self.height)

        # Debugging output
        print(f"camera width = {self.camera.width}, self width={self.width}")
        print(f"Camera coordinates: x={x}, y={y}")
