
from path_calculator.input_parser import get_board, parse_board
from path_calculator.classes import Settlement, Board, START_PORT, FINISH_PORT, \
    VILLAGE, CITY, WHITE, GREY
import os

TEST_PATH = os.path.dirname(__file__) + '/../'
MAKE_BOARDS = False

# Template names for settlement construction
names = [
    'Pallet',
    'Viridian',
    'Pewter',
    'Cerulean',
    'Vermilion',
    'Lavender',
    'Celadon',
    'Fuchsia'
]


# A minimum board
min_setts = [
    Settlement(names[0], START_PORT),
    Settlement(names[1], FINISH_PORT)
]
min_roads = [(min_setts[0], min_setts[1]), (min_setts[1], min_setts[0])]


def test_min_board() -> None:
    board = Board(min_setts, min_roads)
    assert len(board._road_matrix) == 2

if MAKE_BOARDS:
    min_board = Board(min_setts, min_roads)

# A board with a single path to the final node.
single_path_board_str = [
    '0@InPort@SP',
    '1@Pallet@V',
    '2@Viridian@V',
    '3@Pewter@V',
    '4@Cerulean@V',
    '5@Vermilion@V',
    '6@Lavender@V',
    '7@OutPort@FP',
    '==============',
    '0: 1',
    '1: 2',
    '2: 3',
    '3: 4',
    '4: 5',
    '5: 6',
    '6: 7',
]
one_path_board = parse_board(single_path_board_str)

def test_one_path() -> None:
    assert len(one_path_board.get_all_roads()) == 7

# A simple board. The same structure as the one given in the example.
simple_board_str = [
    '0@start@SP',
    '1@A@V',
    '2@B@C',
    '3@C@V',
    '4@D@V',
    '5@end@FP',
    '==============',
    '0: 1',
    '1: 0, 2, 5',
    '2: 1, 3, 4, 5',
    '3: 2',
    '4: 2, 5',
    '5: 1, 2, 4'
]
simple_board = parse_board(simple_board_str)

def test_simple_board() -> None:
    # Ensure that the board has the correct number of unique edges.
    assert len(simple_board.get_all_roads()) == 7

# A simple board. The same structure as the one given in the example.
no_order_simple_board_str = [
    '0@start@SP',
    '1@A@V',
    '2@B@C',
    '3@C@V',
    '4@D@V',
    '5@end@FP',
    '==============',
    '0: 1',
    '1: 0, 2, 5',
    '2: 1, 3, 4, 5',
    '3: 2',
    '4: 2, 5',
    '5: 1, 2, 4'
]
no_order_simple_board = parse_board(simple_board_str)

def test_no_order_simple_board() -> None:
    # Ensure that the board has the correct number of unique edges.
    assert len(no_order_simple_board.get_all_roads()) == 7

# A board with maximum number of roads.
max_board_str = [
    '2@Viridian@V',
    '4@OutPort@FP',
    '1@Pallet@V',
    '3@Pewter@V',
    '0@InPort@SP',
    '==============',
    '2: 0, 1, 3, 4',
    '3: 0, 1, 2, 4',
    '4: 0, 1, 2, 3',
    '0: 1, 2, 3, 4',
    '1: 0, 2, 3, 4',
]
max_board_5 = parse_board(max_board_str)

def test_max_path() -> None:
    # Ensure that the board has the maximum number of unique edges.
    assert len(max_board_5.get_all_roads()) == \
           ((len(max_board_5.settlements) ** 2) -
            len(max_board_5.settlements)) / 2


# A board with a city linking two villages in an X formation
x_board_str = [
    '0@InPort@SP',
    '1@Pallet@V',
    '2@Viridian@V',
    '3@Pewter@V',
    '4@Cerulean@V',
    '5@Vermilion@V',
    '6@OutPort@FP',
    '==============',
    '0: 1, 2',
    '1: 0, 3',
    '2: 0, 3',
    '3: 1, 2, 4, 5',
    '4: 3, 6',
    '5: 3, 6',
    '6: 4, 5'
]
x_board = parse_board(x_board_str)

def test_board_input_from_file() -> None:
    """Tests that the program can handle board input from files."""
    board = get_board(TEST_PATH + 'tests/demo_input.txt')
    assert len(board.get_all_roads()) == 13
