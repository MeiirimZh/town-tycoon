import pygame

from scripts.textandbuttons import Text


class Simulation:
    def __init__(self, x, y, width, height, display):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.display = display

        self.surface = pygame.Surface((self.width, self.height))

        self.hint_text = Text(10, '[SPACE] to reset position', (255, 255, 255), (30, self.height-30), self.surface)

        self.left_border = pygame.Rect(0, 0, 50, self.height)
        self.right_border = pygame.Rect(self.width-50, 0, 50, self.height)
        self.top_border = pygame.Rect(0, 0, self.width, 50)
        self.bottom_border = pygame.Rect(0, self.height-50, self.width, 50)

        self.test = pygame.Rect(200, 200, 100, 100)
        self.test_x = 200
        self.test_y = 200

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

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.scroll = [0, 0]

        self.test.x = self.test_x + self.scroll[0]
        self.test.y = self.test_y + self.scroll[1]

    def render(self):
        self.surface.fill((0, 200, 20))

        pygame.draw.rect(self.surface, (0, 50, 210), self.test)

        self.hint_text.draw()

        self.display.blit(self.surface, (self.x, self.y))

    def draw_borders(self):
        pygame.draw.rect(self.surface, (255, 255, 255), self.left_border)
        pygame.draw.rect(self.surface, (255, 255, 255), self.right_border)
        pygame.draw.rect(self.surface, (255, 255, 255), self.top_border)
        pygame.draw.rect(self.surface, (255, 255, 255), self.bottom_border)
