import os
from Routes import *
from pathlib import Path
import operator as op
from functools import reduce
from math import perm


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2


# V1
def cal_routes_mode_2(num_vil: int) -> int:
    num = 1
    for i in range(1, num_vil + 1):
        added = perm(num_vil, i)
        num += int(added)
    return num


def cal_routes_mode_3(num_vil: int) -> int:
    num = 1
    for i in range(1, num_vil + 1):
        added = perm(num_vil, i) * (1 + (i * (i + 1) / 2))
        num += int(added)
    return num


TEST_PATH = Path(os.path.dirname(__file__))
TEST_BOARDS_PATHS = TEST_PATH / 'test_boards'
print(os.listdir(TEST_BOARDS_PATHS))

# Filename (excluding .txt) to paths found in each of the three modes.
file_to_paths = {}


names_expected = {
    'simple_board': (3, 8, 39),
    'one_city': (1, 1, 1),
    'isolated
    # '1_c-2_v': (1, cal_routes_mode_2(2), cal_routes_mode_3(2)),
    # '1_c-3_v': (1, cal_routes_mode_2(3), cal_routes_mode_3(3)),
    # '1_c-4_v': (1, cal_routes_mode_2(4), cal_routes_mode_3(4)),
    # '1_c-5_v': (1, cal_routes_mode_2(5), cal_routes_mode_3(5))
    # '1_c-10_v': (1, 2 ** 10, cal_routes(10))
}


def test_all_files_scores() -> None:
    """Tests that all files contain boards with specified values."""

    for test_file_path in os.listdir(TEST_BOARDS_PATHS):
        board = get_board(str(TEST_BOARDS_PATHS / test_file_path))
        print(str(test_file_path) + ":")
        file_to_paths[test_file_path[:-4]] = find_and_print_paths(board, False)

    for key in names_expected.keys():
        assert file_to_paths[key] == names_expected[key]





