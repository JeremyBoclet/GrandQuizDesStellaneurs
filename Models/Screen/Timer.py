import pygame

from Models.Events.TimerEventBar import TimerEventBar


class Timer:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 30)
        self.text = self.font.render(str(self.clock.get_fps()), True, (255, 255, 255))
        self.timer_event = TimerEventBar(self.screen, self)

    def render(self, time):
        self.text = self.font.render(str(time), True, (255, 255, 255))
        self.screen.blit(self.text, (self.screen.get_width() / 2, self.screen.get_height() - 30))
        # self.timer_event.update_bar(self.screen)
