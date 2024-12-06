from typing import Any
from automation.get_input import get_input

input: str = get_input(2024, 6)

def main() -> Any:
    grid = [list(row) for row in input.split("\n")]
    width: int = len(grid[0])
    height: int = len(grid)

    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    current_direction = 0
    position = (0, 0)
    visited = []
    found_exit = False

    for i, row in enumerate(grid):
        if "^" in row:
            position = (row.index("^"), i)
            break

    while not found_exit:
        calculated_next_pos = (position[0] + directions[current_direction][0], position[1] + directions[current_direction][1])
        if calculated_next_pos[0] < 0 or calculated_next_pos[0] >= width or \
            calculated_next_pos[1] < 0 or calculated_next_pos[1] >= height:
            print("Out of bounds")
            found_exit = True
            break

        item_at_new_pos = grid[calculated_next_pos[1]][calculated_next_pos[0]]
        if item_at_new_pos != "#":
            position = calculated_next_pos
            if position not in visited:
                visited.append(position)
            continue

        current_direction = (current_direction + 1) % len(directions)

    return len(visited)
