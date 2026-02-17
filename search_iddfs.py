from typing import Dict, Optional, Tuple, List

from grid_env import Grid
from view_gui import GridGUI
from search_utils import reconstruct_path

Node = Tuple[int, int]


def _dls_step(
    grid: Grid,
    current: Node,
    goal: Node,
    depth_limit: int,
    parent: Dict[Node, Optional[Node]],
    gui: GridGUI,
    pause: float,
) -> bool:
    if current not in (grid.start, grid.end):
        grid.grid[current] = Grid.EXPLORED
    gui.update(pause=pause)

    if current == goal:
        return True
    if depth_limit == 0:
        return False

    for nbr in grid.neighbors(current):
        if nbr not in parent:
            parent[nbr] = current
            grid.mark_visit(nbr)
            if nbr not in (grid.start, grid.end):
                grid.grid[nbr] = Grid.FRONTIER
            gui.update(pause=pause)
            if _dls_step(
                    grid, nbr, goal, depth_limit - 1, parent, gui, pause
            ):
                return True
    return False


def iddfs(
    grid: Grid,
    gui: GridGUI,
    max_depth: int = 20,
    pause: float = 0.1,
) -> List[Node]:
    """
    Iterative Deepening Depth-First Search.
    """
    start, goal = grid.start, grid.end

    for depth in range(max_depth + 1):
        grid.clear_search_marks()
        parent: Dict[Node, Optional[Node]] = {start: None}
        grid.mark_visit(start)

        found = _dls_step(grid, start, goal, depth, parent, gui, pause)

        if found:
            path = reconstruct_path(parent, start, goal)
            if not path:
                return []

            for node in path:
                if node not in (start, goal):
                    grid.grid[node] = Grid.PATH
                gui.update(pause=pause)

            return path

    return []


