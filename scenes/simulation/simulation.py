import pygame

from config import images
from scenes.simulation.house import House
from scenes.simulation.build_house_menu import BuildHouseMenu
from scripts.textandbuttons import Text
from config import sounds


class Simulation:
    def __init__(self, x, y, width, height, display, data):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display = display
        self.data = data

        self.surface = pygame.Surface((self.width, self.height))

        self.hint_text = Text(10, '[Right mouse button] to reset the position', (255, 255, 255), (30, self.height-30), self.surface)

        self.left_border = pygame.Rect(0, 0, 50, self.height)
        self.right_border = pygame.Rect(self.width-50, 0, 50, self.height)
        self.top_border = pygame.Rect(0, 0, self.width, 50)
        self.bottom_border = pygame.Rect(0, self.height-50, self.width, 50)

        self.is_building = False
        self.can_build = False
        self.building_house = None
        self.building_house_type = None
        self.building_house_x = 0
        self.building_house_y = 0
        self.building_house_rect = None

        self.build_house_menu = BuildHouseMenu(287, 134, 400, 320, self.surface, self.x, self.y, self)
        self.build_house_menu_active = False

        self.scroll = [0, 0]

    def run(self, events):
        mouse_pos = pygame.mouse.get_pos()
        local_mouse_pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)

        if self.left_border.collidepoint(local_mouse_pos):
            self.scroll[0] += 3

        if self.right_border.collidepoint(local_mouse_pos):
            self.scroll[0] -= 3

        if self.top_border.collidepoint(local_mouse_pos):
            self.scroll[1] += 3

        if self.bottom_border.collidepoint(local_mouse_pos):
            self.scroll[1] -= 3

        if self.is_building:
            self.building_house_x = local_mouse_pos[0]
            self.building_house_y = local_mouse_pos[1]
            self.building_house_rect = pygame.Rect(self.building_house_x, self.building_house_y,
                                                   self.building_house.get_width(), self.building_house.get_height())

            self.can_build = True
            for house in self.data.houses:
                if house.rect.colliderect(self.building_house_rect.move(-self.scroll[0], -self.scroll[1])):
                    self.can_build = False

        self.surface.fill((122, 167, 71))

        for house in self.data.houses:
            house.render(self.surface, self.scroll)

        if self.is_building:
            self.surface.blit(self.building_house, (self.building_house_x, self.building_house_y))

        self.hint_text.draw()

        if self.build_house_menu_active:
            self.build_house_menu.run(events)

        self.display.blit(self.surface, (self.x, self.y))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.is_building:
                        if self.can_build:
                            self.data.houses.append(House(self.building_house_type,
                                                          self.building_house_x - self.scroll[0],
                                                          self.building_house_y - self.scroll[1]))
                            self.is_building = False
                        else:
                            pygame.mixer.Sound.play(sounds['cancel1'])
                if event.button == 2:
                    self.build_house_menu_active = not self.build_house_menu_active
                if event.button == 3:
                    self.scroll = [0, 0]

    def build_house(self, house_type, mouse_pos):
        self.is_building = True
        self.building_house_type = house_type
        self.building_house = images[house_type]
        self.building_house_x = mouse_pos[0]
        self.building_house_y = mouse_pos[1]
        self.building_house_rect = pygame.Rect(self.building_house_x, self.building_house_y,
                                               self.building_house.get_width(), self.building_house.get_height())

        self.build_house_menu_active = False

    def draw_borders(self):
        pygame.draw.rect(self.surface, (255, 255, 255), self.left_border)
        pygame.draw.rect(self.surface, (255, 255, 255), self.right_border)
        pygame.draw.rect(self.surface, (255, 255, 255), self.top_border)
        pygame.draw.rect(self.surface, (255, 255, 255), self.bottom_border)
