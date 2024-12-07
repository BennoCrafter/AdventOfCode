from typing import Any
from automation.get_input import get_input

input: str = get_input(2024, 6)

def get_position_of_guard(grid) -> tuple[int, int]:
    """Find the position of the guard (^) in the grid."""
    for i, row in enumerate(grid):
        if "^" in row:
            return (row.index("^"), i)
    raise ValueError("No guard found")

def main() -> Any:
    grid = [list(row) for row in input.split("\n")]
    width: int = len(grid[0])
    height: int = len(grid)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left
    found_loops = 0
    max_iterations = width * height

    guard_position = get_position_of_guard(grid)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            found_loop = False
            current_direction = 0
            position = guard_position
            visited = set()

            if (j, i) == guard_position or grid[i][j] == "#":
                continue

            new_grid = [row.copy() for row in grid]
            new_grid[i][j] = "#"

            iterations = 0
            while not found_loop:
                iterations += 1

                if iterations > max_iterations:
                    raise RuntimeError("Infinite loop detected")

                calculated_next_pos = (position[0] + directions[current_direction][0], position[1] + directions[current_direction][1])

                if calculated_next_pos[0] < 0 or calculated_next_pos[0] >= width or \
                   calculated_next_pos[1] < 0 or calculated_next_pos[1] >= height:
                    break

                item_at_new_pos = new_grid[calculated_next_pos[1]][calculated_next_pos[0]]
                if item_at_new_pos != "#":
                    position = calculated_next_pos
                    if (position,current_direction) not in visited:
                        visited.add((position, current_direction))
                        continue
                    else:
                        found_loop = True
                        break

                current_direction = (current_direction + 1) % len(directions)

            if found_loop:
                found_loops += 1

    return found_loops
