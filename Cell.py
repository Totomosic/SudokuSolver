import random

class Cell:
    def __init__(self, x, y, largeCellIndex, value = None):
        self.x = x
        self.y = y
        self.largeCellIndex = largeCellIndex
        self.value = value

    def has_value(self):
        return self.value != None

    def get_value(self):
        return self.value

    def to_string(self):
        if self.has_value():
            return str(self.get_value())
        return " "