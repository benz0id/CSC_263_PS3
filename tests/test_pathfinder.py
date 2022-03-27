from path_calculator.find_paths import PathFinder
from tests.test_board_construction import max_board_5, one_path_board, \
    simple_board



def test_simple_board() -> None:
    """Tests that the correct number of paths are found on a simple setting for
    each of the three modes."""
    pf = PathFinder(simple_board, 1)
    assert pf.find_paths() == 3

    pf = PathFinder(simple_board, 2)
    assert pf.find_paths() == 8

    pf = PathFinder(simple_board, 3)
    assert pf.find_paths() == 39
