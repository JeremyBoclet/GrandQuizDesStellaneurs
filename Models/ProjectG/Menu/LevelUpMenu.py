import pygame


class LevelUpMenu:
    def __init__(self, screen, options):
        self.screen = screen
        self.options = options
        self.selected_option = 0
        self.font = pygame.font.Font(None, 36)
        self.background = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/background.png").convert_alpha(),
                                                 (screen.get_width(), screen.get_height()))
        self.option_rects = []

    def draw_rounded_rect(self, surface, rect, color, border_color, corner_radius, border_width):
        rect = pygame.Rect(rect)
        color = pygame.Color(*color)

        # Dessiner l'intérieur du rectangle
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

        # Dessiner la bordure du rectangle
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=corner_radius)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.option_rects = []
        screen_width, screen_height = self.screen.get_size()
        option_width = 600
        option_height = 1000
        padding = 20
        total_width = len(self.options) * (option_width + padding) - padding
        start_x = (screen_width - total_width) // 2
        y = screen_height // 2 - option_height // 2

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
            image_rect = option.image.get_rect(center=(rect.centerx, rect.centery - 100))
            self.screen.blit(option.ico, image_rect)

            # Afficher le tooltip de la prochaine upgrade
            tooltip_rect = pygame.Rect(rect.left, rect.bottom - 430, rect.width, 1)
            self.render_text_wrapped(option.next_upgrade, self.font, (255, 255, 255), tooltip_rect)

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

    def render_text_wrapped(self, text, font, color, rect, line_spacing=5):
        all_line = text.split('/n')
        lines = []

        for ligne in all_line:
            line = str.replace(ligne,'/n','')
            words = line.split(' ')
            current_line = []
            current_width = 0

            for word in words:
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if current_width + word_width >= rect.width:
                    lines.append((current_line, current_width))
                    current_line = [word]
                    current_width = word_width + font.size(' ')[0]  # Include space width
                else:
                    current_line.append(word)
                    current_width += word_width + font.size(' ')[0]

            if current_line:
                lines.append((current_line, current_width))

            y = rect.top
            for line, width in lines:
                line_surface = font.render(' '.join(line), True, color)
                self.screen.blit(line_surface, (rect.left + (rect.width - width) / 2, y))
                y += word_height + line_spacing
