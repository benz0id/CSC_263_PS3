from typing import List, Tuple
from path_calculator.classes import Board, Settlement


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
        The number of paths found up at any given point during the running of the
        algorithm.
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

    def __init__(self, board: Board, mode: int) -> None:
        """Initialises a pathfinder ready to find all paths through the given
        <board>. Will only traverse the board according to the rules
        specified by <mode>. """
        self._board = board
        self._passport_used = False
        self._num_paths_found = 0
        self._mode = mode
        self._record_paths = False
        self._cur_path = []
        self._paths = []

    def find_paths(self) -> int:
        """Returns the number of paths from the start port to the finish port
        using the given traversal rules."""
        start_port = self._board.start_port
        self._depth_first_walk_along(start_port)
        rtrn = self._num_paths_found
        self._num_paths_found = 0
        return rtrn

    def _get_paths(self) -> Tuple[int, List[List[Settlement]]]:
        """Returns the number of paths from the start port to the finish port
        using the given traversal rules. Also returns the contents of each path.
        To be used for debugging."""
        self._record_paths = True
        num_paths = self.find_paths()
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
