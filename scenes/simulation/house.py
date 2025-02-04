from config import images


class House:
    def __init__(self, house_type, x, y):
        self.type = house_type
        self.x = x
        self.y = y

        self.img = images[house_type]

    def render(self, display, scroll):
        display.blit(self.img, (self.x + scroll[0], self.y + scroll[1]))
