import sys
import pygame

from config import SCREENWIDTH, SCREENHEIGHT, FPS
from scenes.town import Town
from scenes.store import Store
from scenes.mini_games.animal_hunt import AnimalHunt
from data import Data


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.game_state_manager = GameStateManager('Town')
        self.data = Data()
        self.town = Town(self.screen, self.game_state_manager, self.data)
        self.store = Store(self.screen, self.game_state_manager, self.data)
        self.animal_hunt = AnimalHunt(self.screen, self.game_state_manager, self.data)
        self.states = {'Town': self.town, 'Store': self.store, 'Animal Hunt': self.animal_hunt}

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
