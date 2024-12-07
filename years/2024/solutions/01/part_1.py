from typing import Any
from automation.get_input import get_input

input: str = get_input(2024, 1)

def main() -> Any:
    left_side: list[int] = []
    right_side: list[int] = []
    total_distance = 0

    for line in input.split("\n"):
        w = line.split("   ")
        left_side.append(int(w[0]))
        right_side.append(int(w[1]))

    left_side.sort()
    right_side.sort()

    for index, (left, right) in enumerate((left_side, right_side)):
        total_distance += abs(left - right)

    return total_distance
