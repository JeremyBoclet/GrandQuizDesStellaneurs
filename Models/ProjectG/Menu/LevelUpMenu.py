import pygame


class LevelUpMenu:
    def __init__(self, screen, options):
        self.screen = screen
        self.options = options
        self.selected_option = 0
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            text = self.font.render(option.name, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + i * 70))
            self.screen.blit(text, rect)

            # Afficher l'image de l'arme
            image_rect = option.image.get_rect(
                center=(self.screen.get_width() // 2 - 70, self.screen.get_height() // 2 + i * 70))
            self.screen.blit(option.image, image_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None
