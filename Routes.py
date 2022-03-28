import sys

from path_calculator.classes import *
from path_calculator.input_parser import *
from path_calculator.pathfinder import *

# REPLACE WITH ACTUAL CODE IN THOSE FILES IN THAT IMPORT ORDER BEFORE SUBMISION

def main():
    """To be run upon execution of this script."""

    # Whether the found paths are to be printed. For debugging.
    print_paths = '-P' in sys.argv or '-p' in sys.argv
    file_path = sys.argv[1]

    board = get_board(file_path)
    find_and_print_paths(board, print_paths)

if __name__ == '__main__':
    main()













