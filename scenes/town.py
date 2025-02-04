import pygame
import random

from collections import deque

from config import *

from scripts.timer import Timer
from scripts.textandbuttons import Text, Button
from scripts.utils import get_quarter, get_section
from scripts.progressbar import Progressbar

from scenes.simulation.simulation import Simulation


class Town:
    def __init__(self, display, game_state_manager, data, animal_hunt, chop_tree):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data
        self.animal_hunt = animal_hunt
        self.chop_tree = chop_tree

        self.simulation = Simulation(392, 0, 974, 588, self.display)

        self.can_harvest = False
        self.btn_cooldown = Timer(True)
        self.btn_cooldown.start(1, 0)

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
        self.text_list.append(Text(64, "Prodos", (255, 255, 255), (65, 60), self.display))
        self.text_list.append(Text(24, f":{self.data.wood}", (255, 255, 255), (460, 640), self.display))
        self.text_list.append(Text(24, f":{self.data.stone}", (255, 255, 255), (610, 640), self.display))
        self.text_list.append(Text(24, f":{self.data.food}", (255, 255, 255), (460, 690), self.display))
        self.text_list.append(Text(24, f":{self.data.water}", (255, 255, 255), (610, 690), self.display))

        self.progressbar = Progressbar(self.display, (30, 645), 1, 330, False)

        self.main_menu = images['gui_main_menu'].convert_alpha()
        self.resources_panel = images['gui_resources_panel'].convert_alpha()
        self.gui_water = pygame.transform.scale(images['water_icon'].convert_alpha(), (50, 50))
        self.gui_food = pygame.transform.scale(images['food_icon'].convert_alpha(), (50, 50))
        self.gui_wood = pygame.transform.scale(images['wood_icon'].convert_alpha(), (50, 50))
        self.gui_stone = pygame.transform.scale(images['stone_icon'].convert_alpha(), (50, 50))

    def harvest(self):
        if self.can_harvest:
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
            self.can_harvest = False
            self.progressbar.reset()

    def calculate_stability(self):
        food_scores = get_section(self.data.food, self.data.food_storage, 12)
        water_scores = get_section(self.data.water, self.data.water_storage, 8)
        total_scores = food_scores + water_scores

        return get_quarter(total_scores, 20)

    def run(self, events):
        mouse_pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()

        self.btn_cooldown.update(current_time)

        if self.btn_cooldown.has_finished():
            self.can_harvest = True

        self.display.fill('blue')
        self.display.blit(self.resources_panel, (0, 588))
        self.display.blit(self.main_menu, (0, 0))
        self.display.blit(self.gui_wood, (410, 620))
        self.display.blit(self.gui_stone, (560, 620))
        self.display.blit(self.gui_food, (410, 680))
        self.display.blit(self.gui_water, (560, 680))


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
            l.draw((100, 365 - (50 * index)))

        self.progressbar.draw()

        self.simulation.update(events)
        self.simulation.render()

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
