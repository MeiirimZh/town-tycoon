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

        self.can_scroll = True
        self.prokrutka_speed = 5

        self.surface = pygame.Surface((self.width, self.height))

        self.hint_text = Text(10, '[SPACE] to reset the position, [MBM] to open build menu', (255, 255, 255), (30, self.height-30), self.surface)

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

        self.build_house_menu = BuildHouseMenu(287, 134, self.surface, self.x, self.y, self)
        self.build_house_menu_active = False

        self.scroll = [0, 0]
        self.tile_texture = images["grass"].convert_alpha()
        self.tile_width, self.tile_height = self.tile_texture.get_size()


    def run(self, events):
        offset_x = self.scroll[0] % self.tile_width
        offset_y = self.scroll[1] % self.tile_height

        for x in range(offset_x - self.tile_width, self.width, self.tile_width):
            for y in range(offset_y - self.tile_height, self.height, self.tile_height):
                self.surface.blit(self.tile_texture, (x, y))

        mouse_pos = pygame.mouse.get_pos()
        local_mouse_pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)

        if self.can_scroll:
            if self.left_border.collidepoint(local_mouse_pos):
                self.scroll[0] += self.prokrutka_speed

            if self.right_border.collidepoint(local_mouse_pos):
                self.scroll[0] -= self.prokrutka_speed

            if self.top_border.collidepoint(local_mouse_pos):
                self.scroll[1] += self.prokrutka_speed

            if self.bottom_border.collidepoint(local_mouse_pos):
                self.scroll[1] -= self.prokrutka_speed

        if self.is_building:
            self.building_house_x = local_mouse_pos[0]
            self.building_house_y = local_mouse_pos[1]
            self.building_house_rect = pygame.Rect(self.building_house_x, self.building_house_y,
                                                   self.building_house.get_width(), self.building_house.get_height())

            self.can_build = True
            for house in self.data.houses:
                if house.rect.colliderect(self.building_house_rect.move(-self.scroll[0], -self.scroll[1])):
                    self.can_build = False

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
                if event.button == 3:
                    if self.is_building:
                        if self.can_build:
                            self.data.houses.append(House(self.building_house_type,
                                                          self.building_house_x - self.scroll[0],
                                                          self.building_house_y - self.scroll[1]))
                            self.is_building = False

                            pygame.mixer.Sound.play(sounds['build'])
                        else:
                            pygame.mixer.Sound.play(sounds['cancel1'])
                if event.button == 2:
                    if not self.is_building:
                        self.build_house_menu_active = not self.build_house_menu_active
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
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
