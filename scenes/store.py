import pygame

from config import BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P, images
from scripts.textandbuttons import Text, Button
from scripts.hlayout import HLayout


class Store:
    def __init__(self, display, game_state_manager, data):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data

        self.title = Text(32, 'STORE', (255, 255, 255), (631, 20), self.display)

        self.upgrade_buttons = [Button(40, 200, 100, 30, BUTTON_COL, BUTTON_COL_H,
                                BUTTON_COL_P, 16, lambda: self.upgrade_wood_click_value(), self.display, "UPGRADE"),
                                Button(40, 200, 100, 30, BUTTON_COL, BUTTON_COL_H,
                                BUTTON_COL_P, 16, lambda: self.upgrade_stone_click_value(), self.display, "UPGRADE")]

        self.upgrade_text = [Text(20, '50 wood: +1 wood per click', (255, 255, 255), (40, 200), self.display),
                             Text(20, '100 stone: +1 stone per click', (255, 255, 255), (40, 250), self.display)]

        self.upgrade_wood_layout = HLayout([self.upgrade_text[0], self.upgrade_buttons[0]], self.display)
        self.upgrade_stone_layout = HLayout([self.upgrade_text[1], self.upgrade_buttons[1]], self.display)

        self.hire_buttons = [Button(200, 200, 100, 30, BUTTON_COL, BUTTON_COL_H,
                             BUTTON_COL_P, 16, lambda: self.hire_lumberjack(), self.display, "HIRE"),
                             Button(200, 200, 100, 30, BUTTON_COL, BUTTON_COL_H,
                             BUTTON_COL_P, 16, lambda: self.hire_miner(), self.display, "HIRE"),
                             Button(200, 200, 100, 30, BUTTON_COL, BUTTON_COL_H,
                             BUTTON_COL_P, 16, lambda: self.hire_hunter(), self.display, "HIRE")]

        self.hire_text = [Text(20, '300 wood: +1 lumberjack', (255, 255, 255), (750, 200), self.display),
                          Text(20, '500 stone: 1+ miner', (255, 255, 255), (750, 250), self.display),
                          Text(20, '100 food: +5 hunters', (255, 255, 255), (750, 300), self.display)]

        self.hire_lumberjack_layout = HLayout([self.hire_text[0], self.hire_buttons[0]], self.display)
        self.hire_miner_layout = HLayout([self.hire_text[1], self.hire_buttons[1]], self.display)
        self.hire_hunter_layout = HLayout([self.hire_text[2], self.hire_buttons[2]], self.display)

        self.info_text = [Text(16, 'Wood', (255, 255, 255), (1150, 700), self.display),
                          Text(16, 'Stone', (255, 255, 255), (1150, 720), self.display),
                          Text(16, 'Food', (255, 255, 255), (1150, 740), self.display)]

        self.bg = images['store_bg']
        self.btn_bg = images['button']

    def run(self, events):
        mouse_pos = pygame.mouse.get_pos()

        self.display.fill((136, 69, 53))

        self.title.draw()

        for button in self.upgrade_buttons:
            button.check_inp(mouse_pos)

        for button in self.hire_buttons:
            button.check_inp(mouse_pos)

        for text in self.upgrade_text:
            if 'wood' in text.msg:
                text.update_msg(f'{self.data.upgrade_wood_click_value_cost} wood: +{self.data.wood_click_value * 2 + 1 - self.data.wood_click_value} wood per click')
            if 'stone' in text.msg:
                text.update_msg(f'{self.data.upgrade_stone_click_value_cost} stone: +{self.data.stone_click_value * 2 + 1 - self.data.stone_click_value} stone per click')

        self.upgrade_wood_layout.draw(30)
        self.upgrade_stone_layout.draw(30)

        self.hire_lumberjack_layout.draw(30)
        self.hire_miner_layout.draw(30)
        self.hire_hunter_layout.draw(30)

        for text in self.info_text:
            text.draw()
            if 'Wood' in text.msg:
                text.update_msg(f'Wood: {self.data.wood}')
            if 'Stone' in text.msg:
                text.update_msg(f'Stone: {self.data.stone}')
            if 'Food' in text.msg:
                text.update_msg(f'Food: {self.data.food}')

        for event in events:
            for button in self.upgrade_buttons:
                button.click(event)
            for button in self.hire_buttons:
                button.click(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.game_state_manager.set_state('Town')

    def upgrade_wood_click_value(self):
        if self.data.wood >= self.data.upgrade_wood_click_value_cost:
            self.data.wood_click_value = self.data.wood_click_value * 2 + 1
            self.data.wood -= self.data.upgrade_wood_click_value_cost
            self.data.upgrade_wood_click_value_cost = self.data.upgrade_wood_click_value_cost * 2 + 100

    def upgrade_stone_click_value(self):
        if self.data.stone >= self.data.upgrade_stone_click_value_cost:
            self.data.stone_click_value = self.data.stone_click_value * 2 + 1
            self.data.stone -= self.data.upgrade_stone_click_value_cost
            self.data.upgrade_stone_click_value_cost = self.data.upgrade_stone_click_value_cost * 2 + 100

    def hire_lumberjack(self):
        if self.data.workers < self.data.people:
            if self.data.wood >= self.data.hire_lumberjack_cost:
                self.data.workers += 1
                self.data.lumberjacks += 1
                self.data.wood -= self.data.hire_lumberjack_cost

    def hire_miner(self):
        if self.data.workers < self.data.people:
            if self.data.stone >= self.data.hire_miner_cost:
                self.data.workers += 1
                self.data.miners += 1
                self.data.stone -= self.data.hire_miner_cost

    def hire_hunter(self):
        if self.data.workers < self.data.people:
            if self.data.food >= self.data.hire_hunter_cost:
                self.data.workers += 5
                self.data.hunters += 5
                self.data.food -= self.data.hire_hunter_cost
