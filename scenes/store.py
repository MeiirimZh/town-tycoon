import pygame


class Store:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager

    def run(self, events):
        self.display.fill('red')

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.game_state_manager.set_state('Town')
