import pygame


class InventoryDisplay:
    def __init__(self, screen, inventory):
        self.screen = screen
        self.inventory = inventory
        self.cell_size = 50
        self.padding = 5
        self.border_radius = 10
        self.border_color = (200, 200, 200)
        self.font = pygame.font.Font(None, 24)

    def draw_rounded_rect(self, surface, rect, color, border_radius):
        # Dessine un rectangle avec des coins arrondis
        pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    def draw_inventory(self):
        cols = 6
        start_x = 10
        start_y = 20

        for index, weapon in enumerate(self.inventory.weapons):
            row = index // cols
            col = index % cols
            x = start_x + col * (self.cell_size + self.padding)
            y = start_y + row * (self.cell_size + self.padding)
            rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

            # Draw the rounded rectangle
            self.draw_rounded_rect(self.screen, rect, (0, 0, 0), self.border_radius)
            pygame.draw.rect(self.screen, self.border_color, rect, width=2, border_radius=self.border_radius)

            # Draw the weapon image in the center of the cell
            if weapon.ico:
                image = pygame.transform.scale(weapon.ico,(40,40)).convert_alpha()
                image_rect = image.get_rect(center=rect.center)
                self.screen.blit(image, image_rect)
