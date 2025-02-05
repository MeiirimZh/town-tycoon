import pygame

from config import images
from scenes.simulation.house import House
from scripts.textandbuttons import Text


class Simulation:
    def __init__(self, x, y, width, height, display, data):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display = display
        self.data = data

        self.surface = pygame.Surface((self.width, self.height))

        self.hint_text = Text(10, '[SPACE] to reset the position', (255, 255, 255), (30, self.height-30), self.surface)

        self.left_border = pygame.Rect(0, 0, 50, self.height)
        self.right_border = pygame.Rect(self.width-50, 0, 50, self.height)
        self.top_border = pygame.Rect(0, 0, self.width, 50)
        self.bottom_border = pygame.Rect(0, self.height-50, self.width, 50)

        self.is_building = False
        self.building_house = None
        self.building_house_type = None
        self.building_house_x = 0
        self.building_house_y = 0

        self.scroll = [0, 0]

    def update(self, events):
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

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.scroll = [0, 0]
                if event.key == pygame.K_z:
                    self.build_house('small_house')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.is_building:
                        self.data.houses.append(House(self.building_house_type,
                                                      self.building_house_x - self.scroll[0],
                                                      self.building_house_y - self.scroll[1]))
                        self.is_building = False

    def render(self):
        self.surface.fill((0, 200, 20))

        for house in self.data.houses:
            house.render(self.surface, self.scroll)

        if self.is_building:
            self.surface.blit(self.building_house, (self.building_house_x, self.building_house_y))

        self.hint_text.draw()

        self.display.blit(self.surface, (self.x, self.y))

    def build_house(self, house_type):
        self.is_building = True
        self.building_house_type = house_type
        self.building_house = images[house_type]

    def draw_borders(self):
        pygame.draw.rect(self.surface, (255, 255, 255), self.left_border)
        pygame.draw.rect(self.surface, (255, 255, 255), self.right_border)
        pygame.draw.rect(self.surface, (255, 255, 255), self.top_border)
        pygame.draw.rect(self.surface, (255, 255, 255), self.bottom_border)
