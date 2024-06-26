import pygame


class ElectricAnimation(pygame.sprite.Sprite):
    def __init__(self, position, image_paths, frame_duration=5):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(path).convert_alpha(),(70,70)) for path in image_paths]
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.frame_counter = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_duration:
            self.frame_counter = 0
            self.current_frame += 1
            if self.current_frame >= len(self.images):
                self.kill()  # Remove the sprite when the animation ends
            else:
                self.image = self.images[self.current_frame]