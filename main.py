'''
Takes input file representing unfilled sudoku using '-' for missing squares
'''
import sys
import math
from Sudoku import Sudoku

def determine_sudoku_dimensions(file_data):
    length = len(file_data)
    dim = int(math.sqrt(length))
    if dim * dim != length:
        print("Sudoku was not a square")
        return 0
    return dim

def main(input_file, output_file):
    with open(input_file, "r") as f:
        iFileData = f.read()
        iFileData = iFileData.replace("\n", "")
        dimension = determine_sudoku_dimensions(iFileData)
        largeCells = int(math.sqrt(dimension))
        board = Sudoku(largeCells)
        board.initialize(iFileData)
        board.print_board()
        board.solve()
        board.print_board()

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print("Usage: python main.py input_file output_file")
    else:    
        main(args[1], args[2])