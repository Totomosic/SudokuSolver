from Cell import Cell

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
                allowedValues = [x for x in range(1, self.totalDim + 1)]
                disallowedValues = self.get_row_values(cell.y) + self.get_col_values(cell.x) + self.get_large_cell_values(cell.largeCellIndex)
                for value in disallowedValues:
                    if value in allowedValues:
                        allowedValues.remove(value)
                matrix.append(allowedValues)
        return matrix

    def naive_solve(self):
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
        print("Done solving")