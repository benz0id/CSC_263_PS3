from typing import List, Tuple

from path_calculator.classes import Board, Settlement
"""

Contains functions required to parse an input file into a board.


Example input file.

# BEGIN
0@InPort@SP
1@Pallet@V
2@Viridian@V
3@Pewter@C
4@Cerulean@V
5@Vermilion@C
6@Lavender@V
7@OutPort@FP
==============
0: 1, 2, 3, 7
1: 0, 2
2: 0, 1, 4
3: 0, 5, 6
4: 5, 6, 7
5: 3, 4, 6
6: 3, 4, 5
7: 0, 4
# END
"""


class MisalignedParserError(Exception):
    """Raised when the parser becomes unaligned when reading input
    text."""
    pass


def extract_settlement(settlements: List[Settlement], line: str,
                       ind: int) -> None:
    """Extracts a settlement from the given <line>."""
    if '@' not in line:
        raise MisalignedParserError("Misaligned on line " + str(ind))

        # Extract data and construct Settlement object.
    s_id, name, s_type = line.split('@')
    settlements.append(Settlement(name, s_type))

    if not int(s_id) == len(settlements) - 1:
        raise MisalignedParserError("Misaligned on line " + str(ind))


def extract_roads(settlements: List[Settlement],
                 roads: List[Tuple[Settlement, Settlement]],
                 line: str, ind: int) -> None:
    """Extracts a road from the given <line>."""
    if ':' not in line:
        raise MisalignedParserError("Misaligned on line " + str(ind))

        # The settlement from which the roads 'leave'.
    out_sett_str = line[0]
    line = line[2:]
    out_sett = settlements[int(out_sett_str)]

    # The settlements to which out_sett is connected. Extract indices
    # and convert to settlements.
    in_sett_str = line.split(',')
    in_sett_strs = [s.strip() for s in in_sett_str]
    try:
        in_setts = [settlements[int(s)] for s in in_sett_strs]
    except IndexError:
        raise ValueError("Road to non-existent settlement requested")

    # Append in_sett - outsett roads to list of roads.
    for in_sett in in_setts:
        roads.append((out_sett, in_sett))


def parse_board(lines: List[str]) -> Board:
    """Parses an input (see example above for formatting) and returns it as a
    Board object."""

    for i, s in enumerate(lines):
        lines[i] = s.strip()

    # A list of settlement objects.
    settlements = []
    # A list of tuples of 2 settlements, representing a road.
    roads = []
    # Start in portion containing settlement info.
    mode = 'sett'

    # Iterate through lines, store data as we progress.
    for ind, line in enumerate(lines):
        # If we have an empty line, continue.
        if line == '' or '#' in line:
            continue
        # Multiple '=' demarcate region specifying roads.
        if '=' in line:
            mode = 'road'
            continue

        # This line contains a specification for a settlement.
        if mode == 'sett':
            extract_settlement(settlements, line, ind)

        # This line contains a specification for a road.
        else:
            extract_roads(settlements, roads, line, ind)

    # There may exist duplicate roads. Max 2n^2 to add.
    return Board(settlements, roads)
