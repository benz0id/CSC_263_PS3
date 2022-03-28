import sys
from typing import List, Dict, Tuple


def main():
    """To be run upon execution of this script."""

    # Whether the found paths are to be printed. For debugging.
    print_paths = '-P' in sys.argv or '-p' in sys.argv
    file_path = sys.argv[1]

    board = get_board(file_path)
    find_and_print_paths(board, print_paths)


START_PORT = 'SP'
FINISH_PORT = 'FP'
VILLAGE = 'V'
CITY = 'C'

# Denotes that this settlement that can still be used in the growing path.
WHITE = 'W'
# Denotes that this settlement that cannot be used in the growing path.
GREY = 'G'
# Denotes that this settlement that cannot be used in a growing path and that
# a passport was used to traverse it.
BLACK = 'B'


class Settlement:
    """A class representing some kind of settlement on the board, connected by
    roads to some other settlement.

    === Public Attributes ===
    name:
        The name of this settlement.
    s_type:
        The type of settlement at this vertex, one of START_PORT, FINISH_PORT,
        VILLAGE, or CITY.
    colour:
        Used by algorithms to mark this node as visited or un-visited.
        WHITE => Visitable.
        GREY => Not visitable.
        BLACK => Not visitable and a passport was used to traverse this
        settlement.

    ID:
        The id of this node. Used for indexing purposes.
    """
    name: str
    s_type: str
    colour: str
    ID: int

    def __init__(self, name: str, s_type: str) -> None:
        """Initialises this vertex to a settlement with the given attributes.
        Must be inserted into a Graph in order to become functional. """
        self.name = name
        self.s_type = s_type
        self.colour = WHITE
        self.ID = -1

    def __str__(self) -> str:
        """Returns a string representation of this class."""
        return self.name + ': ' + str(self.ID)

    def __eq__(self, other) -> bool:
        """Returns whether <self> and <other> these are the same settlement."""
        cond1 = self.ID == other.ID
        cond2 = self.name == other.name
        cond3 = self.s_type == other.s_type
        return cond1 and cond2 and cond3

    def set_white(self) -> None:
        self.colour = WHITE

    def set_grey(self) -> None:
        self.colour = GREY

    def set_black(self) -> None:
        self.colour = BLACK

    def is_white(self) -> bool:
        return self.colour == WHITE

    def is_grey(self) -> bool:
        return self.colour == GREY

    def is_black(self) -> bool:
        return self.colour == BLACK

    def is_start(self) -> bool:
        return self.s_type == START_PORT

    def is_finish(self) -> bool:
        return self.s_type == FINISH_PORT

    def is_village(self) -> bool:
        return self.s_type == VILLAGE

    def is_city(self) -> bool:
        return self.s_type == CITY


class Board:
    """A class representing a game-ready board. Stores the settlements on the
    board and any roads between those settlements.

    === Public Attributes ===
    settlements:
        The settlements currently contained in the graph.

    start_port:
        The start port.

    === Private Attributes ===
    _max_set_id:
        The maximum settlement ID allocated.
        max_set_id == len(settlements) - 1

    _road_matrix:
        A 2x2 matrix that can be used to tell whether two settlements are
        connected by road. Indexing by the IDs of two settlements will return
        whether those two settlements are connected by a road. In order to
        eliminate redundancy and save space, one must index using the greater ID
        and then the smaller ID.
    """

    settlements: List[Settlement]
    start_port: Settlement
    _max_set_id: int
    _road_matrix: List[List[bool]]

    def __init__(self, settlements: List[Settlement],
                 roads: List[Tuple[Settlement, Settlement]]) -> None:
        """Initialises an empty board."""
        self._max_set_id = -1
        # Construct settlements.
        self.settlements = []
        self._init_settlements(settlements)

        # Construct roads.
        self._init_empty_road_matrix(self._max_set_id + 1)
        for road in roads:
            self.add_road(road[0], road[1])

        # Ensure no cities are adjacent.
        for i, row in enumerate(self._road_matrix):
            for j, is_road in enumerate(row):
                if is_road:
                    cond1 = settlements[i].s_type == CITY
                    cond2 = settlements[j].s_type == CITY
                    if cond1 and cond2:
                        raise ValueError('Two cities cannot be connected.')

    def _init_settlements(self, settlements: List[Settlement]) -> None:
        """Initialises the board with the given settlements. Clears the
        current settlements. """

        # Add all settlements and locate start port. Ensure that there exist
        # exactly one start and one finish port.
        start_found = False
        finish_found = False
        for sett in settlements:
            self.add_settlement(sett)

            # We've found a start port.
            if sett.s_type == START_PORT:
                self.set_start(sett)
                if start_found:
                    raise ValueError("Board can only contain one start port.")
                start_found = True

            # We've found a finish port.
            elif sett.s_type == FINISH_PORT:
                if finish_found:
                    raise ValueError("Board can only contain one finish port.")
                finish_found = True

        if not start_found or not finish_found:
            raise ValueError("Board must contain both a finish and start port.")

    def _init_empty_road_matrix(self, size: int) -> None:
        """Initialises an empty road matrix for a board of <size>."""
        self._road_matrix = []
        for i in range(size):
            self._road_matrix.append([])
            for j in range(0, i):
                self._road_matrix[i].append(False)

    def get_size(self) -> int:
        """Gets the size of this board."""
        return len(self.settlements)

    def get_all_roads(self) -> List[Tuple[Settlement, Settlement]]:
        """Returns all roads on this board without duplicates."""
        roads = []
        for i, row in enumerate(self._road_matrix):
            for j, is_road in enumerate(row):
                if is_road:
                    roads.append((self.settlements[i], self.settlements[j]))
        return roads

    def set_start(self, sett: Settlement) -> None:
        """Sets <sett> as the start port."""
        if sett.s_type != START_PORT:
            raise ValueError("Settlement must be a start port.")
        if sett not in self.settlements:
            self.add_settlement(sett)
        self.start_port = sett

    def add_settlement(self, sett: Settlement) -> None:
        """Adds <sett> to the list of settlements."""
        self._max_set_id += 1
        sett.ID = self._max_set_id
        self.settlements.append(sett)

    def are_adjacent(self, sett1: Settlement, sett2: Settlement) -> bool:
        """Returns whether the given settlements are neighbors."""
        min_id, max_id = sorted((sett1.ID, sett2.ID))
        return self._road_matrix[max_id][min_id]

    def add_road(self, sett1: Settlement, sett2: Settlement) -> None:
        """Adds a road connecting <sett1> to <sett2>, which must both already
        exist in the graph."""
        if sett1.ID == sett2.ID:
            raise ValueError("Settlements cannot have roads to themselves."
                             "Offending nodes: " + str(sett1) + str(sett2))
        min_id, max_id = sorted((sett1.ID, sett2.ID))
        self._road_matrix[max_id][min_id] = True

    def get_adjacent_settlements(self, sett: Settlement) -> List[Settlement]:
        """Takes a <sett> in this graph and returns all settlements to which it
        is adjacent."""
        setts = []
        i = 0
        # Checking row in road matrix.
        while i < sett.ID:
            if self._road_matrix[sett.ID][i]:
                setts.append(self.settlements[i])
            i += 1
        i += 1
        # Checking column in road matrix.
        while i <= self._max_set_id:
            if self._road_matrix[i][sett.ID]:
                setts.append(self.settlements[i])
            i += 1
        return setts

    def get_white_neighbors(self, sett: Settlement) -> List[Settlement]:
        """Returns all white, non-start neighbors of the given settlement."""
        neighbors = self.get_adjacent_settlements(sett)
        white_neighbors = []
        for neighbor in neighbors:
            if neighbor.is_white() and not neighbor.is_start():
                white_neighbors.append(neighbor)
        return white_neighbors

    def get_grey_village_neighbors(self, sett: Settlement) -> List[Settlement]:
        """Returns all adjacent nodes of the given settlement that are grey
        villages."""
        neighbors = self.get_adjacent_settlements(sett)
        grey_villages = []
        for neighbor in neighbors:
            if neighbor.is_grey() and neighbor.is_village():
                grey_villages.append(neighbor)
        return grey_villages


class MisalignedParserError(Exception):
    """Raised when the parser becomes unaligned when reading input
    text."""
    pass


def extract_settlement(settlements: Dict[int, Settlement], line: str,
                       ind: int) -> None:
    """Extracts a settlement from the given <line>."""
    if '@' not in line:
        raise MisalignedParserError("Misaligned on line " + str(ind))

        # Extract data and construct Settlement object.
    s_id, name, s_type = line.split('@')
    settlements[int(s_id)] = (Settlement(name, s_type))


def extract_roads(settlements: Dict[int, Settlement],
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

    # A list of settlement objects. id: Settlement.
    settlements = {}
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

    # Extract settlements.
    settlement_list = list(settlements.values())

    # There may exist duplicate roads. Max 2n^2 to add.
    return Board(settlement_list, roads)


def get_board(fp: str) -> Board:
    """Extracts the board from the specification file at the given filepath."""
    fp = fp.strip()

    # Extract file contents and filter a bit.
    with open(fp, 'r') as txt_file:
        lines = txt_file.readlines()
    for i, s in enumerate(lines):
        lines[i] = s.strip()

    return parse_board(lines)


class PathFinder:
    """Finds all given paths from the start port to the end port given some
    traversal specifications.

    === Private Attributes ===
    _mode:
        Specifies the flavour of traversal algorithm to be used when finding
        paths to the end port.
    _passport_used:
        Whether the passport has been used on the currently traversed path.
        Only used when mode = 3.
    _num_paths_found:
        The number of paths found up at any given point during the running of
        the algorithm.
    _board:
        The board being traversed.

    _record_paths:
        Whether paths should be recorded.
    _cur_path:
        The current path.
    _paths:
        To be used for debugging. Stores the settlements along the paths found.
    """

    _mode: int
    _passport_used: bool
    _num_paths_found: int
    _board: Board

    _record_paths: bool
    _cur_path: List[Settlement]
    _paths: List[List[Settlement]]

    def __init__(self, board: Board, mode: int,
                 record_paths: bool = False) -> None:
        """Initialises a pathfinder ready to find all paths through the given
        <board>. Will only traverse the board according to the rules
        specified by <mode>. """
        self._board = board
        self._passport_used = False
        self._num_paths_found = 0
        self._mode = mode
        self._record_paths = record_paths
        self._cur_path = []
        self._paths = []

    def find_num_paths(self) -> int:
        """Returns the number of paths from the start port to the finish port
        using the given traversal rules."""
        start_port = self._board.start_port
        self._depth_first_walk_along(start_port)
        rtrn = self._num_paths_found
        self._num_paths_found = 0
        return rtrn

    def get_paths(self) -> Tuple[int, List[List[Settlement]]]:
        """Returns the number of paths from the start port to the finish port
        using the given traversal rules. Also returns the contents of each path.
        To be used for debugging."""
        self._record_paths = True
        num_paths = self.find_num_paths()
        rtrn = num_paths, self._paths
        self._record_paths = False
        self._cur_path = []
        self._paths = []
        return rtrn

    def _depth_first_walk_along(self, sett: Settlement) -> None:
        """From the current <sett>, recursively traverse every allowable path
        to the finish port. Increment counter whenever a new path is found."""
        # Add this node to the current path.
        if self._record_paths:
            self._cur_path.append(sett)

        # We've reached the finish port. This path is complete.
        if sett.is_finish():
            self._num_paths_found += 1
            if self._record_paths:
                self._paths.append(self._cur_path[:])
                self._cur_path.pop()
            return

        # Don't return to this settlement in future traversals.
        if self._mode == 1:
            sett.set_grey()
        elif sett.is_village() and sett.is_white():
            sett.set_grey()
        # A passport was used to traverse this node.
        elif sett.is_grey():
            sett.set_black()

        # Recurse to each adjacent vertex that isn't grey.
        for adj_sett in self._board.get_white_neighbors(sett):
            self._depth_first_walk_along(adj_sett)

        # Try to use the passport if it's available.
        self._try_to_use_passport(sett)

        # We've completed traversing this settlement along this path.
        # Update its colour to mark it as available.
        if sett.is_grey():
            sett.set_white()
        if sett.is_black():
            sett.set_grey()

        # Remove this settlement from the current path.
        if self._record_paths:
            self._cur_path.pop()

    def _try_to_use_passport(self, sett: Settlement) -> None:
        """If the passport hasn't already been used along this path, will
        attempt to use the passport to traverse into an adjacent grey village.
        Will only do so if mode = 3."""
        # We can't use the passport.
        if self._mode != 3 or self._passport_used:
            return

        # Use passport to traverse into each allowable adjacent settlement.
        # Update passport status.
        adj_setts = self._board.get_grey_village_neighbors(sett)
        self._passport_used = True
        for adj_sett in adj_setts:
            self._depth_first_walk_along(adj_sett)
        self._passport_used = False


def paths_to_str(paths: List[List[Settlement]]) -> str:
    """Prints a string representation of the paths found by the given <pf>."""
    rtrn = ''
    for i, path in enumerate(paths):
        s = '    Path ' + str(i) + ': '
        for sett in path:
            s += str(sett) + ' -> '
        s = s[:-4] + '\n\n'
        rtrn += s

    return rtrn


def find_and_print_paths(board: Board, print_paths: bool) -> None:
    """Finds all the given paths along a board and prints a string
    representation of the results. Will print the paths found iff
    <print_paths>."""

    # Compute and print for each mode.
    for mode in (1, 2, 3):
        pf = PathFinder(board, mode, record_paths=print_paths)

        # Include traversed paths if requested.
        if not print_paths:
            # Default settings.
            num_found = pf.find_num_paths()
            print('MODE {i}: {n}'.format(i=mode, n=num_found))
        else:
            num_found, paths = pf.get_paths()
            print('MODE {i}: {n}'.format(i=mode, n=num_found))
            print(paths_to_str(paths))


if __name__ == '__main__':
    main()
