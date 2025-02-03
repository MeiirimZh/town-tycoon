import pygame

from config import BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P
from scripts.textandbuttons import Text, Button
from scripts.hlayout import HLayout


class Store:
    def __init__(self, display, game_state_manager, data):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data

        self.title = Text(32, 'STORE', (255, 255, 255), (631, 20), self.display)
        self.upgrade_buttons = [Button(40, 200, 100, 30, BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P, 16, lambda: print('hello'),
                                       self.display, "UPGRADE")]
        self.upgrade_text = [Text(20, '25 wood: +1 wood per click', (255, 255, 255), (40, 200), self.display)]

        self.upgrade_wood_layout = HLayout([self.upgrade_text[0], self.upgrade_buttons[0]], self.display)

    def run(self, events):
        mouse_pos = pygame.mouse.get_pos()

        self.display.fill((136, 69, 53))

        self.title.draw()

        for button in self.upgrade_buttons:
            button.check_inp(mouse_pos)

        self.upgrade_wood_layout.draw(30)

        for event in events:
            for button in self.upgrade_buttons:
                button.click(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.game_state_manager.set_state('Town')
                if event.key == pygame.K_z:
                    print(f'Wood: {self.data.wood}')
                    print(f'Stone: {self.data.stone}')
                if event.key == pygame.K_x:
                    print(f'Wood click value: {self.data.wood_click_value}')
                    print(f'Stone click value: {self.data.stone_click_value}')
                if event.key == pygame.K_v:
                    print(f'Upgrade wood click value: {self.data.upgrade_wood_click_value_cost}')
                    print(f'Upgrade stone click value: {self.data.upgrade_stone_click_value_cost}')
                    print(f'Hire lumberjack: {self.data.hire_lumberjack_cost}')
                    print(f'Hire miner: {self.data.hire_miner_cost}')
                if event.key == pygame.K_q:
                    pass
                if event.key == pygame.K_w:
                    if self.data.stone >= self.data.upgrade_stone_click_value_cost:
                        self.data.stone_click_value = self.data.stone_click_value * 2 + 1
                        self.data.stone -= self.data.upgrade_stone_click_value_cost
                        self.data.upgrade_stone_click_value_cost = self.data.upgrade_stone_click_value_cost * 2 + 100
                if event.key == pygame.K_e:
                    if self.data.wood >= self.data.hire_lumberjack_cost:
                        self.data.lumberjacks += 1
                        self.data.wood -= self.data.hire_lumberjack_cost
                if event.key == pygame.K_r:
                    if self.data.stone >= self.data.hire_miner_cost:
                        self.data.miners += 1
                        self.data.stone -= self.data.hire_miner_cost

    def upgrade_wood_click_value(self):
        if self.data.wood >= self.data.upgrade_wood_click_value_cost:
            self.data.wood_click_value = self.data.wood_click_value * 2 + 1
            self.data.wood -= self.data.upgrade_wood_click_value_cost
            self.data.upgrade_wood_click_value_cost = self.data.upgrade_wood_click_value_cost * 2 + 100
