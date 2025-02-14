import sys
import pygame

from config import SCREENWIDTH, SCREENHEIGHT, FPS
from scenes.town import Town
from scenes.store import Store
from scenes.mini_games.animal_hunt import AnimalHunt
from scenes.mini_games.chop_tree import ChopTree
from scenes.mini_games.mining_stone import MiningStone
from scripts import utils
from data import Data


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.game_state_manager = GameStateManager('Town')
        self.data = utils.load()
        self.store = Store(self.screen, self.game_state_manager, self.data)
        self.animal_hunt = AnimalHunt(self.screen, self.game_state_manager, self.data)
        self.chop_tree = ChopTree(self.screen, self.game_state_manager, self.data)
        self.mining_stone = MiningStone(self.screen, self.game_state_manager, self.data)
        self.town = Town(self.screen, self.game_state_manager, self.data, self.animal_hunt,
                         self.chop_tree, self.mining_stone)
        self.states = {'Town': self.town, 'Store': self.store,
                       'Animal Hunt': self.animal_hunt, 'Chop Tree': self.chop_tree, 'Mining Stone': self.mining_stone}

        pygame.display.set_caption("Town Tycoon")

    def run(self):
        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    utils.save(self.data)
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
