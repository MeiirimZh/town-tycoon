import pygame


class Simulation:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.surface = pygame.Surface((self.width, self.height))

        self.left_border = pygame.Rect(0, 0, 50, self.height)
        self.right_border = pygame.Rect(self.width-50, 0, 50, self.height)

        self.test = pygame.Rect(200, 200, 100, 100)

        self.scroll = [0, 0]

    def update(self):
        pass

    def render(self, display):
        self.surface.fill('green')

        pygame.draw.rect(self.surface, (255, 255, 255), self.left_border)
        pygame.draw.rect(self.surface, (255, 255, 255), self.right_border)

        pygame.draw.rect(self.surface, (0, 50, 210), self.test)

        display.blit(self.surface, (self.x, self.y))
