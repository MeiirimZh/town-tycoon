import pygame

from scripts.textandbuttons import Text


class MiniGameResultWindow:
    def __init__(self, x, y, width, height, display):
        self.display = display
        self.rect = pygame.Rect(x, y, width, height)
        self.result_text = Text(40, 'RESULT', (255, 255, 255), (608, 164), self.display)

    def draw(self):
        pygame.draw.rect(self.display, (93, 37, 37), self.rect)
        self.result_text.draw()
