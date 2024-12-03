from typing import Any
from automation.get_input import get_input
import re

input: str = get_input(2024, 3)

def main() -> Any:
    result = 0
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, input)
    for match in matches:
        result += int(match[0]) * int(match[1])
    return result
