import pygame.font

from config import MONOCRAFT_FONT


def get_quarter(x, y):
    quarter_size = y / 4
    if x == 0:
        return 1
    for i in range(4):
        if i * quarter_size < x <= (i + 1) * quarter_size:
            return i + 1


def get_section(x, y, z):
    section_size = y / z
    if x == 0:
        return 1
    for i in range(z):
        if i * section_size < x <= (i + 1) * section_size:
            return i + 1


def create_font(size):
    return pygame.font.Font(MONOCRAFT_FONT, size)