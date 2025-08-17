# 🧩 Maze Solver (BFS / DFS)  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)  
![License](https://img.shields.io/badge/License-MIT-green.svg)  
![Status](https://img.shields.io/badge/Status-Active-success.svg)  
![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange.svg)

---

## 🚀 Overview
**Maze Solver** is a Python project that generates mazes and finds a path between a start and an exit point using **graph traversal algorithms**.  
It supports both **Breadth-First Search (BFS)** for finding the **shortest path** and **Depth-First Search (DFS)** for **backtracking exploration**.

You can run it in two modes:
- **Interactive mode** – the program asks for grid size, entry/exit, wall density, etc.  
- **Command-line mode** – provide arguments (`--rows`, `--cols`, etc.) for automation and testing.

This project is perfect for showcasing **DSA (Data Structures & Algorithms)** knowledge, particularly graphs, queues, recursion, and backtracking.

---

## ✨ Features
- Generate **random mazes** with configurable wall density.  
- Solve mazes using:
  - **BFS** – always finds the shortest path.  
  - **DFS** – explores deeply and backtracks.  
- Optionally **ensure solvable mazes** by regenerating until a valid path exists.  
- Support for **visited overlay** (`·`) and **path overlay** (`*`).  
- Export generated mazes to `.txt` files for reuse.  
- Run in **interactive mode** (prompts) or **CLI mode** (arguments).  

---

## 🔧 Installation
Clone the repository and make sure you have **Python 3.8+** installed.

```bash
git clone https://github.com/your-username/maze-solver.git
cd maze-solver
