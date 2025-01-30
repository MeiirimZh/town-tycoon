import pygame
import math
import time
import random
from config import *


class Fire:
    def __init__(self, color, iterations, display):
        self.color = color
        self.iterations = iterations
        self.display = display

    def draw(self):
        for i in range(1, self.iterations + 1):
            new_color = []
            for j in self.color:
                new_color.append(min(255, math.ceil(j / (i * 3))))

            height_var = int(30 * (math.sin(time.time())))

            pygame.draw.rect(
                self.display,
                tuple(new_color),
                pygame.Rect(0, SCREENWIDTH + 50 - i * 50 - height_var, SCREENHEIGHT, 50)
            )


class Particle:
    def __init__(self, x, y, color, velocity, lifetime) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifetime = lifetime
        self.init_lifetime = lifetime
        self.size = random.randint(1, 4)

        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.surface.fill(color)

    def update(self):
        self.y -= self.velocity

        fade_factor = max(0, self.lifetime / self.init_lifetime)
        alpha = int((fade_factor / 2) * 255)

        self.surface.set_alpha(alpha)

        self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))


color_list = [(255, 0, 0), (255, 100, 0), (0, 0, 0)]


class ParticleSystem:
    def __init__(self, display) -> None:
        self.particles = []
        self.display = display

    def add_particle(self):
        part = Particle(random.randint(0, SCREENWIDTH), SCREENHEIGHT - 10, random.choice(color_list), random.randint(1, 2),
                        random.randint(200, 300))
        self.particles.append(part)

    def draw(self):
        for p in self.particles:
            p.update()

        self.particles = [p for p in self.particles if p.is_alive()]

        for particle in self.particles:
            particle.draw(self.display)