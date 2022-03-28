from path_calculator.Routes import PathFinder
from tests.test_board_construction import max_board_5, one_path_board, \
    simple_board


def vis_paths(pf: PathFinder) -> None:
    """Prints a string representation of the paths found by the given <pf>."""
    num, paths = pf.get_paths()
    print(num)

    for path in paths:
        s = ''
        for sett in path:
            s += str(sett) + ' -> '
        s = s[:-4] + '\n'
        print(s)


pf = PathFinder(simple_board, 1)
vis_paths(pf)

pf = PathFinder(simple_board, 2)
vis_paths(pf)

pf = PathFinder(simple_board, 3)
vis_paths(pf)
