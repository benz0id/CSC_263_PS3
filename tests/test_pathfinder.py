from path_calculator.pathfinder import PathFinder
from tests.test_board_construction import *

def test_one_path_board() -> None:
    """Tests that the correct number of paths are found for a simple board."""
    board = one_path_board
    pf = PathFinder(board, 1)
    assert pf.find_num_paths() == 1

    pf = PathFinder(board, 2)
    assert pf.find_num_paths() == 1

    pf = PathFinder(board, 3)
    assert pf.find_num_paths() == 1

def test_simple_board() -> None:
    """Tests that the correct number of paths are found on a simple setting for
    each of the three modes."""
    board = simple_board
    pf = PathFinder(board, 1)
    assert pf.find_num_paths() == 3

    pf = PathFinder(board, 2)
    assert pf.find_num_paths() == 8

    pf = PathFinder(board, 3)
    assert pf.find_num_paths() == 39

def test_simple_board() -> None:
    """Tests that the correct number of paths are found on a cross setting for
    each of the three modes."""
    board = x_board
    pf = PathFinder(board, 1)
    assert pf.find_num_paths() == 2

    pf = PathFinder(board, 2)
    assert pf.find_num_paths() == 4

    pf = PathFinder(board, 3)
    assert pf.find_num_paths() == 4



