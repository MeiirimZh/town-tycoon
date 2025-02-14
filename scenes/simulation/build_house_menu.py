import pygame

from config import BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P, images, sounds
from scripts.textandbuttons import Text, Button


class BuildHouseMenu:
    def __init__(self, x, y, display, display_x, display_y, simulation):
        self.x = x
        self.y = y
        self.display = display
        self.display_x = display_x
        self.display_y = display_y
        self.simulation = simulation

        self.scroll_buttons = [Button(642, 392, 25, 16, BUTTON_COL, BUTTON_COL_H,
                               BUTTON_COL_P, 14, self.previous_tab, self.display, '^'),
                               Button(642, 418, 25, 16, BUTTON_COL, BUTTON_COL_H,
                               BUTTON_COL_P, 14, self.next_tab, self.display, 'v')]

        self.small_house_img = images['small_house_icon']
        self.small_house_title = Text(14, 'Small house', (255, 255, 255), (371, 154), self.display)
        self.small_house_resources = Text(12, '50 wood, 10 stone', (255, 255, 255), (371, 171), self.display)
        self.small_house_result = Text(12, '+10 dwellers', (255, 255, 255), (371, 186), self.display)
        self.small_house_button = Button(610, 168, 57, 22, BUTTON_COL, BUTTON_COL_H,
                                         BUTTON_COL_P, 14, lambda: self.build_house('small_house'),
                                         self.display, 'BUILD')
        self.build_menu_gui = images['gui_build_menu'].convert_alpha()

        self.medium_house_img = images['medium_house_icon']
        self.medium_house_title = Text(14, 'Medium house', (255, 255, 255), (371, 217), self.display)
        self.medium_house_resources = Text(12, '125 wood, 30 stone', (255, 255, 255), (371, 234), self.display)
        self.medium_house_result = Text(12, '+30 dwellers', (255, 255, 255), (371, 249), self.display)
        self.medium_house_button = Button(610, 231, 57, 22, BUTTON_COL, BUTTON_COL_H,
                                          BUTTON_COL_P, 14, lambda: self.build_house('medium_house'),
                                          self.display, 'BUILD')

        self.large_house_img = images['large_house_icon']
        self.large_house_title = Text(14, 'Large house', (255, 255, 255), (371, 280), self.display)
        self.large_house_resources = Text(12, '300 wood, 100 stone', (255, 255, 255), (371, 297), self.display)
        self.large_house_result = Text(12, '+70 dwellers', (255, 255, 255), (371, 312), self.display)
        self.large_house_button = Button(610, 294, 57, 22, BUTTON_COL, BUTTON_COL_H,
                                          BUTTON_COL_P, 14, lambda: self.build_house('large_house'),
                                          self.display, 'BUILD')

        self.school_img = images['school_icon']
        self.school_title = Text(14, 'School', (255, 255, 255), (371, 154), self.display)
        self.school_resources = Text(12, '200 wood, 50 stone', (255, 255, 255), (371, 171), self.display)
        self.school_result = Text(12, 'Provides education', (255, 255, 255), (371, 186), self.display)
        self.school_button = Button(610, 168, 57, 22, BUTTON_COL, BUTTON_COL_H,
                                         BUTTON_COL_P, 14, lambda: self.build_house('school'),
                                         self.display, 'BUILD')

        self.guard_house_img = images['guard_house_icon']
        self.guard_house_title = Text(14, 'Guard house', (255, 255, 255), (371, 217), self.display)
        self.guard_house_resources = Text(12, '350 wood, 125 stone', (255, 255, 255), (371, 234), self.display)
        self.guard_house_result = Text(12, 'Provides safety', (255, 255, 255), (371, 249), self.display)
        self.guard_house_button = Button(610, 231, 57, 22, BUTTON_COL, BUTTON_COL_H,
                                          BUTTON_COL_P, 14, lambda: self.build_house('guard_house'),
                                          self.display, 'BUILD')

        self.hospital_img = images['hospital_icon']
        self.hospital_title = Text(14, 'Hospital', (255, 255, 255), (371, 280), self.display)
        self.hospital_resources = Text(12, '300 wood, 100 stone', (255, 255, 255), (371, 297), self.display)
        self.hospital_result = Text(12, 'Provides health', (255, 255, 255), (371, 312), self.display)
        self.hospital_button = Button(610, 294, 57, 22, BUTTON_COL, BUTTON_COL_H,
                                         BUTTON_COL_P, 14, lambda: self.build_house('hospital'),
                                         self.display, 'BUILD')

        self.tab = 1
        self.tabs = {1: self.first_tab, 2: self.second_tab}

    def run(self, events):
        mouse_pos = pygame.mouse.get_pos()
        local_mouse_pos = (mouse_pos[0] - self.display_x, mouse_pos[1] - self.display_y)

        self.display.blit(self.build_menu_gui, (self.x, self.y))

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
        # Small house
        self.display.blit(self.small_house_img, (307, 154))
        self.small_house_title.draw()
        self.small_house_resources.draw()
        self.small_house_result.draw()

        self.small_house_button.check_inp(mouse_pos)
        self.small_house_button.draw()

        # Medium house
        self.display.blit(self.medium_house_img, (307, 217))
        self.medium_house_title.draw()
        self.medium_house_resources.draw()
        self.medium_house_result.draw()

        self.medium_house_button.check_inp(mouse_pos)
        self.medium_house_button.draw()

        # Large house
        self.display.blit(self.large_house_img, (307, 280))
        self.large_house_title.draw()
        self.large_house_resources.draw()
        self.large_house_result.draw()

        self.large_house_button.check_inp(mouse_pos)
        self.large_house_button.draw()

        for event in events:
            self.small_house_button.click_on_mouse_pos(event, mouse_pos)
            self.medium_house_button.click_on_mouse_pos(event, mouse_pos)
            self.large_house_button.click_on_mouse_pos(event, mouse_pos)

    def second_tab(self, events, mouse_pos):
        # School
        self.display.blit(self.school_img, (307, 154))
        self.school_title.draw()
        self.school_resources.draw()
        self.school_result.draw()

        self.school_button.check_inp(mouse_pos)
        self.school_button.draw()

        # Guard house
        self.display.blit(self.guard_house_img, (307, 217))
        self.guard_house_title.draw()
        self.guard_house_resources.draw()
        self.guard_house_result.draw()

        self.guard_house_button.check_inp(mouse_pos)
        self.guard_house_button.draw()

        # Hospital
        self.display.blit(self.hospital_img, (307, 280))
        self.hospital_title.draw()
        self.hospital_resources.draw()
        self.hospital_result.draw()

        self.hospital_button.check_inp(mouse_pos)
        self.hospital_button.draw()

        for event in events:
            self.school_button.click_on_mouse_pos(event, mouse_pos)
            self.guard_house_button.click_on_mouse_pos(event, mouse_pos)
            self.hospital_button.click_on_mouse_pos(event, mouse_pos)

    def build_house(self, house_type):
        if house_type == 'small_house':
            if self.simulation.data.wood >= 50 and self.simulation.data.stone >= 10:
                self.simulation.build_house(house_type,
                                            (pygame.mouse.get_pos()[0] - self.display_x,
                                             pygame.mouse.get_pos()[1] - self.display_y))
                self.small_house_button.is_pressed = False

                self.simulation.data.people += 10
                self.simulation.data.wood -= 50
                self.simulation.data.stone -= 10
            else:
                pygame.mixer.Sound.play(sounds['cancel1'])
        elif house_type == 'medium_house':
            if self.simulation.data.wood >= 125 and self.simulation.data.stone >= 30:
                self.simulation.build_house(house_type,
                                            (pygame.mouse.get_pos()[0] - self.display_x,
                                             pygame.mouse.get_pos()[1] - self.display_y))
                self.medium_house_button.is_pressed = False

                self.simulation.data.people += 30
                self.simulation.data.wood -= 125
                self.simulation.data.stone -= 30
            else:
                pygame.mixer.Sound.play(sounds['cancel1'])
        elif house_type == 'large_house':
            if self.simulation.data.wood >= 300 and self.simulation.data.stone >= 100:
                self.simulation.build_house(house_type,
                                            (pygame.mouse.get_pos()[0] - self.display_x,
                                             pygame.mouse.get_pos()[1] - self.display_y))
                self.large_house_button.is_pressed = False

                self.simulation.data.people += 70
                self.simulation.data.wood -= 300
                self.simulation.data.stone -= 100
            else:
                pygame.mixer.Sound.play(sounds['cancel1'])
        elif house_type == 'school':
            if self.simulation.data.wood >= 200 and self.simulation.data.stone >= 50:
                self.simulation.build_house(house_type,
                                            (pygame.mouse.get_pos()[0] - self.display_x,
                                             pygame.mouse.get_pos()[1] - self.display_y))
                self.school_button.is_pressed = False

                self.simulation.data.schools += 1
                self.simulation.data.wood -= 200
                self.simulation.data.stone -= 50
            else:
                pygame.mixer.Sound.play(sounds['cancel1'])
        elif house_type == 'guard_house':
            if self.simulation.data.wood >= 350 and self.simulation.data.stone >= 125:
                self.simulation.build_house(house_type,
                                            (pygame.mouse.get_pos()[0] - self.display_x,
                                             pygame.mouse.get_pos()[1] - self.display_y))
                self.guard_house_button.is_pressed = False

                self.simulation.data.guard_houses += 1
                self.simulation.data.wood -= 350
                self.simulation.data.stone -= 125
            else:
                pygame.mixer.Sound.play(sounds['cancel1'])
        elif house_type == 'hospital':
            if self.simulation.data.wood >= 200 and self.simulation.data.stone >= 50:
                self.simulation.build_house(house_type,
                                            (pygame.mouse.get_pos()[0] - self.display_x,
                                             pygame.mouse.get_pos()[1] - self.display_y))
                self.hospital_button.is_pressed = False

                self.simulation.data.hospitals += 1
                self.simulation.data.wood -= 200
                self.simulation.data.stone -= 50
            else:
                pygame.mixer.Sound.play(sounds['cancel1'])
