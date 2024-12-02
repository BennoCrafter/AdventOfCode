from typing import Any
from automation.get_input import get_input

input: str = get_input(2024, 2)

def is_save(nums: list[int], valid_differences: list[int]) -> bool:
    for i in range(len(nums)-1):
        if nums[i] - nums[i+1] not in valid_differences:
            return False

    return True

def main() -> Any:
    total_saves = 0
    for line in input.split("\n"):
        nums: list[int] = [int(i) for i in line.split(" ")]

        if is_save(nums, [-3, -2, -1]):
            total_saves += 1
            continue
        elif is_save(nums, [1, 2, 3]):
            total_saves += 1
            continue

    return total_saves
