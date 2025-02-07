import pygame
from config import images


class House:
    def __init__(self, house_type, x, y):
        self.type = house_type
        self.x = x
        self.y = y

        self.img = images[house_type]
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        self.shadow = pygame.Surface((100, 80), pygame.SRCALPHA)
        self.shadow.fill((0, 0, 0, 128))

    def render(self, display, scroll):
        display.blit(self.shadow, (self.x + 8 + scroll[0], self.y + 25 + scroll[1]))
        display.blit(self.img, (self.x + scroll[0], self.y + scroll[1]))
