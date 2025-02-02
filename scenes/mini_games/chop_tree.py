import pygame
import random


class ChopTree:
    def __init__(self, display, game_state_manager, data):
        self.display = display
        self.game_state_manager = game_state_manager
        self.data = data

        self.parts = [pygame.Rect(583, 109, 100, 50)]
        self.target = None

        for i in range(9):
            self.parts.append(pygame.Rect(583, self.parts[-1].y+50, 100, 50))

        self.axe = pygame.Rect(790, 109, 200, 50)
        self.detect_rect = pygame.Rect(583, 109, 100, 50)
        self.axe_pos = 109

        self.direction = 1

    def start_new_game(self):
        self.generate_target()

    def run(self, events):
        self.display.fill('green')

        pygame.draw.rect(self.display, (255, 255, 255), self.axe)

        if self.axe.y == 109:
            self.direction = 1
        elif self.axe.y == 559:
            self.direction = -1

        self.axe.y += 5 * self.direction
        self.detect_rect.y = self.axe.y

        for part in self.parts:
            pygame.draw.rect(self.display, (125, 28, 28), part)

        pygame.draw.rect(self.display, (255, 255, 0), self.target)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.target.colliderect(self.detect_rect):
                        self.generate_target()

    def generate_target(self):
        self.target = random.choice(self.parts)
