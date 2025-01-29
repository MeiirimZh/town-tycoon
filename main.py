import sys
import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scenes.town import Town
from scenes.store import Store
from data import Data


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game_state_manager = GameStateManager('Town')
        self.data = Data()
        self.town = Town(self.screen, self.game_state_manager, self.data)
        self.store = Store(self.screen, self.game_state_manager, self.data)
        self.states = {'Town': self.town, 'Store': self.store}

        pygame.display.set_caption("Town Tycoon")

    def run(self):
        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.states[self.game_state_manager.get_state()].run(events)

            pygame.display.update()
            self.clock.tick(FPS)


class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.current_state = state


if __name__ == '__main__':
    game = Game()
    game.run()
