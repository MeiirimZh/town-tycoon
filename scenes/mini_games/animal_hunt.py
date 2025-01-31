import pygame
import random

from config import SCREENWIDTH, SCREENHEIGHT, images
from scripts.timer import Timer
from scripts.textandbuttons import Text, Button
from scripts.darken_background import DarkenBG
from scripts.mini_game_result_window import MiniGameResultWindow


class AnimalHunt:
    def __init__(self, display, game_state_manager, data):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data

        self.timer = Timer()

        self.positions = [(47, 144), (85, 359), (167, 618), (367, 199), (774, 132),
                          (683, 329), (583, 562), (1112, 39), (1097, 399), (956, 658)]

        self.animal_width = 200
        self.animal_height = 80

        self.animals = []

        self.reward = self.data.people // 5
        self.rounds = 0
        self.meat = 0

        self.text_list = [Text(24, 'Meat: 0', (255, 255, 255), (30, 30), self.display),
                          Text(24, 'Round: 1', (255, 255, 255), (30, 60), self.display)]

        self.darken_bg = DarkenBG(0, 0, SCREENWIDTH, SCREENHEIGHT, (0, 0, 0), (0, 0), (SCREENWIDTH, SCREENHEIGHT), 128)

        self.result_window = MiniGameResultWindow(513, 199, 340, 260, self.display, self.game_state_manager)

        self.crosshair = images['crosshair']
        self.crosshair_width = images['crosshair'].get_width()
        self.crosshair_height = images['crosshair'].get_height()

        self.game_finished = False

    def start_new_game(self, current_time):
        pygame.mixer.music.load('music/mini_games/Animal Hunt theme.mp3')
        pygame.mixer.music.play(-1)

        self.timer.start(20, current_time)
        self.generate_animals()
        self.meat = 0
        self.rounds = 0

    def run(self, events):
        mouse_pos = pygame.mouse.get_pos()

        current_time = pygame.time.get_ticks()

        self.display.fill('green')

        for t in self.text_list:
            t.draw()
            if 'Meat' in t.msg:
                t.update_msg(f'Meat: {self.meat}')
            elif 'Round' in t.msg:
                t.update_msg(f'Round: {self.rounds + 1}')

        self.timer.update(current_time)

        if self.timer.has_finished():
            self.darken_bg.draw(self.display)

            self.result_window.set_results('MEAT', self.meat, 'ROUNDS', self.rounds)
            self.result_window.draw(events)

            self.game_finished = True

            pygame.mouse.set_visible(True)
        else:
            for animal in self.animals:
                pygame.draw.rect(self.display, (255, 255, 255), animal)
            pygame.mouse.set_visible(False)
            self.display.blit(self.crosshair, (mouse_pos[0]-self.crosshair_width/2, mouse_pos[1]-self.crosshair_height/2))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for animal in self.animals:
                    if animal.collidepoint(mouse_pos):
                        self.animals.remove(animal)

        if len(self.animals) == 0:
            result = random.randint(self.reward - 10, self.reward + 10)

            self.meat += result
            self.data.food += result

            self.rounds += 1
            self.generate_animals()

    def generate_animals(self):
        random.shuffle(self.positions)

        self.animals = []

        for i in range(5):
            self.animals.append(pygame.Rect(self.positions[i][0], self.positions[i][1],
                                            self.animal_width, self.animal_height))
