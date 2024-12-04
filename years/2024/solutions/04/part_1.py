from typing import Any
from automation.get_input import get_input
import re

input: str = get_input(2024, 4)

def go_horizontal(grid: list[list[str]], word_to_search: str, pattern: str) -> int:
    c = 0
    for row in grid:
        r = re.findall(pattern, "".join(row))  # Search horizontally
        c += len(r)
    return c

def go_vertical(grid: list[list[str]], word_to_search: str, pattern: str) -> int:
    # Transpose the grid (swap rows and columns) to search vertically
    return go_horizontal(list(zip(*grid)), word_to_search, pattern)

def go_diagonal(grid: list[list[str]], word_to_search: str, pattern: str) -> int:
    c = 0
    diagonals_primary = []
    diagonals_secondary = []
    rows, cols = len(grid), len(grid[0])

    for d in range(-(rows - 1), cols):  # Range of diagonals
        diagonal = [grid[i][i - d] for i in range(max(0, d), min(rows, cols + d)) if 0 <= i - d < cols]
        if diagonal:
            diagonals_primary.append(diagonal)

    for d in range(0, rows + cols - 1):  # Range of diagonals
        diagonal = [grid[i][d - i] for i in range(max(0, d - cols + 1), min(rows, d + 1)) if 0 <= d - i < cols]
        if diagonal:
            diagonals_secondary.append(diagonal)

    for diagonal in diagonals_primary:
        r = re.findall(pattern, "".join(diagonal))  # Search diagonally
        c += len(r)
    for diagonal in diagonals_secondary:
        r = re.findall(pattern, "".join(diagonal))  # Search diagonally
        c += len(r)

    return c


def main() -> Any:
    word_to_search: str = "XMAS"
    pattern = r"(?=(%s|%s))" % (word_to_search, word_to_search[::-1])
    count = 0

    grid: list[list[str]] = [[char for char in line] for line in input.split("\n")]

    count += go_horizontal(grid, word_to_search, pattern)
    count += go_vertical(grid, word_to_search, pattern)
    count += go_diagonal(grid, word_to_search, pattern)

    return count
