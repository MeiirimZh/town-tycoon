import pygame

from config import *

from scripts.timer import Timer
from scripts.textandbuttons import Text


class Intro:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager

        self.timer = Timer()
        self.timer.start(2, 0)
        self.text = Text(64, "Prodos", (255, 255, 255), (800, 350), self.display)

    def run(self, events):
        current_time = pygame.time.get_ticks()
        self.display.fill((0, 0, 0))
        self.timer.update(current_time)

        self.text.draw()

        if self.timer.has_finished():
            self.game_state_manager.set_state("Town")

