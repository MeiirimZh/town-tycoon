import pygame
import random

from collections import deque

from config import *

from scripts.timer import Timer
from scripts.textandbuttons import Text, Button

from scripts.utils import get_quarter, get_section

from scenes.simulation.simulation import Simulation


class Town:
    def __init__(self, display, game_state_manager, data, animal_hunt, chop_tree):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data
        self.animal_hunt = animal_hunt
        self.chop_tree = chop_tree

        self.simulation = Simulation(392, 0, 974, 588)

        self.worker_timer = Timer(True)
        self.worker_timer.start(1, 0)

        self.basic_resources_timer = Timer(True)
        self.basic_resources_timer.start(30, 0)

        self.animal_hunt_cooldown_timer = Timer()
        self.animal_hunt_cooldown_timer.start(ANIMAL_HUNT_COOLDOWN_TIME, 0)

        self.chop_tree_cooldown_timer = Timer()
        self.chop_tree_cooldown_timer.start(CHOP_TREE_COOLDOWN_TIME, 0)

        self.animal_hunt_active = False
        self.chop_tree_active = False

        self.text_list = []
        self.button_list = []
        self.log = deque(maxlen=4)

        self.button_list.append(Button(30, 650, 330, 100, BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P, 32, self.harvest, self.display, "Find Resources"))
        self.text_list.append(Text(64, "Prodos", (255, 255, 255), (30, 60), self.display))
        self.text_list.append(Text(24, f"W: {self.data.wood}", (255, 255, 255), (430, 730), self.display))
        self.text_list.append(Text(24, f"S: {self.data.stone}", (255, 255, 255), (560, 730), self.display))
        self.text_list.append(Text(24, f"F: {self.data.stone}", (255, 255, 255), (690, 730), self.display))
        self.text_list.append(Text(24, f"H: {self.data.stone}", (255, 255, 255), (820, 730), self.display))

    def harvest(self):
        resource = random.choice(self.data.resource_types)
        if resource == 'Wood':
            self.data.wood += self.data.wood_click_value
            # print(f'Wood: {self.data.wood}')
            self.log.append(Text(32, f'Wood: {self.data.wood_click_value}', (255, 255, 255), (60, 400), self.display))
        elif resource == 'Stone':
            self.data.stone += self.data.stone_click_value
            # print(f'Stone: {self.data.stone}')
            self.log.append(Text(32, f'Stone: {self.data.stone_click_value}', (255, 255, 255), (60, 400), self.display))
        elif resource == 'Food':
            self.data.food = min(self.data.food_storage, self.data.food + self.data.food_click_value)
            # print(f'Food: {self.data.food}')
            self.log.append(Text(32, f'Food: {self.data.food_click_value}', (255, 255, 255), (60, 400), self.display))
        elif resource == 'Water':
            self.data.water = min(self.data.water_storage, self.data.water + self.data.water_click_value)
            # print(f'Water: {self.data.water}')
            self.log.append(Text(32, f'Water: {self.data.water_click_value}', (255, 255, 255), (60, 400), self.display))

        self.button_f = ""

    def calculate_stability(self):
        food_scores = get_section(self.data.food, self.data.food_storage, 12)
        water_scores = get_section(self.data.water, self.data.water_storage, 8)
        total_scores = food_scores + water_scores

        return get_quarter(total_scores, 20)

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
            self.data.food += self.data.hunters

        self.basic_resources_timer.update(current_time)

        if self.basic_resources_timer.has_finished():
            self.data.food = max(0, self.data.food - self.data.people // 5)
            self.data.water = max(0, self.data.water - self.data.people // 2)
            # print(f'Food: {self.data.food}')
            # print(f'Water: {self.data.water}')

        # print(f'Stability: {self.calculate_stability()}')

        self.animal_hunt_cooldown_timer.update(current_time)

        if self.animal_hunt_cooldown_timer.has_finished():
            self.animal_hunt_active = True

        if self.animal_hunt.game_finished:
            self.animal_hunt_cooldown_timer.start(ANIMAL_HUNT_COOLDOWN_TIME, current_time)
            self.animal_hunt_active = False
            self.animal_hunt.game_finished = False

        self.chop_tree_cooldown_timer.update(current_time)

        if self.chop_tree_cooldown_timer.has_finished():
            self.chop_tree_active = True

        if self.chop_tree.game_finished:
            self.chop_tree_cooldown_timer.start(CHOP_TREE_COOLDOWN_TIME, current_time)
            self.chop_tree_active = False
            self.chop_tree.game_finished = False

        for t in self.text_list:
            if "W" in t.msg:
                t.update_msg(f"W: {self.data.wood}")
            elif "S" in t.msg:
                t.update_msg(f"S: {self.data.stone}")
            elif "F" in t.msg:
                t.update_msg(f"F: {self.data.food}")
            elif "H" in t.msg:
                t.update_msg(f"H: {self.data.water}")
            t.draw()

        for b in self.button_list:
            b.check_inp(mouse_pos)
            b.draw()

        for index, l in enumerate(self.log):
            l.draw((30, 300 - (50 * index)))

        self.simulation.render(self.display)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.game_state_manager.set_state('Store')
                if event.key == pygame.K_s:
                    if self.animal_hunt_active:
                        self.animal_hunt.start_new_game(current_time)
                        self.game_state_manager.set_state('Animal Hunt')
                if event.key == pygame.K_d:
                    if self.chop_tree_active:
                        self.chop_tree.start_new_game(current_time)
                        self.game_state_manager.set_state('Chop Tree')
            for b in self.button_list:
                b.click(event)
