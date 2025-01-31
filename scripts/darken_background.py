import pygame


class DarkenBG:
    def __init__(self, x, y, width, height, rect_color, rect_pos, rect_size, alpha_value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect_color = rect_color
        self.rect_pos = rect_pos
        self.rect_size = rect_size

        self.transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.transparent_surface.set_alpha(alpha_value)
        pygame.draw.rect(self.transparent_surface, rect_color, (rect_pos[0], rect_pos[1], rect_size[0], rect_size[1]))

    def draw(self, display):
        display.blit(self.transparent_surface, (self.x, self.y))
