import pygame
import random

from scripts.timer import Timer


class Town:
    def __init__(self, display, game_state_manager, data):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data

        self.timer = Timer(True)
        self.timer.start(1, 0)

    def run(self, events):
        current_time = pygame.time.get_ticks()

        self.display.fill('blue')

        self.timer.update(current_time)

        if self.timer.has_finished():
            self.data.wood += 1
            print(self.data.wood)

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
