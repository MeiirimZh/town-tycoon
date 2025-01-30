import pygame
import random

from scripts.timer import Timer


class AnimalHunt:
    def __init__(self, display, game_state_manager, data):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data

        self.timer = Timer()
        # self.timer.start(15, 0)

        self.positions = [(124, 39), (85, 359), (167, 618), (367, 199), (774, 132),
                          (683, 329), (583, 562), (1112, 39), (1097, 399), (956, 658)]

        self.animal_width = 200
        self.animal_height = 80

        self.animals = []

        self.reward = self.data.people // 5
        self.rounds = 0

        # self.generate_animals()

    def start_new_game(self, current_time):
        self.timer.start(15, current_time)
        self.generate_animals()
        self.rounds = 0

    def run(self, events):
        current_time = pygame.time.get_ticks()

        self.display.fill('green')

        self.timer.update(current_time)

        if self.timer.has_finished():
            self.game_state_manager.set_state('Town')

        for animal in self.animals:
            pygame.draw.rect(self.display, (255, 255, 255), animal)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for animal in self.animals:
                    if animal.collidepoint(mouse_pos):
                        self.animals.remove(animal)

        if len(self.animals) == 0:
            self.data.food += self.reward
            print(self.data.food)
            self.rounds += 1
            self.generate_animals()

    def generate_animals(self):
        random.shuffle(self.positions)

        self.animals = []

        for i in range(5):
            self.animals.append(pygame.Rect(self.positions[i][0], self.positions[i][1],
                                            self.animal_width, self.animal_height))
