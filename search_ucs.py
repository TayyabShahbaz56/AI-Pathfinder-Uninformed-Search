import heapq
from typing import Dict, Optional, Tuple, List

from grid_env import Grid
from view_gui import GridGUI
from search_utils import reconstruct_path

Node = Tuple[int, int]


def ucs(
    grid: Grid,
    gui: GridGUI,
    pause: float = 0.1,
) -> List[Node]:
    """
    Uniform-Cost Search with unit step cost (like Dijkstra's algorithm).
    """
    grid.clear_search_marks()
    start, goal = grid.start, grid.end

    pq: List[Tuple[int, Node]] = []
    heapq.heappush(pq, (0, start))

    parent: Dict[Node, Optional[Node]] = {start: None}
    cost_so_far: Dict[Node, int] = {start: 0}
    grid.mark_visit(start)

    while pq:
        current_cost, current = heapq.heappop(pq)
        if current not in (start, goal):
            grid.grid[current] = Grid.EXPLORED

        if current == goal:
            break

        for nbr in grid.neighbors(current):
            new_cost = current_cost + 1
            if nbr not in cost_so_far or new_cost < cost_so_far[nbr]:
                cost_so_far[nbr] = new_cost
                parent[nbr] = current
                grid.mark_visit(nbr)
                heapq.heappush(pq, (new_cost, nbr))
                if nbr not in (start, goal):
                    grid.grid[nbr] = Grid.FRONTIER

        gui.update(pause=pause)

    path = reconstruct_path(parent, start, goal)
    if not path:
        return []

    for node in path:
        if node not in (start, goal):
            grid.grid[node] = Grid.PATH
        gui.update(pause=pause)

    return path


