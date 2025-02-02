import pygame
import random

from config import SCREENWIDTH, SCREENHEIGHT
from scripts.timer import Timer
from scripts.textandbuttons import Text
from scripts.darken_background import DarkenBG


class ChopTree:
    def __init__(self, display, game_state_manager, data):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data

        self.timer = Timer()

        self.parts = [pygame.Rect(583, 109, 100, 50)]
        self.target = None

        for i in range(9):
            self.parts.append(pygame.Rect(583, self.parts[-1].y+50, 100, 50))

        self.axe = pygame.Rect(790, 109, 200, 50)
        self.detect_rect = pygame.Rect(583, 109, 100, 50)
        self.axe_pos = 109

        self.direction = 1

        self.reward = 40
        self.chops = 0
        self.wood = 0

        self.text_list = [Text(24, 'Wood: 0', (255, 255, 255), (30, 30), self.display),
                          Text(24, 'Chops: 0', (255, 255, 255), (30, 60), self.display)]

        self.darken_bg = DarkenBG(0, 0, SCREENWIDTH, SCREENHEIGHT, (0, 0, 0), (0, 0), (SCREENWIDTH, SCREENHEIGHT), 128)

    def start_new_game(self, current_time):
        self.timer.start(40, current_time)
        self.generate_target()
        self.wood = 0
        self.chops = 0

    def run(self, events):
        current_time = pygame.time.get_ticks()

        self.display.fill('green')

        self.timer.update(current_time)
        print(self.timer.time_left())

        if self.timer.has_finished():
            self.darken_bg.draw(self.display)
        else:
            pygame.draw.rect(self.display, (255, 255, 255), self.axe)

            if self.axe.y == 109:
                self.direction = 1
            elif self.axe.y == 559:
                self.direction = -1

            self.axe.y += 5 * self.direction
            self.detect_rect.y = self.axe.y

            for part in self.parts:
                pygame.draw.rect(self.display, (125, 28, 28), part)

            pygame.draw.rect(self.display, (255, 255, 0), self.target)

        for t in self.text_list:
            t.draw()
            if 'Wood' in t.msg:
                t.update_msg(f'Wood: {self.wood}')
            elif 'Chops' in t.msg:
                t.update_msg(f'Chops: {self.chops}')

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.target.colliderect(self.detect_rect):
                        result = random.randint(self.reward - 10, self.reward + 10)

                        self.wood += result
                        self.data.wood += result

                        self.chops += 1
                        self.generate_target()

    def generate_target(self):
        self.target = random.choice(self.parts)
