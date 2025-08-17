#!/usr/bin/env python3
"""
Interactive Maze Solver (BFS/DFS)
---------------------------------
Prompts the user for:
- Grid size (rows, cols)
- Start and end coordinates (0-indexed)
- Wall density (for random walls)
- Algorithm (bfs/dfs)
- Ensure solvable? (y/n)
- Seed (optional) for reproducibility
- Show visited overlay? (y/n)
- Export generated maze to .txt? (optional path)

Run:
  python maze_solver_interactive.py
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import List, Tuple, Optional, Iterable, Dict, Set
import random
import time
import sys

Coord = Tuple[int, int]

@dataclass
class Maze:
    grid: List[List[str]]
    start: Coord
    end: Coord

    @staticmethod
    def random(rows: int, cols: int, start: Coord, end: Coord, density: float, rng: random.Random) -> "Maze":
        if rows <= 1 or cols <= 1:
            raise ValueError("rows and cols must be >= 2")
        if not (0 <= start[0] < rows and 0 <= start[1] < cols):
            raise ValueError("start out of bounds")
        if not (0 <= end[0] < rows and 0 <= end[1] < cols):
            raise ValueError("end out of bounds")
        if start == end:
            raise ValueError("start and end cannot be the same cell")
        if not (0.0 <= density < 1.0):
            raise ValueError("density must be in [0.0, 1.0)")

        grid = [['#' if rng.random() < density else '.' for _ in range(cols)] for _ in range(rows)]
        sr, sc = start
        er, ec = end
        grid[sr][sc] = '.'
        grid[er][ec] = '.'
        return Maze(grid, start, end)

    def neighbors(self, rc: Coord) -> Iterable[Coord]:
        r, c = rc
        for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
            nr, nc = r+dr, c+dc
            if 0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0]):
                if self.grid[nr][nc] != '#':
                    yield (nr, nc)

    def draw_with_path(self, path: Optional[List[Coord]], visited: Optional[Set[Coord]] = None) -> str:
        g = [row[:] for row in self.grid]
        if visited:
            for (r, c) in visited:
                if g[r][c] == '.':
                    g[r][c] = '·'
        if path:
            for (r, c) in path:
                if g[r][c] not in ('S','E'):
                    g[r][c] = '*'
        sr, sc = self.start
        er, ec = self.end
        if g[sr][sc] != '*': g[sr][sc] = 'S'
        if g[er][ec] != '*': g[er][ec] = 'E'
        return "\n".join("".join(row) for row in g)

def reconstruct_path(parents: Dict[Coord, Coord], end: Coord, start: Coord) -> List[Coord]:
    path = [end]
    cur = end
    while cur != start:
        cur = parents[cur]
        path.append(cur)
    path.reverse()
    return path

def bfs(maze: Maze):
    from collections import deque
    q = deque([maze.start])
    parents: Dict[Coord, Coord] = {}
    visited: Set[Coord] = {maze.start}
    while q:
        cur = q.popleft()
        if cur == maze.end:
            return reconstruct_path(parents, maze.end, maze.start), visited
        for nb in maze.neighbors(cur):
            if nb not in visited:
                visited.add(nb)
                parents[nb] = cur
                q.append(nb)
    return None, visited

def dfs_backtracking(maze: Maze):
    visited: Set[Coord] = set()
    parents: Dict[Coord, Coord] = {}
    found = False
    def dfs(u: Coord):
        nonlocal found
        if found:
            return
        visited.add(u)
        if u == maze.end:
            found = True
            return
        for v in maze.neighbors(u):
            if v not in visited:
                parents[v] = u
                dfs(v)
    dfs(maze.start)
    if found:
        return reconstruct_path(parents, maze.end, maze.start), visited
    return None, visited

def ask_int(prompt: str, min_val: Optional[int]=None, max_val: Optional[int]=None) -> int:
    while True:
        s = input(prompt).strip()
        try:
            v = int(s)
            if min_val is not None and v < min_val:
                print(f"  -> must be >= {min_val}")
                continue
            if max_val is not None and v > max_val:
                print(f"  -> must be <= {max_val}")
                continue
            return v
        except ValueError:
            print("  -> please enter an integer")

def ask_coord(prompt: str) -> Coord:
    while True:
        s = input(prompt).strip()
        try:
            r_str, c_str = s.split(",")
            r, c = int(r_str), int(c_str)
            return r, c
        except Exception:
            print("  -> format must be row,col (e.g., 1,2)")

def ask_float(prompt: str, min_val: float, max_val: float) -> float:
    while True:
        s = input(prompt).strip()
        try:
            v = float(s)
            if not (min_val <= v <= max_val):
                print(f"  -> must be between {min_val} and {max_val}")
                continue
            return v
        except ValueError:
            print("  -> please enter a number")

def ask_choice(prompt: str, choices: List[str]) -> str:
    choices_lower = [c.lower() for c in choices]
    while True:
        s = input(prompt).strip().lower()
        if s in choices_lower:
            return s
        print(f"  -> choose one of: {', '.join(choices)}")

def main():
    print("=== Interactive Maze Solver ===")
    rows = ask_int("Enter number of rows (>=2): ", min_val=2)
    cols = ask_int("Enter number of cols (>=2): ", min_val=2)

    print("\nCoordinates are 0-indexed (top-left is 0,0)")
    start = ask_coord("Enter start (row,col): ")
    end = ask_coord("Enter exit  (row,col): ")

    density = ask_float("Enter wall density (0.0 - 0.9 recommended): ", 0.0, 0.99)
    algo = ask_choice("Choose algorithm (bfs/dfs): ", ["bfs", "dfs"])
    ensure = ask_choice("Ensure solvable? (y/n): ", ["y", "n"]) == "y"
    show_visited = ask_choice("Show visited overlay? (y/n): ", ["y", "n"]) == "y"

    seed_in = input("Enter RNG seed (optional, press Enter to skip): ").strip()
    seed = int(seed_in) if seed_in else None
    rng = random.Random(seed)

    max_tries = 200
    attempt = 0
    while True:
        attempt += 1
        try:
            maze = Maze.random(rows, cols, start, end, density, rng)
        except Exception as e:
            print(f"Input error: {e}")
            return

        t0 = time.perf_counter()
        if algo == "bfs":
            path, visited = bfs(maze)
        else:
            path, visited = dfs_backtracking(maze)
        ms = (time.perf_counter() - t0) * 1000.0

        if path is not None or not ensure or attempt >= max_tries:
            break

    print(f"\nGenerated Maze ({rows}x{cols})  density={density:.2f}  seed={seed}")
    print(f"Start={start}  End={end}  Algo={algo.upper()}  Attempt={attempt}")
    print(f"Visited: {len(visited)} nodes")
    if path:
        print(f"Path len: {len(path)-1} steps")
    else:
        print("Path: — (no path found)")

    overlay = visited if show_visited else None
    print("\n" + maze.draw_with_path(path, overlay))
    print(f"\nTime: {ms:.2f} ms")

    exp = input("\nExport this maze layout to a file? Enter path or press Enter to skip: ").strip()
    if exp:
        # Save walls + S/E, not path/visited overlay
        g = [row[:] for row in maze.grid]
        sr, sc = maze.start
        er, ec = maze.end
        g[sr][sc] = 'S'
        g[er][ec] = 'E'
        with open(exp, "w", encoding="utf-8") as f:
            f.write("\n".join("".join(row) for row in g))
        print(f"Saved maze to: {exp}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
