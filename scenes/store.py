import pygame


class Store:
    def __init__(self, display, game_state_manager, data):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data

    def run(self, events):
        self.display.fill('red')

        for event in events:
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
                if event.key == pygame.K_q:
                    if self.data.wood >= self.data.upgrade_wood_click_value_cost:
                        self.data.wood_click_value = self.data.wood_click_value * 2 + 1
                        self.data.wood -= self.data.upgrade_wood_click_value_cost
                        self.data.upgrade_wood_click_value_cost = self.data.upgrade_wood_click_value_cost * 2 + 100
                if event.key == pygame.K_w:
                    if self.data.stone >= self.data.upgrade_stone_click_value_cost:
                        self.data.stone_click_value = self.data.stone_click_value * 2 + 1
                        self.data.stone -= self.data.upgrade_stone_click_value_cost
                        self.data.upgrade_stone_click_value_cost = self.data.upgrade_stone_click_value_cost * 2 + 100
