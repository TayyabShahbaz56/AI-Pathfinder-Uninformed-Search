import matplotlib.pyplot as plt  # type: ignore
import matplotlib.colors as mcolors  # type: ignore
import matplotlib.patches as mpatches  # type: ignore

from grid_env import Grid


class GridGUI:
    """
    Simple Matplotlib based GUI for visualizing search on the grid.

    Each update completely redraws the matrix so that the animation is easy
    to follow and consistent across algorithms.
    """

    # softer, modern colour palette
    COLOR_MAP = {
        Grid.EMPTY: "#f4f4f4",        # light background
        Grid.WALL: "#ff4d4f",         # vivid static wall
        Grid.START: "#00b894",        # teal start (S)
        Grid.END: "#0984e3",          # blue target (T)
        Grid.FRONTIER: "#ffeaa7",     # yellow = frontier / to be expanded
        Grid.EXPLORED: "#a3e4d7",     # soft teal explored region
        Grid.PATH: "#00c96b",         # bright green path / visited route
    }

    def __init__(self, grid: Grid, title: str = "AIPathFinder"):
        self.grid = grid
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.title = title

        # build a fixed colormap for the discrete codes
        ordered_keys = sorted(self.COLOR_MAP.keys())
        self._bounds = ordered_keys
        self._cmap = mcolors.ListedColormap([self.COLOR_MAP[k] for k in ordered_keys])
        self._norm = mcolors.BoundaryNorm(self._bounds + [self._bounds[-1] + 1], self._cmap.N)

    def show_initial(self):
        """Show first frame without blocking the Python process."""
        self.update()
        plt.show(block=False)

    def block_until_closed(self):
        """Block the program until the plot window is closed."""
        plt.show()

    def update(self, pause: float = 0.1):
        self.ax.clear()
        # leave some extra vertical space at the top for the legend
        self.ax.set_title(self.title, fontsize=16, fontweight="bold", pad=20)
        # draw subtle grid lines, hide tick labels
        self.ax.set_xticks(range(self.grid.cols))
        self.ax.set_yticks(range(self.grid.rows))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        # thicker border and slightly darker outer background
        self.ax.grid(which="both", color="#bfbfbf", linewidth=0.8)
        self.ax.set_facecolor("#d9d9d9")
        self.ax.set_aspect("equal")

        # compact legend explaining cell roles; place it outside the grid on the right
        legend_handles = [
            mpatches.Patch(
                facecolor=self.COLOR_MAP[Grid.PATH],
                edgecolor="black",
                label="Visited path",
            ),
            mpatches.Patch(
                facecolor=self.COLOR_MAP[Grid.FRONTIER],
                edgecolor="black",
                label="Frontier (in queue)",
            ),
            mpatches.Patch(
                facecolor=self.COLOR_MAP[Grid.EXPLORED],
                edgecolor="black",
                label="Expanded / explored",
            ),
            mpatches.Patch(
                facecolor=self.COLOR_MAP[Grid.WALL],
                edgecolor="black",
                label="Static obstacle",
            ),
        ]
        self.ax.legend(
            handles=legend_handles,
            loc="upper right",
            bbox_to_anchor=(-0.02, 1.0),  # just outside the axes to the left
            ncol=1,
            frameon=False,
            fontsize=8,
        )

        vis = self.grid.grid
        # Use the discrete BoundaryNorm only; do NOT also pass vmin/vmax,
        # otherwise newer Matplotlib versions raise a ValueError.
        self.ax.imshow(vis, cmap=self._cmap, norm=self._norm)

        # numeric labels (visit order) and S/T marker so it looks like the assignment mockup
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell_code = self.grid.grid[r, c]
                visit_val = self.grid.visit_order[r, c]

                # numeric label for every cell
                if cell_code == Grid.WALL:
                    txt = "-1"
                elif cell_code == Grid.PATH:
                    # path cells are always labelled 0, as requested
                    txt = "0"
                else:
                    txt = str(visit_val) if visit_val >= 0 else "0"

                self.ax.text(
                    c,
                    r,
                    txt,
                    ha="center",
                    va="center",
                    color="black",
                    fontsize=10,
                )

                # overlays for start / end on top of cell colour
                if (r, c) == self.grid.start:
                    self.ax.text(
                        c,
                        r,
                        "S",
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=14,
                        fontweight="bold",
                    )
                if (r, c) == self.grid.end:
                    self.ax.text(
                        c,
                        r,
                        "T",
                        ha="center",
                        va="center",
                        color="white",
                        fontsize=14,
                        fontweight="bold",
                    )

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(pause)


