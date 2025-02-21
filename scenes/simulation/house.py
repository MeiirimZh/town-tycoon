import pygame
import json

from config import images


class House:
    def __init__(self, house_type, x, y):
        self.type = house_type
        self.x = x
        self.y = y
        if self.type == 'small_house':
            self.shadow_size = (100, 20)
        elif self.type == 'medium_house':
            self.shadow_size = (200, 20)
        elif self.type == 'large_house':
            self.shadow_size = (200, 20)
        elif self.type == 'school':
            self.shadow_size = (200, 20)
        elif self.type == 'guard_house':
            self.shadow_size = (200, 20)
        elif self.type == 'hospital':
            self.shadow_size = (200, 20)
        else:
            self.shadow_size = (0, 0)

        self.img = images[house_type]
        self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        self.shadow = pygame.Surface(self.shadow_size, pygame.SRCALPHA)
        self.shadow.fill((0, 0, 0, 128))

    def render(self, display, scroll):
        display.blit(self.shadow, (self.x + 8 + scroll[0], self.y + self.img.get_height() - 15 + scroll[1]))
        display.blit(self.img, (self.x + scroll[0], self.y + scroll[1]))


    def to_dict(self):
        return {"house_type": self.type, "x": self.x, "y": self.y}