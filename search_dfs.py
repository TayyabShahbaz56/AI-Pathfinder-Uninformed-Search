from typing import Dict, Optional, Tuple, List

from grid_env import Grid
from view_gui import GridGUI
from search_utils import reconstruct_path

Node = Tuple[int, int]


def dfs(
    grid: Grid,
    gui: GridGUI,
    pause: float = 0.1,
) -> List[Node]:
    """
    Depth-First Search using an explicit stack.
    """
    grid.clear_search_marks()
    start, goal = grid.start, grid.end

    stack: List[Node] = [start]
    parent: Dict[Node, Optional[Node]] = {start: None}
    grid.mark_visit(start)

    while stack:
        current = stack.pop()
        if current not in (start, goal):
            grid.grid[current] = Grid.EXPLORED

        if current == goal:
            break

        # push neighbours in reverse order so the first in movement order is expanded first
        neighbours = list(grid.neighbors(current))
        neighbours.reverse()
        for nbr in neighbours:
            if nbr not in parent:
                parent[nbr] = current
                grid.mark_visit(nbr)
                if nbr not in (start, goal):
                    grid.grid[nbr] = Grid.FRONTIER
                stack.append(nbr)

        gui.update(pause=pause)

    path = reconstruct_path(parent, start, goal)
    if not path:
        return []

    for node in path:
        if node not in (start, goal):
            grid.grid[node] = Grid.PATH
        gui.update(pause=pause)

    return path


