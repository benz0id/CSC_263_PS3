from typing import List, Tuple

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
        WHITE => Not visited.
        GREY => Visited.
        BLACK => Visited & completed. Completed is some condition defined
        by the algorithm.

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

