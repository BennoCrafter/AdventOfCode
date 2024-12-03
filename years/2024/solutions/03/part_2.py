from typing import Any
from automation.get_input import get_input
import re

input: str = get_input(2024, 3)

def main() -> Any:
    result = 0
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    is_active = True

    for m in re.split(r"(do\(\))|(don't\(\))", input):
        if m == None:
            continue

        is_active = True if m == "do()" else False if m == "don't()" else is_active

        if not is_active:
            continue

        for match in re.findall(pattern, m):
            result += int(match[0]) * int(match[1])

    return result
