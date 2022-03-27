import pytest
from tests.test_board_construction import max_board_5, one_path_board, \
    simple_board


@pytest.mark.parametrize('board', [
    one_path_board,
    simple_board,
    max_board_5
    ]
                         )
def test_neighborhood(board) -> None:
    """Tests that all vertecies in a given graphs neightborhood are adjacent."""
    for vertex in board.settlements:
        neighbors = board.get_adjacent_settlements(vertex)

        # Neighbor => Adjacent
        for neighbor in neighbors:
            assert board.are_adjacent(vertex, neighbor)

        other_vertecies = board.settlements[:]
        other_vertecies.remove(vertex)

        # not Neighbor => not Adjacent
        for other_vertex in other_vertecies:
            if other_vertex not in neighbors:
                assert not board.are_adjacent(vertex, other_vertex)



