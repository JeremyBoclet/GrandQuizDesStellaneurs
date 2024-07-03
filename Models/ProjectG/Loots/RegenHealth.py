import pygame.sprite


class RegenHealth(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/health_potion.png").convert_alpha(),
                                            (40, 40))
        self.health_regen = 50
        self.rect = self.image.get_rect()
