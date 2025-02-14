import pygame

from config import *

from scripts.timer import Timer
from scripts.textandbuttons import Text


class Intro:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager

        self.timer = Timer()
        self.timer_to_fade = Timer()
        self.timer.start(4, 0)
        self.text = Text(64, "Prodos", (255, 255, 255), (560, 350), self.display)
        self.authors = Text(16, "Vlad Paul & Meiirim Zhanzhumanov", (255, 255, 255), (515, 700), self.display)
        self.authors2 = Text(16, "9-2-PO-22", (255, 255, 255), (635, 730), self.display)
        self.alpha = 0
        self.alpha_change = False
        self.vladdebil = 0

    def run(self, events):
        current_time = pygame.time.get_ticks()
        self.display.fill((0, 0, 0))
        self.timer.update(current_time)


        if self.alpha <= 250 and not self.alpha_change:
            self.alpha += 5
        if self.alpha == 255:
            self.alpha_change = True
        
        if self.alpha_change == True and self.vladdebil < 80:
            self.vladdebil += 1
        
        if self.vladdebil >= 80:
            self.alpha -= 10

        self.text.text_surface.set_alpha(self.alpha)
        self.authors.text_surface.set_alpha(self.alpha)
        self.authors2.text_surface.set_alpha(self.alpha)

        self.text.draw()
        self.authors.draw()
        self.authors2.draw()

        if self.timer.has_finished():
            self.game_state_manager.set_state("Town")

