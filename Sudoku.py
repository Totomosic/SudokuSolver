from Cell import Cell
import copy
import random

class Sudoku:
    def __init__(self, largeCellDim):
        self.largeCellsDim = largeCellDim
        self.smallCellsDim = largeCellDim
        self.totalDim = self.largeCellsDim * self.smallCellsDim
        self.cells = []
        for ly in range(self.largeCellsDim):
            for y in range(self.smallCellsDim):
                for lx in range(self.largeCellsDim):                
                    for x in range(self.smallCellsDim):
                        xIndex = x + lx * self.smallCellsDim
                        yIndex = y + ly * self.smallCellsDim
                        self.cells.append(Cell(xIndex, yIndex, int(lx + ly * self.largeCellsDim)))

    def get_all_cells(self):
        return self.cells
        
    def get_cell(self, x, y):
        return self.cells[int(x) + int(y) * self.totalDim]

    def get_row(self, row):
        cells = []
        for x in range(self.totalDim):
            cells.append(self.get_cell(x, row))
        return cells

    def get_col(self, col):
        cells = []
        for y in range(self.totalDim):
            cells.append(self.get_cell(col, y))
        return cells

    def get_large_cell(self, cellIndex):
        cells = []
        for cell in self.cells:
            if cell.largeCellIndex == cellIndex:
                cells.append(cell)
        return cells

    def get_row_values(self, row):
        values = []
        for cell in self.get_row(row):
            values.append(cell.value)
        return values

    def get_col_values(self, col):
        values = []
        for cell in self.get_col(col):
            values.append(cell.value)
        return values

    def get_large_cell_values(self, cellIndex):
        values = []
        for cell in self.get_large_cell(cellIndex):
            values.append(cell.value)
        return values

    def is_solved(self):
        for cell in self.cells:
            if cell.value == None:
                return False
        return True
    
    def is_row_solved(self, row):
        for cell in self.get_row(row):
            if cell.value == None:
                return False
        return True

    def is_col_solved(self, col):
        for cell in self.get_col(col):
            if cell.value == None:
                return False
        return True

    def is_large_cell_solved(self, cellIndex):
        for cell in self.get_large_cell(cellIndex):
            if cell.value == None:
                return False
        return True

    def get_available_values_of_cell(self, cell):
        allowedValues = [x for x in range(1, self.totalDim + 1)]
        disallowedValues = self.get_row_values(cell.y) + self.get_col_values(cell.x) + self.get_large_cell_values(cell.largeCellIndex)
        for value in disallowedValues:
            if value in allowedValues:
                allowedValues.remove(value)
        return allowedValues

    def get_missing_values_from_cells(self, cells):
        missingValues = [x for x in range(1, self.totalDim + 1)]
        for cell in cells:
            if cell.value in missingValues:
                missingValues.remove(cell.value)
        return missingValues

    def initialize(self, fileData):
        index = 0
        for y in range(self.totalDim):
            for x in range(self.totalDim):
                value = fileData[index]
                if value == "-":
                    value = None
                else:
                    value = int(value)
                self.get_cell(x, y).value = value
                index += 1

    def to_string(self):
        result = ""
        for y in range(self.totalDim):
            for x in range(self.totalDim):
                result += self.get_cell(x, y).to_string()
            result += '\n'
        return result

    def to_string_formatted(self):
        result = ""
        for ly in range(self.largeCellsDim):
            for y in range(self.smallCellsDim):
                for lx in range(self.largeCellsDim):                
                    for x in range(self.smallCellsDim):
                        xIndex = x + lx * self.smallCellsDim
                        yIndex = y + ly * self.smallCellsDim
                        result += self.get_cell(xIndex, yIndex).to_string() + " "
                    result += "| "
                result += '\n'
            for tx in range(self.smallCellsDim * self.largeCellsDim + self.largeCellsDim):
                result += '--'
            result += '\n'
        return result

    def print_board(self):
        print(self.to_string_formatted())

    def get_possible_values_matrix(self):
        matrix = []
        for cell in self.get_all_cells():
            if cell.value != None:
                matrix.append(None)
            else:
                matrix.append(self.get_available_values_of_cell(cell))
        return matrix

    def solve_possible_values(self):
        shouldContinue = True
        while shouldContinue:
            matrix = self.get_possible_values_matrix()
            found = False
            index = 0
            for values in matrix:
                if values != None:
                    if len(values) == 1:
                        self.cells[index].value = values[0]
                        found = True
                index += 1
            shouldContinue = found

    def solve_cells(self, cells):
        missingValues = self.get_missing_values_from_cells(cells)
        for value in missingValues:
            potentialCells = []
            for cell in cells:
                if cell.value == None:
                    availableCellValues = self.get_available_values_of_cell(cell)
                    if value in availableCellValues:
                        potentialCells.append(cell)
            if len(potentialCells) == 1:
                potentialCells[0].value = value
                self.solve_cells(cells)
                return

    def solve_rows(self):
        for row in range(self.totalDim):
            self.solve_cells(self.get_row(row))

    def solve_cols(self):
        for col in range(self.totalDim):
            self.solve_cells(self.get_col(col))

    def solve_large_cells(self):
        for c in range(self.largeCellsDim * self.largeCellsDim):
            self.solve_cells(self.get_large_cell(c))

    def get_possible_guesses_from_cells(self, cells):
        minNum = 100
        guesses = []
        for cell in cells:
            if cell.value == None:
                availableValues = self.get_available_values_of_cell(cell)
                if len(availableValues) <= minNum:
                    minNum = len(availableValues)
                    for val in availableValues:
                        guesses.append([cell.x, cell.y, val])
        return guesses

    def make_guess(self, guess):
        self.get_cell(guess[0], guess[1]).value = guess[2]

    def try_solve(self):
        count = 0
        while not self.is_solved() and count < 10:
            self.solve_possible_values()
            self.solve_rows()
            self.solve_cols()
            self.solve_large_cells()
            count += 1

    def solve(self):
        self.try_solve()
        if not self.is_solved():
            state = copy.deepcopy(self.cells)
            remainingGuesses = self.get_possible_guesses_from_cells(state)
            while not self.is_solved() and len(remainingGuesses) > 0:
                self.cells = copy.deepcopy(state)
                guess = remainingGuesses[random.randint(0, len(remainingGuesses) - 1)]
                print("Making guess", guess)
                self.make_guess(guess)   
                remainingGuesses.remove(guess)      
                self.try_solve()
            