import pygame

class Progressbar:
    def __init__(self, display, coords, time, length, loop=True):
        self.display = display
        self.coords = coords 
        self.time = time 
        self.length = length 
        self.loop = loop
        self.current_length = 0  
        self.pixel_per_frame = self.length / (self.time * 60)

    def draw(self):
        pygame.draw.rect(self.display, (0, 0, 0), (self.coords[0], self.coords[1], self.length, 5))

        progress = self.current_length / self.length
        red = int(255 * (1 - progress))
        green = int(255 * progress)

        pygame.draw.rect(self.display, (red, green, 0), (self.coords[0], self.coords[1], self.current_length, 5))

        if self.loop:
            if self.current_length >= self.length:
                self.current_length = 0
            self.current_length += self.pixel_per_frame
        else:
            if self.current_length < self.length:
                self.current_length += self.pixel_per_frame
    
    def reset(self):
        self.current_length = 0
