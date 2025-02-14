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
    def __init__(self, display, game_state_manager, data, animal_hunt, chop_tree, mining_stone):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data
        self.animal_hunt = animal_hunt
        self.chop_tree = chop_tree
        self.mining_stone = mining_stone

        self.simulation = Simulation(392, 0, 974, 588, self.display, self.data)

        self.can_harvest = False
        self.btn_cooldown = Timer(True)
        self.btn_cooldown.start(1, 0)

        self.worker_timer = Timer(True)
        self.worker_timer.start(1, 0)

        self.basic_resources_timer = Timer(True)
        self.basic_resources_timer.start(30, 0)

        self.town_development_timer = Timer(True)
        self.town_development_timer.start(15, 0)

        self.animal_hunt_cooldown_timer = Timer()
        self.animal_hunt_cooldown_timer.start(ANIMAL_HUNT_COOLDOWN_TIME, 0)

        self.chop_tree_cooldown_timer = Timer()
        self.chop_tree_cooldown_timer.start(CHOP_TREE_COOLDOWN_TIME, 0)

        self.mining_stone_cooldown_timer = Timer()
        self.mining_stone_cooldown_timer.start(MINING_STONE_COOLDOWN_TIME, 0)

        self.animal_hunt_active = False
        self.chop_tree_active = False
        self.mining_stone_active = False

        self.text_list = []
        self.button_list = []
        self.log = deque(maxlen=4)

        self.button_list.append(Button(30, 650, 330, 100, BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P, 32, self.harvest, self.display, "Find Resources"))
        self.text_list.append(Text(64, "Prodos", (255, 255, 255), (65, 60), self.display))
        self.text_list.append(Text(24, f":{self.data.wood}", (255, 255, 255), (460, 640), self.display))
        self.text_list.append(Text(24, f":{self.data.stone}", (255, 255, 255), (610, 640), self.display))
        self.text_list.append(Text(24, f":{self.data.food}", (255, 255, 255), (460, 690), self.display))
        self.text_list.append(Text(24, f":{self.data.water}", (255, 255, 255), (610, 690), self.display))
        self.text_list.append(Text(24, "Stability:", (255, 255, 255), (45, 505), self.display))
        self.text_list.append(Text(16, f"Dwellers: {self.data.people}", (255, 255, 255), (45, 540), self.display))
        self.text_list.append(Text(16, f"Education: {self.data.education}", (255, 255, 255), (45, 560), self.display))
        self.text_list.append(Text(16, f"Safety: {self.data.safety}", (255, 255, 255), (45, 580), self.display))
        self.text_list.append(Text(16, f"Health: {self.data.health}", (255, 255, 255), (45, 600), self.display))

        self.progressbar = Progressbar(self.display, (30, 645), 1, 330, False)

        self.main_menu = images['gui_main_menu'].convert_alpha()
        self.resources_panel = images['gui_resources_panel'].convert_alpha()
        self.gui_water = pygame.transform.scale(images['water_icon'].convert_alpha(), (50, 50))
        self.gui_food = pygame.transform.scale(images['food_icon'].convert_alpha(), (50, 50))
        self.gui_wood = pygame.transform.scale(images['wood_icon'].convert_alpha(), (50, 50))
        self.gui_stone = pygame.transform.scale(images['stone_icon'].convert_alpha(), (50, 50))
        self.st_frame = images['st_frame'].convert_alpha()
        self.gui_icon_sh = images['sh_icon'].convert_alpha()
        self.gui_icon_h = images['h_icon'].convert_alpha()
        self.gui_icon_avg = images['avg_icon'].convert_alpha()
        self.gui_icon_sad = images['sad_icon'].convert_alpha()

        self.button_list.append(Button(1218, 608, 130, 27, BUTTON_COL, BUTTON_COL_H,
                                       BUTTON_COL_P, 16, self.show_mini_games, self.display, 'MINI-GAMES'))

        self.mini_games_menu_active = False
        self.mini_games_buttons = []
        self.mini_games_buttons.append(Button(1198, 581, 150, 27, BUTTON_COL, BUTTON_COL_H,
                                              BUTTON_COL_P, 16, lambda: self.start_minigame('ct'), self.display, 'Chop Tree'))
        self.mini_games_buttons.append(Button(1198, 554, 150, 27, BUTTON_COL, BUTTON_COL_H,
                                              BUTTON_COL_P, 16, lambda: self.start_minigame('ms'), self.display, 'Mining Stone'))
        self.mini_games_buttons.append(Button(1198, 527, 150, 27, BUTTON_COL, BUTTON_COL_H,
                                              BUTTON_COL_P, 16, lambda: self.start_minigame('ah'), self.display, 'Animal Hunt'))



    def start_minigame(self, minigame):
        current_time = pygame.time.get_ticks()
        if minigame == 'ah':
            self.animal_hunt.start_new_game(current_time)
            self.game_state_manager.set_state('Animal Hunt')
        elif minigame == 'ct':
            self.chop_tree.start_new_game(current_time)
            self.game_state_manager.set_state('Chop Tree')
        elif minigame == 'ms':
            self.mining_stone.start_new_game(current_time)
            self.game_state_manager.set_state('Mining Stone')

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


    def show_mini_games(self):
        self.mini_games_menu_active = not self.mini_games_menu_active

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
        self.display.blit(self.st_frame, (250, 470))

        self.worker_timer.update(current_time)

        if self.data.education >= 75:
            self.data.buffs.append('High Efficiency')
            if 'Low Efficiency' in self.data.debuffs:
                self.data.debuffs.remove('Low Efficiency')
        elif self.data.education <= 25:
            self.data.debuffs.append('Low Efficiency')
            if 'High Efficiency' in self.data.buffs:
                self.data.buffs.remove('High Efficiency')

        if self.worker_timer.has_finished():
            if 'High Efficiency' in self.data.buffs:
                self.data.wood += self.data.lumberjacks * 2
                self.data.stone += self.data.miners * 2
                self.data.food += self.data.hunters * 2
            elif 'Low Efficiency' in self.data.debuffs:
                self.data.wood += self.data.lumberjacks // 2
                self.data.stone += self.data.miners // 2
                self.data.food += self.data.hunters // 2
            else:
                self.data.wood += self.data.lumberjacks
                self.data.stone += self.data.miners
                self.data.food += self.data.hunters
            if self.data.food >= self.data.food_storage:
                self.data.food = self.data.food_storage

        self.basic_resources_timer.update(current_time)

        if self.basic_resources_timer.has_finished():
            self.data.food = max(0, self.data.food - self.data.people // 5)
            self.data.water = max(0, self.data.water - self.data.people // 2)
            # print(f'Food: {self.data.food}')
            # print(f'Water: {self.data.water}')

        # print(f'Stability: {self.calculate_stability()}')

        self.town_development_timer.update(current_time)

        if self.town_development_timer.has_finished():
            # Education
            if self.data.schools < self.data.people // 100:
                self.data.education = max(0, self.data.education - 1)
            elif self.data.schools == self.data.people // 100:
                pass
            else:
                self.data.education = min(100, self.data.education + 1)
            # Safety
            if self.data.guard_houses < self.data.people // 100:
                self.data.guard_houses = max(0, self.data.safety - 1)
            elif self.data.guard_houses == self.data.people // 100:
                pass
            else:
                self.data.safety = min(100, self.data.safety + 1)
            # Health
            if self.data.hospitals < self.data.people // 100:
                self.data.hospitals = max(0, self.data.health - 1)
            elif self.data.hospitals == self.data.people // 100:
                pass
            else:
                self.data.health = min(100, self.data.health + 1)

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

        self.mining_stone_cooldown_timer.update(current_time)

        if self.mining_stone_cooldown_timer.has_finished():
            self.mining_stone_active = True

        if self.mining_stone.game_finished:
            self.mining_stone_cooldown_timer.start(MINING_STONE_COOLDOWN_TIME, current_time)
            self.mining_stone_active = False
            self.mining_stone.game_finished = False

        self.text_list[1].update_msg(f':{self.data.wood}')
        self.text_list[2].update_msg(f':{self.data.stone}')
        self.text_list[3].update_msg(f':{self.data.food}')
        self.text_list[4].update_msg(f':{self.data.water}')
        self.text_list[6].update_msg(f"Dwellers: {self.data.people}")
        self.text_list[7].update_msg(f"Education: {self.data.education}")
        self.text_list[8].update_msg(f"Safety: {self.data.safety}")
        self.text_list[9].update_msg(f"Health: {self.data.health}")

        for t in self.text_list:
            t.draw()

        for b in self.button_list:
            b.check_inp(mouse_pos)
            b.draw()

        for index, l in enumerate(self.log):
            l.draw((100, 365 - (50 * index)))

        self.progressbar.draw()

        self.simulation.run(events)

        if self.mini_games_menu_active:
            for b in self.mini_games_buttons:
                b.check_inp(mouse_pos)
                b.draw()

        if self.calculate_stability() == 1:
            self.display.blit(self.gui_icon_sad, (266, 486))
        elif self.calculate_stability() == 2:
            self.display.blit(self.gui_icon_avg, (266, 486))
        elif self.calculate_stability() == 3:
            self.display.blit(self.gui_icon_h, (266, 486))
        elif self.calculate_stability() == 4:
            self.display.blit(self.gui_icon_sh, (266, 486))

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
                if event.key == pygame.K_f:
                    if self.mining_stone_active:
                        self.mining_stone.start_new_game(current_time)
                        self.game_state_manager.set_state('Mining Stone')
                if event.key == pygame.K_c:
                    self.data.wood = 9999
                    self.data.stone = 9999
                    self.data.food = self.data.food_storage
                    self.data.water = self.data.water_storage
            for b in self.button_list:
                b.click(event)
            for b in self.mini_games_buttons:
                b.click(event)