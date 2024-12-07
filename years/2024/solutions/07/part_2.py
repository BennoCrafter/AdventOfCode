from typing import Any
from automation.get_input import get_input

input: str = get_input(2024, 7)
elements: list[str] = ["*", "+", "||"]

def get_combinations(nums: list[int], length: int) -> list[list[str]]:
    combinations = [[]]
    for i in range(length):
        new_combinations = []

        for combo in combinations:
            for element in elements:
                new_combinations.append(combo + [element])

        combinations = new_combinations
    return combinations

def try_equation(target: int, nums: list[int], combinations: list[list[str]]) -> bool:
    for combo in combinations:
        res = nums[0]
        for i in range(1, len(nums)):
            if combo[i-1] == "+":
                res += nums[i]
            elif combo[i-1] == "*":
                res *= nums[i]
            elif combo[i-1] == "||":
                res = int(str(res) + str(nums[i]))
        if res == target:
            return True
    return False

def main() -> Any:
    test_equations = []
    result = 0
    for line in input.split("\n"):
        tn, nums = line.split(": ")
        nums = [int(n) for n in nums.split(" ")]
        test_equations.append((int(tn), nums))

    for test_equation in test_equations:
        combinations = get_combinations(test_equation[1], len(test_equation[1])-1)
        if try_equation(test_equation[0], test_equation[1], combinations):
            result += test_equation[0]
    return result
