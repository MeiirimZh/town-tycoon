import pygame
import random

from collections import deque

from config import *

from scripts.timer import Timer
from scripts.textandbuttons import Text, Button
from scripts.utils import get_quarter, get_section, save
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

        self.people_timer = Timer(True)
        self.people_timer.start(5, 0)

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
        self.text_list.append(Text(16, f"Education: {self.data.education}", (104, 19, 240), (45, 560), self.display))
        self.text_list.append(Text(16, f"Safety: {self.data.safety}", (104, 19, 240), (45, 580), self.display))
        self.text_list.append(Text(16, f"Health: {self.data.health}", (104, 19, 240), (45, 600), self.display))

        self.health_buff = ""
        self.ed_buff = ""
        self.guard_buff = ""

        self.text_list.append(Text(16, self.health_buff, (255, 255, 255), (730, 630), self.display))
        self.text_list.append(Text(16, self.ed_buff, (255, 255, 255), (730, 670), self.display))
        self.text_list.append(Text(16, self.guard_buff, (255, 255, 255), (730, 710), self.display))

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

        self.button_list.append(Button(1218, 635, 130, 27, BUTTON_COL, BUTTON_COL_H,
                                       BUTTON_COL_P, 16, lambda: self.game_state_manager.set_state('Store'), self.display, 'STORE'))

        self.button_list.append(Button(1218, 662, 130, 27, BUTTON_COL, BUTTON_COL_H,
                                       BUTTON_COL_P, 16, self.quit_and_save, self.display, 'QUIT'))

        self.mini_games_menu_active = False
        self.mini_games_buttons = []
        self.mini_games_buttons.append(Button(1148, 581, 200, 27, BUTTON_COL, BUTTON_COL_H,
                                              BUTTON_COL_P, 16, lambda: self.start_minigame('ct'), self.display, 'Chop Tree'))
        self.mini_games_buttons.append(Button(1148, 554, 200, 27, BUTTON_COL, BUTTON_COL_H,
                                              BUTTON_COL_P, 16, lambda: self.start_minigame('ms'), self.display, 'Mining Stone'))
        self.mini_games_buttons.append(Button(1148, 527, 200, 27, BUTTON_COL, BUTTON_COL_H,
                                              BUTTON_COL_P, 16, lambda: self.start_minigame('ah'), self.display, 'Animal Hunt'))

        self.base_upgrade_wood_click_value_cost = 50
        self.base_upgrade_stone_click_value_cost = 100

        self.base_hire_lumberjack_cost = 300
        self.base_hire_miner_cost = 500
        self.base_hire_hunter_cost = 100

    def quit_and_save(self):
        save(self.data)
        pygame.quit()

    def start_minigame(self, minigame):
        current_time = pygame.time.get_ticks()
        if minigame == 'ah':
            if self.animal_hunt_active:
                self.animal_hunt.start_new_game(current_time)
                self.game_state_manager.set_state('Animal Hunt')
        elif minigame == 'ct':
            if self.chop_tree_active:
                self.chop_tree.start_new_game(current_time)
                self.game_state_manager.set_state('Chop Tree')
        elif minigame == 'ms':
            if self.mining_stone_active:
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

        if "Perfect Health" in self.data.buffs:
            self.health_buff = "Perfect Health"
        elif "Pandemic" in self.data.debuffs:
            self.health_buff = "Pandemic"
        else:
            self.health_buff = ""
        
        if "High Efficiency" in self.data.buffs:
            self.ed_buff = "High Efficiency"
        elif "Low Efficiency" in self.data.debuffs:
            self.ed_buff = "Low Efficiency"
        else:
            self.ed_buff = ""
        
        if "Good Reputation" in self.data.buffs:
            self.guard_buff = "Good Reputation"
        elif "Smooth Criminal" in self.data.debuffs:
            self.guard_buff = "Smooth Criminal"
        else:
            self.guard_buff = ""


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
            if 'High Efficiency' not in self.data.buffs:
                self.data.buffs.append('High Efficiency')
            if 'Low Efficiency' in self.data.debuffs:
                self.data.debuffs.remove('Low Efficiency')
        elif self.data.education <= 25:
            if 'Low Efficiency' not in self.data.debuffs:
                self.data.debuffs.append('Low Efficiency')
            if 'High Efficiency' in self.data.buffs:
                self.data.buffs.remove('High Efficiency')

        if self.data.health >= 75:
            if 'Perfect Health' not in self.data.buffs:
                self.data.buffs.append('Perfect Health')
            if 'Pandemic' in self.data.debuffs:
                self.data.debuffs.remove('Pandemic')
        elif self.data.health <= 25:
            if 'Pandemic' not in self.data.debuffs:
                self.data.debuffs.append('Pandemic')
            if 'Perfect Health' in self.data.buffs:
                self.data.buffs.remove('Perfect Health')

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

        self.people_timer.update(current_time)

        if self.people_timer.has_finished():
            if 'Perfect Health' in self.data.buffs:
                self.data.people += 1
            elif 'Pandemic' in self.data.debuffs:
                self.data.people -= 1

        if self.data.safety >= 75:
            if 'Good Reputation' not in self.data.buffs:
                self.data.buffs.append('Good Reputation')
            if 'Smooth Criminal' in self.data.debuffs:
                self.data.debuffs.remove('Smooth Criminal')
        elif self.data.safety <= 25:
            if 'Smooth Criminal' not in self.data.debuffs:
                self.data.debuffs.append('Smooth Criminal')
            if 'Good Reputation' in self.data.buffs:
                self.data.buffs.remove('Good Reputation')

        if 'Good Reputation' in self.data.buffs:
            self.data.price_multiplier = 0.5
        elif 'Smooth Criminal' in self.data.debuffs:
            self.data.price_multiplier = 1.5
        else:
            self.data.price_multiplier = 1.0

        self.data.upgrade_wood_click_value_cost = self.base_upgrade_wood_click_value_cost * self.data.price_multiplier
        self.data.upgrade_stone_click_value_cost = self.base_upgrade_stone_click_value_cost * self.data.price_multiplier
        self.data.hire_lumberjack_cost = self.base_hire_lumberjack_cost * self.data.price_multiplier
        self.data.hire_miner_cost = self.base_hire_miner_cost * self.data.price_multiplier
        self.data.hire_hunter_cost = self.base_hire_hunter_cost * self.data.price_multiplier

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
        self.text_list[10].update_msg(self.health_buff)
        self.text_list[11].update_msg(self.ed_buff)
        self.text_list[12].update_msg(self.guard_buff)

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
            self.simulation.can_scroll = False
            for b in self.mini_games_buttons:
                b.check_inp(mouse_pos)
                if 'Chop Tree' in b.text:
                    if self.chop_tree_cooldown_timer.time_left() == 0:
                        b.text = 'Chop Tree: OK'
                    else:
                        b.text = f'Chop Tree: {self.chop_tree_cooldown_timer.time_left()}'
                elif 'Mining Stone' in b.text:
                    if self.mining_stone_cooldown_timer.time_left() == 0:
                        b.text = 'Mining Stone: OK'
                    else:
                        b.text = f'Mining Stone: {self.mining_stone_cooldown_timer.time_left()}'
                elif 'Animal Hunt' in b.text:
                    if self.animal_hunt_cooldown_timer.time_left() == 0:
                        b.text = 'Animal Hunt: OK'
                    else:
                        b.text = f'Animal Hunt: {self.animal_hunt_cooldown_timer.time_left()}'
                b.draw()
        else:
            self.simulation.can_scroll = True

        if self.calculate_stability() == 1:
            self.display.blit(self.gui_icon_sad, (266, 486))
        elif self.calculate_stability() == 2:
            self.display.blit(self.gui_icon_avg, (266, 486))
        elif self.calculate_stability() == 3:
            self.display.blit(self.gui_icon_h, (266, 486))
        elif self.calculate_stability() == 4:
            self.display.blit(self.gui_icon_sh, (266, 486))

        for event in events:
            for b in self.button_list:
                b.click(event)
            for b in self.mini_games_buttons:
                b.click(event)
