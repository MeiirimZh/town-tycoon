import pygame
import random

from collections import deque

from config import *

from scripts.timer import Timer
from scripts.textandbuttons import Text, Button


class Town:
    def __init__(self, display, game_state_manager, data):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data

        self.worker_timer = Timer(True)
        self.worker_timer.start(1, 0)

        self.food_timer = Timer(True)
        self.food_timer.start(3, 0)

        self.text_list = []
        self.button_list = []
        self.log = deque(maxlen=4)

        self.button_list.append(Button(30, 650, 330, 100, BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P, 32, self.harvest, self.display, "Find Resources"))
        self.text_list.append(Text(64, "Prodos", (255, 255, 255), (30, 60), self.display))
        self.text_list.append(Text(24, f"W: {self.data.wood}", (255, 255, 255), (430, 730), self.display))
        self.text_list.append(Text(24, f"S: {self.data.stone}", (255, 255, 255), (530, 730), self.display))

    def harvest(self):
        resource = random.choice(self.data.resource_types)
        if resource == 'Wood':
            self.data.wood += self.data.wood_click_value
            print(f'Wood: {self.data.wood}')
            self.log.append(Text(32, f'Wood: {self.data.wood_click_value}', (255, 255, 255), (60, 400), self.display))
        elif resource == 'Stone':
            self.data.stone += self.data.stone_click_value
            print(f'Stone: {self.data.stone}')
            self.log.append(Text(32, f'Stone: {self.data.stone_click_value}', (255, 255, 255), (60, 400), self.display))

        self.button_f = ""

    def run(self, events):
        mouse_pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()

        self.display.fill('blue')
        pygame.draw.rect(self.display, (50, 5, 0), (0, 710, 1366, 768))
        pygame.draw.rect(self.display, (74, 10, 0), (0, 0, 400, 768))

        self.worker_timer.update(current_time)

        if self.worker_timer.has_finished():
            self.data.wood += self.data.lumberjacks
            self.data.stone += self.data.miners

        self.food_timer.update(current_time)

        if self.food_timer.has_finished():
            self.data.food = max(0, self.data.food - self.data.people // 5)
            print(f'Food: {self.data.food}')

        for t in self.text_list:
            if "Wood" in t.msg:
                t.update_msg(f"Wood: {self.data.wood}")
            elif "Stone" in t.msg:
                t.update_msg(f"Stone: {self.data.stone}")
            t.draw()

        for b in self.button_list:
            b.check_inp(mouse_pos)
            b.draw()

        for index, l in enumerate(self.log):
            l.draw((30, 300 - (50 * index)))

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.game_state_manager.set_state('Store')
            for b in self.button_list:
                b.click(event)