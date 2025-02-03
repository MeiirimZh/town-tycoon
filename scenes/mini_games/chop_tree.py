import pygame
import random

from config import SCREENWIDTH, SCREENHEIGHT, images
from scripts.timer import Timer
from scripts.textandbuttons import Text
from scripts.darken_background import DarkenBG
from scripts.mini_game_result_window import MiniGameResultWindow


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

        self.axe = images['axe']
        self.detect_rect = pygame.Rect(583, 109, 100, 50)
        self.axe_pos = 109

        self.direction = 1

        self.reward = self.data.wood_click_value
        self.chops = 0
        self.wood = 0

        self.text_list = [Text(24, 'Wood: 0', (255, 255, 255), (30, 30), self.display),
                          Text(24, 'Chops: 0', (255, 255, 255), (30, 60), self.display)]

        self.darken_bg = DarkenBG(0, 0, SCREENWIDTH, SCREENHEIGHT, (0, 0, 0), (0, 0), (SCREENWIDTH, SCREENHEIGHT), 128)

        self.result_window = MiniGameResultWindow(513, 199, 340, 260, self.display, self.game_state_manager)

        self.game_finished = False

    def start_new_game(self, current_time):
        pygame.mixer.music.load('music/mini_games/Chop Tree theme.mp3')
        pygame.mixer.music.play(-1)

        self.timer.start(40, current_time)
        self.generate_target()
        self.wood = 0
        self.chops = 0

    def run(self, events):
        current_time = pygame.time.get_ticks()

        self.display.fill('green')

        self.timer.update(current_time)

        for t in self.text_list:
            t.draw()
            if 'Wood' in t.msg:
                t.update_msg(f'Wood: {self.wood}')
            elif 'Chops' in t.msg:
                t.update_msg(f'Chops: {self.chops}')

        if self.timer.has_finished():
            self.darken_bg.draw(self.display)

            self.result_window.set_results('WOOD', self.wood, 'CHOPS', self.chops)
            self.result_window.draw(events)

            self.game_finished = True
        else:
            self.display.blit(self.axe, (790, self.axe_pos))

            if self.axe_pos == 109:
                self.direction = 1
            elif self.axe_pos == 559:
                self.direction = -1

            self.axe_pos += 5 * self.direction
            self.detect_rect.y = self.axe_pos

            for part in self.parts:
                pygame.draw.rect(self.display, (125, 28, 28), part)

            pygame.draw.rect(self.display, (255, 255, 0), self.target)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.target.colliderect(self.detect_rect):
                        result = random.randint(self.reward, self.reward * 5)

                        self.wood += result
                        self.data.wood += result

                        self.chops += 1
                        self.generate_target()

    def generate_target(self):
        self.target = random.choice(self.parts)
