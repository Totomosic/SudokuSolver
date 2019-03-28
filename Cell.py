import random

class Cell:
    def __init__(self, x, y, largeCellIndex, value = None):
        self.x = x
        self.y = y
        self.largeCellIndex = largeCellIndex
        self.value = value

    def to_string(self):
        if self.value != None:
            return str(self.value)
        return " "