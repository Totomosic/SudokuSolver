from Cell import Cell

class Sudoku:
    def __init__(self, largeCellDim, smallCellDim):
        self.largeCellDim = largeCellDim
        self.smallCellDim = smallCellDim
        self.cells = []
        index = 0
        for y in range(self.get_dimension()):
            for x in range(self.get_dimension()):
                self.cells.append(Cell(x, y, int(x / self.smallCellDim) + int(y / self.smallCellDim) * self.largeCellDim))
                index += 1

    def get_dimension(self):
        return self.largeCellDim * self.smallCellDim

    def get_cell(self, x, y):
        return self.cells[int(x + y * self.get_dimension())]

    def get_row_values(self, row):
        values = []
        for x in range(self.get_dimension()):
            values.append(self.get_cell(x, row).get_value())
        return values
        
    def get_col_values(self, col):
        values = []
        for y in range(self.get_dimension()):
            values.append(self.get_cell(col, y).get_value())
        return values
    
    def get_large_cell_values(self, cellIndex):
        values = []
        for y in range(int(cellIndex / self.largeCellDim) * self.smallCellDim, int(cellIndex / self.largeCellDim) * self.smallCellDim + self.smallCellDim):
            for x in range(cellIndex % self.largeCellDim * self.smallCellDim, cellIndex % self.largeCellDim * self.smallCellDim + self.smallCellDim):
                print(cellIndex, x, y)
                values.append(self.get_cell(x, y).get_value())
        return values

    def get_all_cells(self):
        return self.cells

    def initialize(self, filedata):
        index = 0
        for y in range(self.get_dimension()):
            for x in range(self.get_dimension()):
                num = filedata[index]
                if num == "-":
                    num = None
                else:
                    num = int(num)
                self.get_cell(x, y).value = num
                index += 1

    def to_string(self):
        result = ""
        for y in range(self.get_dimension()):
            for x in range(self.get_dimension()):
                result += self.get_cell(x, y).to_string() + " "
            result += "\n"
        return result

    def to_string_formatted(self):
        result = ""
        for largeY in range(self.largeCellDim):
            for smallY in range(self.smallCellDim):
                for largeX in range(self.largeCellDim):
                    for smallX in range(self.smallCellDim):
                        y = largeY * self.largeCellDim + smallY
                        x = largeX * self.largeCellDim + smallX
                        result += self.get_cell(x, y).to_string() + " "
                    result += "| "
                result += "\n"
            for t in range(self.largeCellDim * self.smallCellDim + self.largeCellDim):
                result += "--"
            result += "\n"
        return result

    def print_board(self):
        print(self.to_string_formatted())

    def solve(self):
        cells = self.get_all_cells()
        
    def get_possible_values_matrix(self):
        matrix = []
        for cell in self.get_all_cells():
            if cell.has_value():
                matrix.append(None)
            else:
                allowedValues = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                disallowedValues = self.get_row_values(cell.y) + self.get_col_values(cell.x) + self.get_large_cell_values(cell.largeCellIndex)
                for val in disallowedValues:
                    if val in allowedValues:
                        allowedValues.remove(val)
                matrix.append(allowedValues)
        return matrix 