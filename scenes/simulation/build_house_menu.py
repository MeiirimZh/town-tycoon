import pygame

from config import BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P, images
from scripts.textandbuttons import Text, Button


class BuildHouseMenu:
    def __init__(self, x, y, width, height, display):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display = display

        self.bg = pygame.Rect(self.x, self.y, self.width, self.height)

        self.up_btn = Button(652, 402, 25, 16, BUTTON_COL, BUTTON_COL_H,
                             BUTTON_COL_P, 14, 'a', self.display, '^')
        self.down_btn = Button(652, 428, 25, 16, BUTTON_COL, BUTTON_COL_H,
                               BUTTON_COL_P, 14, 'a', self.display, 'v')
        self.small_house_img = images['small_house_icon']

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(self.display, (116, 63, 57), self.bg)
        self.up_btn.draw()
        self.down_btn.draw()
