import pygame

from config import BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P, images
from scripts.textandbuttons import Text, Button


class BuildHouseMenu:
    def __init__(self, x, y, width, height, display, display_x, display_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display = display
        self.display_x = display_x
        self.display_y = display_y

        self.bg = pygame.Rect(self.x, self.y, self.width, self.height)

        self.scroll_buttons = [Button(652, 402, 25, 16, BUTTON_COL, BUTTON_COL_H,
                               BUTTON_COL_P, 14, lambda: print("hello"), self.display, '^'),
                               Button(652, 428, 25, 16, BUTTON_COL, BUTTON_COL_H,
                               BUTTON_COL_P, 14, lambda: print("hello"), self.display, 'v')]
        self.small_house_img = images['small_house_icon']

    def update(self, events):
        for event in events:
            for button in self.scroll_buttons:
                button.click(event)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        local_mouse_pos = (mouse_pos[0] - self.display_x, mouse_pos[1] - self.display_y)

        pygame.draw.rect(self.display, (116, 63, 57), self.bg)

        for button in self.scroll_buttons:
            button.check_inp(local_mouse_pos)
            button.draw()
