from typing import Any, Optional
from automation.get_input import get_input

input: str = get_input(2024, 2)


def is_safe(nums: list[int], valid_differences: list[int]) -> tuple[bool, Optional[int]]:
    for i in range(len(nums) - 1):
        if nums[i] - nums[i + 1] not in valid_differences:
            return False, i
    return True, None


def is_safe_with_dampener(nums: list[int], valid_differences: list[int]) -> bool:
    # Check if already safe
    if is_safe(nums, valid_differences)[0]:
        return True

    # Check safety after removing one level
    for i in range(len(nums)):
        # Create a new list without the i-th element
        modified_nums = nums[:i] + nums[i + 1:]
        if is_safe(modified_nums, valid_differences)[0]:
            return True

    return False


def main() -> Any:
    total_saves = 0
    for line in input.strip().split("\n"):
        nums: list[int] = [int(i) for i in line.split()]

        # Check if safe using either original rules or with Problem Dampener
        if is_safe(nums, [-3, -2, -1])[0] or is_safe(nums, [1, 2, 3])[0]:
            total_saves += 1
        elif is_safe_with_dampener(nums, [-3, -2, -1]) or is_safe_with_dampener(nums, [1, 2, 3]):
            total_saves += 1

    return total_saves
