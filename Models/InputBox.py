import pygame


class InputBox:
    def __init__(self, x, y, w, h, number_only, size, text='', need_focus=True):
        self.need_focus = need_focus
        self.number_Only = number_only
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        self.FONT = pygame.font.SysFont("Futura-bold", size)

        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active or not self.need_focus:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    print("enter")
                else:
                    if self.number_Only and self.intTryParse(event.unicode) is not None:
                        self.text += event.unicode
                    elif not self.number_Only:
                        self.text += event.unicode

                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def intTryParse(self, value):
        try:
            return int(value), True
        except ValueError:
            return None

    def change_position(self,x,y,w,h):
        self.rect = pygame.Rect(x, y, w, h)