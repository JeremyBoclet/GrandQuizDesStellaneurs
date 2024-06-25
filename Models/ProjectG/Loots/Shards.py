import pygame.sprite


class Shards(pygame.sprite.Sprite):
    def __init__(self, x, y, image, experience_gain):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/{}.png".format(image)).convert_alpha(),
                                            (20, 30))
        self.experience_gain = experience_gain
        self.rect = self.image.get_rect(center=(x, y))

