from typing import Dict, List, Optional, Tuple

Node = Tuple[int, int]


def reconstruct_path(parent: Dict[Node, Optional[Node]], start: Node, goal: Node) -> List[Node]:
    """
    Rebuild the path from start to goal using the parent dictionary
    filled by the search algorithms.
    """
    if goal not in parent:
        return []

    path: List[Node] = []
    cur: Optional[Node] = goal
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = parent.get(cur)

    path.reverse()
    return path
