import numpy as np  # type: ignore


class Grid:
    """
    Represents the environment grid (static walls).

    Cell codes (kept intentionally simple for visualization):
    -  0: empty
    - -1: static wall
    -  1: start
    -  2: target
    -  3: frontier (in open list)
    -  4: explored (already expanded)
    -  5: final path
    """

    EMPTY = 0
    WALL = -1
    START = 1
    END = 2
    FRONTIER = 3
    EXPLORED = 4
    PATH = 5

    def __init__(self, rows: int = 8, cols: int = 8):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        
        self.visit_order = np.full((rows, cols), -1, dtype=int)
        self._visit_counter = 0
    
        self.max_dynamic_walls: int | None = None

    
        self.start = (3, 5)
        self.end = (5, 1)

        # make a vertical wall in the middle
        self.static_walls = [(i, 3) for i in range(1, 7)]
        self.dynamic_walls = set()

        self.reset()

    # ------------------------------------------------------------------
    # basic helpers
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """
        Reset all non-wall markings (frontier / explored / path) but keep
        static walls and the current start/end positions.
        """
        self.grid.fill(self.EMPTY)
        self.visit_order.fill(-1)
        self._visit_counter = 0

        # static walls
        for r, c in self.static_walls:
            self.grid[r, c] = self.WALL

        # start / end
        sr, sc = self.start
        er, ec = self.end
        self.grid[sr, sc] = self.START
        self.grid[er, ec] = self.END

    def clear_search_marks(self) -> None:
        """Remove FRONTIER / EXPLORED / PATH marks from the grid."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r, c] in (self.FRONTIER, self.EXPLORED, self.PATH):
                    self.grid[r, c] = self.EMPTY
                # clear any visit labels for next run
                if self.visit_order[r, c] >= 0 and self.grid[r, c] == self.EMPTY:
                    self.visit_order[r, c] = -1
        
        sr, sc = self.start
        er, ec = self.end
        self.grid[sr, sc] = self.START
        self.grid[er, ec] = self.END
        # mark start node as first in visit order
        self.mark_visit(self.start)

    def in_bounds(self, node) -> bool:
        r, c = node
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_free(self, node) -> bool:
        """Walkable for the agent (explored/frontier/path are all walkable)."""
        r, c = node
        # A cell is free if it is not a static wall
        return self.grid[r, c] != self.WALL

    def neighbors(self, node):
        """
        Clockwise movement order:

        1. Up
        2. Right
        3. Bottom
        4. Bottom-Right (diagonal)
        5. Left
        6. Top-Left (diagonal)

        """
        r, c = node
        moves = [
            (-1, 0),   # up
            (0, 1),    # right
            (1, 0),    # bottom
            (1, 1),    # bottom-right (main diagonal)
            (0, -1),   # left
            (-1, -1),  # top-left (main diagonal)
        ]
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            nxt = (nr, nc)
            if self.in_bounds(nxt) and self.is_free(nxt):
                yield nxt

   

    # ------------------------------------------------------------------
    # visit order helpers (for numeric labels in GUI)
    # ------------------------------------------------------------------
    def mark_visit(self, node) -> None:
        """Assign a unique incremental id the first time a node is discovered."""
        r, c = node
        if self.visit_order[r, c] == -1:
            self.visit_order[r, c] = self._visit_counter
            self._visit_counter += 1


