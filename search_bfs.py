from collections import deque
from typing import Dict, Optional, Tuple, List

from grid_env import Grid
from view_gui import GridGUI
from search_utils import reconstruct_path

Node = Tuple[int, int]


def bfs(
    grid: Grid,
    gui: GridGUI,
    pause: float = 0.1,
) -> List[Node]:
    """
    Breadth-First Search (unit cost, shortest number of steps).
    Returns the discovered path from start to end (including both).
    """
    grid.clear_search_marks()
    start, goal = grid.start, grid.end

    q: deque[Node] = deque()
    q.append(start)
    parent: Dict[Node, Optional[Node]] = {start: None}
    grid.mark_visit(start)

    while q:
        current = q.popleft()
        if current not in (start, goal):
            grid.grid[current] = Grid.EXPLORED

        if current == goal:
            break

        for nbr in grid.neighbors(current):
            if nbr not in parent:
                parent[nbr] = current
                grid.mark_visit(nbr)
                if nbr not in (start, goal):
                    grid.grid[nbr] = Grid.FRONTIER
                q.append(nbr)

        gui.update(pause=pause)

    path = reconstruct_path(parent, start, goal)
    if not path:
        return []

    # mark final path
    for node in path:
        if node not in (start, goal):
            grid.grid[node] = Grid.PATH
        gui.update(pause=pause)

    return path


