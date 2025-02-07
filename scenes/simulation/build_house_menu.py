import pygame

from config import BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P, images
from scripts.textandbuttons import Text, Button


class BuildHouseMenu:
    def __init__(self, x, y, width, height, display, display_x, display_y, simulation):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display = display
        self.display_x = display_x
        self.display_y = display_y
        self.simulation = simulation

        self.bg = pygame.Rect(self.x, self.y, self.width, self.height)

        self.scroll_buttons = [Button(652, 402, 25, 16, BUTTON_COL, BUTTON_COL_H,
                               BUTTON_COL_P, 14, self.previous_tab, self.display, '^'),
                               Button(652, 428, 25, 16, BUTTON_COL, BUTTON_COL_H,
                               BUTTON_COL_P, 14, self.next_tab, self.display, 'v')]

        self.small_house_img = images['small_house_icon']
        self.small_house_title = Text(14, 'Small house', (255, 255, 255), (371, 154), self.display)
        self.small_house_resources = Text(12, '50 wood, 10 stone', (255, 255, 255), (371, 171), self.display)
        self.small_house_result = Text(12, '+10 dwellers', (255, 255, 255), (371, 186), self.display)
        self.small_house_button = Button(526, 168, 57, 22, BUTTON_COL, BUTTON_COL_H,
                                         BUTTON_COL_P, 14, lambda: self.build_house('small_house'),
                                         self.display, 'BUILD')

        self.tab = 1
        self.tabs = {1: self.first_tab, 2: self.second_tab}

    def run(self, events):
        mouse_pos = pygame.mouse.get_pos()
        local_mouse_pos = (mouse_pos[0] - self.display_x, mouse_pos[1] - self.display_y)

        pygame.draw.rect(self.display, (116, 63, 57), self.bg)

        tab_action = self.tabs[self.tab]
        tab_action(events, local_mouse_pos)

        for button in self.scroll_buttons:
            button.check_inp(local_mouse_pos)
            button.draw()

        for event in events:
            for button in self.scroll_buttons:
                button.click_on_mouse_pos(event, local_mouse_pos)

    def next_tab(self):
        self.tab = min(2, self.tab + 1)

    def previous_tab(self):
        self.tab = max(1, self.tab - 1)

    def first_tab(self, events, mouse_pos):
        self.display.blit(self.small_house_img, (307, 154))
        self.small_house_title.draw()
        self.small_house_resources.draw()
        self.small_house_result.draw()

        self.small_house_button.check_inp(mouse_pos)
        self.small_house_button.draw()

        for event in events:
            self.small_house_button.click_on_mouse_pos(event, mouse_pos)

    def second_tab(self, events, mouse_pos):
        pass

    def build_house(self, house_type):
        self.simulation.build_house(house_type,
                                    (pygame.mouse.get_pos()[0] - self.display_x,
                                     pygame.mouse.get_pos()[1] - self.display_y))
        self.small_house_button.is_pressed = False
