import pygame
import os
from config import MONOCRAFT_FONT


class Text:
    def __init__(self, size, msg, color, position, display):
        pygame.font.init()
        self.size = size
        self.font = pygame.font.Font(MONOCRAFT_FONT, self.size)
        self.msg = msg
        self.color = color
        self.position = position
        self.display = display

    def draw(self):
        text_surface = self.font.render(self.msg, False, self.color)
        text_rect = text_surface.get_rect(topleft=self.position)
        self.display.blit(text_surface, text_rect)


class Button:
    def __init__(self, x, y, width, height, color, hover_col, pressed_col, font_size, click_func, display,
                 text="", font_path=MONOCRAFT_FONT) -> None:
        pygame.font.init()

        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_col = hover_col
        self.pressed_col = pressed_col
        self.display = display
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(font_path, font_size)
        self.is_hovered = False
        self.is_pressed = False
        self.was_pressed = False
        self.text_color = (0, 0, 0)
        self.click_func = click_func
        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.Font(None, font_size)

    def draw(self):
        current_col = self.pressed_col if self.is_pressed else self.hover_col if self.is_hovered else self.color
        pygame.draw.rect(self.display, current_col, self.rect)
        text_surface = self.font.render(self.text, False, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.display.blit(text_surface, text_rect)

    def check_inp(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def click(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos):
            if mouse_click[0]:
                self.is_pressed = True
                if not self.was_pressed:
                    self.was_pressed = True
                    self.click_func()
            else:
                self.is_pressed = False
                self.was_pressed = False
        return None
