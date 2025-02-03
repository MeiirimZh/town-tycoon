from scripts.textandbuttons import Text, Button
from scripts.utils import create_font


class HLayout:
    def __init__(self, elements, display):
        self.elements = elements
        self.display = display

    def draw(self, spacing):
        for i in range(1, len(self.elements)):
            if isinstance(self.elements[i], Text):
                if isinstance(self.elements[i-1], Text):
                    font = create_font(self.elements[i-1].size)
                    text = self.elements[i-1].msg
                    self.elements[i].update_pos((font.size(text)[0] + self.elements[i-1].position[0] + spacing,
                                                self.elements[i-1].position[1]))
                if isinstance(self.elements[i-1], Button):
                    self.elements[i].update_pos((self.elements[i-1].x + self.elements[i-1].width + spacing,
                                                self.elements[i-1].y))
            if isinstance(self.elements[i], Button):
                if isinstance(self.elements[i-1], Text):
                    font = create_font(self.elements[i - 1].size)
                    text = self.elements[i - 1].msg
                    self.elements[i].update_pos((font.size(text)[0] + self.elements[i-1].position[0] + spacing,
                                                 self.elements[i-1].position[1]))
                if isinstance(self.elements[i-1], Button):
                    self.elements[i].update_pos((self.elements[i-1].x + self.elements[i-1].width + spacing,
                                                self.elements[i-1].y))

        for element in self.elements:
            element.draw()
