"""
AIPathFinder
============

Simple runner for the grid search visualisations.

Usage (from this folder):
    python main.py

You will be asked which uninformed search algorithm to run.
The GUI window will then animate how the algorithm explores the grid
and how the agent follows the path while reacting to dynamic walls.
"""

from grid_env import Grid
from view_gui import GridGUI
from search_bfs import bfs
from search_dfs import dfs
from search_ucs import ucs
from search_dls import dls
from search_iddfs import iddfs
from search_bidirectional import bidirectional_search


def choose_algorithm():
    print("AIPathFinder - Uninformed Search")
    print("Choose an algorithm:")
    print("  1) Breadth-First Search (BFS)")
    print("  2) Depth-First Search (DFS)")
    print("  3) Uniform-Cost Search (UCS)")
    print("  4) Depth-Limited Search (DLS)")
    print("  5) Iterative Deepening DFS (IDDFS)")
    print("  6) Bidirectional Search")

    choice = input("Enter 1-6: ").strip()
    return choice


def main():
    choice = choose_algorithm()

    # validate menu choice early; do not open any window if invalid
    valid_choices = {"1", "2", "3", "4", "5", "6"}
    if choice not in valid_choices:
        print("Error: invalid choice. Please run again and enter a number from 1 to 6.")
        return

    # Common environment
    grid = Grid(rows=8, cols=8)

    # Dynamic obstacles / re-planning have been disabled in this version,
    # so we no longer ask for a maximum number of dynamic walls.

    algo_name = {
        "1": "BFS",
        "2": "DFS",
        "3": "UCS",
        "4": "DLS",
        "5": "IDDFS",
        "6": "Bidirectional",
    }.get(choice, "BFS")

    gui = GridGUI(grid, title=f"AIPathFinder - {algo_name}")
    gui.show_initial()

    # Dynamic obstacles feature removed; set probability to 0 so
    # algorithms run on a purely static grid.
    dynamic_prob = 0.0
    pause = 0.15         # seconds between frames

    # Map the menu choice to the proper search function.
    # For DLS / IDDFS we wrap the function to provide the depth parameters.
    if choice == "1":
        search_fn = bfs
    elif choice == "2":
        search_fn = dfs
    elif choice == "3":
        search_fn = ucs
    elif choice == "4":
        depth_limit = 12

        def search_fn(g, gu, pause=pause):
            return dls(
                g,
                gu,
                depth_limit=depth_limit,
                pause=pause,
            )

    elif choice == "5":
        max_depth = 20

        def search_fn(g, gu, pause=pause):
            return iddfs(
                g,
                gu,
                max_depth=max_depth,
                pause=pause,
            )

    elif choice == "6":
        search_fn = bidirectional_search

    # First: run the chosen search algorithm to compute a path and draw the final path.
    path = search_fn(grid, gui, pause=pause)

    if not path:
        print("No path found - maybe walls completely block the target.")
        # Window stays open (opened with block=False), but code exits
        return

    print("Target reached successfully.")

    # Block so the final path is visible.
    gui.block_until_closed()


if __name__ == "__main__":
    main()


