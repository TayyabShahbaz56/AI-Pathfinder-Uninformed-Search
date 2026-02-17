# AI-Pathfinder-Uninformed-Search

> A step-by-step animated pathfinding visualizer implementing 6 uninformed search algorithms on a dynamic grid with real-time obstacle re-planning.

**AI 2002 – Artificial Intelligence | Spring 2026 | Assignment 1 – Question 7**

---

## Preview

> GUI title: **GOOD PERFORMANCE TIME APP**

The visualizer animates the search frontier flooding across the grid in real-time, highlights explored nodes, and draws the final path from **S** (Start) to **T** (Target).

---

##  Algorithms Implemented

| # | Algorithm | Type |
|---|-----------|------|
| 1 | Breadth-First Search (BFS) | Queue-based |
| 2 | Depth-First Search (DFS) | Stack-based |
| 3 | Uniform-Cost Search (UCS) | Priority Queue |
| 4 | Depth-Limited Search (DLS) | DFS with depth cap |
| 5 | Iterative Deepening DFS (IDDFS) | Repeated DLS |
| 6 | Bidirectional Search | Dual BFS |

---

##  Movement Order

When expanding nodes, neighbors are added in the following **clockwise** order (all 8 directions including diagonals):

1. Up
2. Right
3. Down
4. Bottom-Right ↘
5. Left
6. Top-Left ↖
7. Top-Right ↗
8. Bottom-Left ↙

---

##  Dynamic Obstacles

- At each algorithm step, there is a small random **probability** that a new wall spawns at an empty cell.
- If a dynamic obstacle appears **on the planned path**, the agent **re-plans** immediately using the same active algorithm.
- If no path exists after re-planning, the GUI displays an appropriate message.

---

##  GUI Visualization

| Color | Meaning |
|-------|---------|
| 🟩 Green | Start node (S) |
| 🟥 Red | Target node (T) |
| ⬛ Black | Wall / Static obstacle |
| 🟧 Orange | Dynamic obstacle (spawned at runtime) |
| 🟦 Blue | Frontier (nodes in queue/stack) |
| 🟨 Yellow | Explored nodes |
| 🟪 Purple | Final path |

---

##  Getting Started

### Installation
```bash
git clone https://github.com/YOUR_USERNAME/AI-Pathfinder-Uninformed-Search.git
cd AI-Pathfinder-Uninformed-Search
pip install pygame
```

### Run
```bash
python main.py
```

---

##  Project Structure
```
AI-Pathfinder-Uninformed-Search/
├── main.py
├── grid.py
├── algorithms/
│   ├── bfs.py
│   ├── dfs.py
│   ├── ucs.py
│   ├── dls.py
│   ├── iddfs.py
│   └── bidirectional.py
├── visualizer.py
├── dynamic_obstacles.py
└── README.md
```

---

##  Algorithm Comparison

| Algorithm | Complete? | Optimal? | Time | Space |
|-----------|-----------|----------|------|-------|
| BFS | ✅ | ✅ | O(b^d) | O(b^d) |
| DFS | ✅ | ❌ | O(b^m) | O(bm) |
| UCS | ✅ | ✅ | O(b^(C*/ε)) | O(b^(C*/ε)) |
| DLS | ❌ | ❌ | O(b^l) | O(bl) |
| IDDFS | ✅ | ✅ | O(b^d) | O(bd) |
| Bidirectional | ✅ | ✅ | O(b^(d/2)) | O(b^(d/2)) |

---

## 👤 Author

**Student ID:** 24F-0506
**Course:** AI 2002 – Artificial Intelligence  
**Semester:** Spring 2026
