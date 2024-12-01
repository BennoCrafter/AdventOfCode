from typing import Any
from automation.get_input import get_input

input: str = get_input(2024, 1)

def main() -> Any:
    similarity_score = 0
    left_side: list[int] = []
    right_side: list[int] = []

    for line in input.split("\n"):
        w = line.split("   ")
        left_side.append(int(w[0]))
        right_side.append(int(w[1]))

    for item in left_side:
        similarity_score += item * right_side.count(item)

    return similarity_score
