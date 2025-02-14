import pygame

from config import BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P
from scripts.textandbuttons import Text, Button


class MiniGameResultWindow:
    def __init__(self, x, y, width, height, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
        self.rect = pygame.Rect(x, y, width, height)

        self.title_text = Text(40, 'RESULT', (255, 255, 255), (608, 221), self.display)
        self.result_text = Text(24, '', (255, 255, 255), (535, 299), self.display)
        self.levels_text = Text(24, '', (255, 255, 255), (535, 329), self.display)

        self.button = Button(566, 387, 233, 50, BUTTON_COL, BUTTON_COL_H, BUTTON_COL_P, 20,
                             self.return_to_town, self.display, "RETURN TO TOWN")

    def set_results(self, result, result_value, level, level_value):
        self.result_text.update_msg(f'{result}: {result_value}')
        self.levels_text.update_msg(f'{level}: {level_value}')

    def draw(self, events):
        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(self.display, (93, 37, 37), self.rect)
        self.title_text.draw()
        self.result_text.draw()
        self.levels_text.draw()

        self.button.check_inp(mouse_pos)
        self.button.draw()

        for event in events:
            self.button.click(event)

    def return_to_town(self):
        pygame.mixer.music.load('music/terraria.mp3')
        pygame.mixer.music.play(-1)
        self.game_state_manager.set_state('Town')
