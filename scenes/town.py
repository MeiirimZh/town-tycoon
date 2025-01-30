import pygame
import random
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

        self.button_list.append(Button(30, 600, 330, 100, BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P, 32, "harvest", self.display, "Find Resources"))
        self.text_list.append(Text(64, "Prodos", (255, 255, 255), (60, 60), self.display))

        self.button_f = ""

    def run(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        current_time = pygame.time.get_ticks()

        self.display.fill('blue')

        self.worker_timer.update(current_time)

        if self.worker_timer.has_finished():
            self.data.wood += self.data.lumberjacks
            self.data.stone += self.data.miners

        self.food_timer.update(current_time)

        if self.food_timer.has_finished():
            self.data.food = max(0, self.data.food - self.data.people // 5)
            print(f'Food: {self.data.food}')

        for t in self.text_list:
            t.draw()

        for b in self.button_list:
            b.check_inp(mouse_pos)
            if b.click(mouse_pos, mouse_pressed):
                self.button_f = b.click_func
            b.draw()

        if self.button_f == "harvest":
            resource = random.choice(self.data.resource_types)
            if resource == 'Wood':
                self.data.wood += self.data.wood_click_value
                print(f'Wood: {self.data.wood}')
            elif resource == 'Stone':
                self.data.stone += self.data.stone_click_value
                print(f'Stone: {self.data.stone}')
            self.button_f = ""

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.game_state_manager.set_state('Store')
                if event.key == pygame.K_SPACE:
                    resource = random.choice(self.data.resource_types)
                    if resource == 'Wood':
                        self.data.wood += self.data.wood_click_value
                        print(f'Wood: {self.data.wood}')
                    elif resource == 'Stone':
                        self.data.stone += self.data.stone_click_value
                        print(f'Stone: {self.data.stone}')
