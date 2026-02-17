from typing import Dict, Optional, Tuple, List

from grid_env import Grid
from view_gui import GridGUI
from search_utils import reconstruct_path

Node = Tuple[int, int]


def _recursive_dls(
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
            if _recursive_dls(
                grid, nbr, goal, depth_limit - 1, parent, gui, pause
            ):
                return True
    return False


def dls(
    grid: Grid,
    gui: GridGUI,
    depth_limit: int,       
    pause: float = 0.1,
) -> List[Node]:
    """
    Depth-Limited Search (recursive DFS up to a given depth).
    """
    grid.clear_search_marks()
    start, goal = grid.start, grid.end

    parent: Dict[Node, Optional[Node]] = {start: None}
    grid.mark_visit(start)

    found = _recursive_dls(grid, start, goal, depth_limit, parent, gui, pause)

    if not found:
        return []

    path = reconstruct_path(parent, start, goal)
    if not path:
        return []

    for node in path:
        if node not in (start, goal):
            grid.grid[node] = Grid.PATH
        gui.update(pause=pause)

    return path


