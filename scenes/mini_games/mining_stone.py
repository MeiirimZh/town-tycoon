import pygame
import random

from config import SCREENWIDTH, SCREENHEIGHT, images
from scripts.timer import Timer
from scripts.textandbuttons import Text
from scripts.darken_background import DarkenBG
from scripts.mini_game_result_window import MiniGameResultWindow


class MiningStone:
    def __init__(self, display, game_state_manager, data):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data

        self.timer = Timer()
        self.round_timer = Timer(True)
        self.strike_duration = Timer()

        self.reward = self.data.stone_click_value
        self.rounds = 1
        self.stone = 0

        self.bar = pygame.Rect(183, 650, 300, 30)
        self.bar_width = self.bar.width
        self.bar_step = 0.1
        self.bar_bg = pygame.Rect(183, 650, 1000, 30)
        self.bar_width_initial = self.bar_bg.width
        self.bar_click_step = 25

        self.marker = pygame.Rect(1023, 650, 10, 30)

        self.text_list = [Text(24, 'Stone: 0', (255, 255, 255), (30, 30), self.display),
                          Text(24, 'Round: 0', (255, 255, 255), (30, 60), self.display),
                          Text(40, '10', (255, 255, 255), (671, 100), self.display)]

        self.darken_bg = DarkenBG(0, 0, SCREENWIDTH, SCREENHEIGHT, (0, 0, 0), (0, 0), (SCREENWIDTH, SCREENHEIGHT), 128)

        self.result_window = MiniGameResultWindow(513, 199, 340, 260, self.display, self.game_state_manager)

        self.game_finished = False

        self.pickaxe = pygame.transform.scale(images['m_pickaxe'], (400, 400)).convert_alpha()
        self.stone_sprite = images['m_stone'].convert_alpha()
        self.shards = images['m_shards'].convert_alpha()
        self.bg = images['m_bg'].convert_alpha()

    def start_new_game(self, current_time):
        self.timer.start(30, current_time)
        self.round_timer.start(10, current_time)

        self.stone = 0
        self.rounds = 0

    def run(self, events):
        current_time = pygame.time.get_ticks()

        self.display.blit(self.bg, (0, 0))

        self.timer.update(current_time)
        self.round_timer.update(current_time)
        self.display.blit(self.pickaxe, (300, 200))
        if self.strike_duration.has_finished():
            self.display.blit(self.stone_sprite, (700, 400))
        else:
            self.display.blit(self.shards, (700, 400))

        pygame.draw.rect(self.display, (23, 23, 23), self.bar_bg)
        pygame.draw.rect(self.display, (255, 255, 255), self.bar)
        pygame.draw.rect(self.display, (200, 10, 0), self.marker)

        for t in self.text_list:
            t.draw()
            if 'Stone' in t.msg:
                t.update_msg(f'Stone: {self.stone}')
            elif 'Round' in t.msg:
                t.update_msg(f'Round: {self.rounds}')
            else:
                if not self.game_finished:
                    t.update_msg(str(self.round_timer.time_left()))

        if self.timer.has_finished():
            self.darken_bg.draw(self.display)

            self.result_window.set_results('STONE', self.stone, 'ROUNDS', self.rounds + 1)
            self.result_window.draw(events)

            self.game_finished = True
        else:
            if self.round_timer.has_finished():
                if self.bar_width >= 850:
                    result = random.randint(self.reward * 5, self.reward * 10)

                    self.data.stone += result
                    self.stone += result
                    self.strike_duration.start(0.3, current_time)

                self.bar_width = 300
                self.rounds += 1

            if self.bar_width - self.get_bar_step_pixels() >= 0:
                self.bar_width -= self.get_bar_step_pixels()
                self.bar = pygame.Rect(183, 650, self.bar_width, 30)
        
        self.strike_duration.update(current_time)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.game_finished and self.bar_width + self.bar_click_step <= self.bar_width_initial:
                        self.bar_width += self.bar_click_step

    def get_bar_step_pixels(self):
        return self.bar_width_initial * self.bar_step / 100
