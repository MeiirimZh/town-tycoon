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
        self.strike_duration = Timer()

        self.parts = [pygame.Rect(583, 159, 100, 50)]
        self.target = None

        for i in range(9):
            self.parts.append(pygame.Rect(583, self.parts[-1].y+50, 100, 50))

        self.aim = pygame.transform.flip(images['ct_aim'].convert_alpha(), True, False)
        self.indicator = images['ct_strike_indicator'].convert_alpha()
        self.tree_sprite = images['ct_tree'].convert_alpha()
        self.leaves = images['ct_leaves'].convert_alpha()
        self.strike = images['ct_strike'].convert_alpha()
        self.detect_rect = pygame.Rect(583, 109, 100, 50)
        self.aim_pos = 109

        self.direction = 1

        self.reward = self.data.wood_click_value
        self.chops = 0
        self.wood = 0

        self.text_list = [Text(24, 'Wood: 0', (255, 255, 255), (30, 30), self.display),
                          Text(24, 'Chops: 0', (255, 255, 255), (30, 60), self.display)]

        self.darken_bg = DarkenBG(0, 0, SCREENWIDTH, SCREENHEIGHT, (0, 0, 0), (0, 0), (SCREENWIDTH, SCREENHEIGHT), 128)

        self.result_window = MiniGameResultWindow(513, 199, 340, 260, self.display, self.game_state_manager)

        self.game_finished = False
        
        self.bg = images['ct_bg'].convert_alpha()

    def start_new_game(self, current_time):
        pygame.mixer.music.load('music/mini_games/Chop Tree theme.mp3')
        pygame.mixer.music.play(-1)

        self.timer.start(40, current_time)
        self.generate_target()
        self.wood = 0
        self.chops = 0
        self.strike_pos = 0

    def run(self, events):
        current_time = pygame.time.get_ticks()

        self.display.blit(self.bg, (0, 0))
        self.display.blit(self.tree_sprite, (583, 0))
        self.display.blit(self.leaves, (300, -200))

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
            self.display.blit(self.aim, (790, self.aim_pos))

            if self.aim_pos <= 109:
                self.direction = 1
            elif self.aim_pos >= 639:
                self.direction = -1

            self.aim_pos += 7 * self.direction
            self.detect_rect.y = self.aim_pos

            self.display.blit(self.indicator, (self.target[0] - 70, self.target[1])) 
            if not self.strike_duration.has_finished():
                self.display.blit(self.strike, (500, self.strike_pos - 40))        
            self.strike_duration.update(current_time)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.target.colliderect(self.detect_rect):
                        self.strike_pos = self.aim_pos
                        result = random.randint(self.reward, self.reward * 5)

                        self.wood += result
                        self.data.wood += result

                        self.chops += 1
                        self.generate_target()         
                        self.strike_duration.start(0.3, current_time)


    def generate_target(self):
        self.target = random.choice(self.parts)
