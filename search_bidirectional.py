from collections import deque
from typing import Dict, Optional, Tuple, List

from grid_env import Grid
from view_gui import GridGUI

Node = Tuple[int, int]


def _reconstruct_meeting_path(
    parent_start: Dict[Node, Optional[Node]],
    parent_goal: Dict[Node, Optional[Node]],
    meet: Node,
    start: Node,
    goal: Node,
) -> List[Node]:
    # path from start -> meet
    path_start: List[Node] = []
    cur: Optional[Node] = meet
    while cur is not None:
        path_start.append(cur)
        if cur == start:
            break
        cur = parent_start.get(cur)
    path_start.reverse()

    # path from meet -> goal
    path_goal: List[Node] = []
    cur = parent_goal.get(meet)
    while cur is not None:
        path_goal.append(cur)
        if cur == goal:
            break
        cur = parent_goal.get(cur)

    return path_start + path_goal


def bidirectional_search(
    grid: Grid,
    gui: GridGUI,
    pause: float = 0.1,
) -> List[Node]:
    """
    Bidirectional BFS from start and goal simultaneously.
    """
    grid.clear_search_marks()
    start, goal = grid.start, grid.end

    q_start: deque[Node] = deque([start])
    q_goal: deque[Node] = deque([goal])

    parent_start: Dict[Node, Optional[Node]] = {start: None}
    parent_goal: Dict[Node, Optional[Node]] = {goal: None}
    grid.mark_visit(start)
    grid.mark_visit(goal)

    visited_start = {start}
    visited_goal = {goal}

    meet: Optional[Node] = None

    while q_start and q_goal and meet is None:
        # expand from start side
        for _ in range(len(q_start)):
            current = q_start.popleft()
            if current not in (start, goal):
                grid.grid[current] = Grid.EXPLORED
            if current in visited_goal:
                meet = current
                break
            for nbr in grid.neighbors(current):
                if nbr not in visited_start:
                    visited_start.add(nbr)
                    parent_start[nbr] = current
                    grid.mark_visit(nbr)
                    if nbr not in (start, goal):
                        grid.grid[nbr] = Grid.FRONTIER
                    q_start.append(nbr)

        if meet is not None:
            break

        # expand from goal side
        for _ in range(len(q_goal)):
            current = q_goal.popleft()
            if current not in (start, goal):
                grid.grid[current] = Grid.EXPLORED
            if current in visited_start:
                meet = current
                break
            for nbr in grid.neighbors(current):
                if nbr not in visited_goal:
                    visited_goal.add(nbr)
                    parent_goal[nbr] = current
                    grid.mark_visit(nbr)
                    if nbr not in (start, goal):
                        grid.grid[nbr] = Grid.FRONTIER
                    q_goal.append(nbr)

        gui.update(pause=pause)

    if meet is None:
        return []

    path = _reconstruct_meeting_path(parent_start, parent_goal, meet, start, goal)

    for node in path:
        if node not in (start, goal):
            grid.grid[node] = Grid.PATH
        gui.update(pause=pause)

    return path


