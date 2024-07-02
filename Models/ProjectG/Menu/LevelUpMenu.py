import pygame


class LevelUpMenu:
    def __init__(self, screen, options):
        self.screen = screen
        self.options = options
        self.selected_option = 0
        self.font = pygame.font.Font(None, 36)

    def draw_rounded_rect(self, surface, rect, color, border_color, corner_radius, border_width):
        rect = pygame.Rect(rect)
        color = pygame.Color(*color)

        # Dessiner l'intérieur du rectangle
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

        # Dessiner la bordure du rectangle
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=corner_radius)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.option_rects = []
        screen_width, screen_height = self.screen.get_size()
        option_width = 600
        option_height = 1000
        padding = 20
        total_width = len(self.options) * (option_width + padding) - padding
        start_x = (screen_width - total_width) // 2
        y = screen_height // 2 - option_height // 2

        mouse_pos = pygame.mouse.get_pos()

        for i, option in enumerate(self.options):
            x = start_x + i * (option_width + padding)
            rect = pygame.Rect(x, y, option_width, option_height)
            self.option_rects.append(rect)

            if i == self.selected_option:
                border_color = (0, 255, 0)
            else:
                border_color = (100, 100, 100)

            self.draw_rounded_rect(self.screen, rect, (0, 0, 0, 150), border_color, 20, 10)

            # Afficher l'image de l'arme
            image_rect = option.image.get_rect(center=rect.center)
            self.screen.blit(option.image, image_rect)

            # Afficher le nom de l'arme
            text = self.font.render(option.name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(rect.centerx, rect.bottom - 20))
            self.screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(mouse_pos):
                    self.selected_option = i
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(mouse_pos):
                    return self.options[i]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_RIGHT:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]

        return None
