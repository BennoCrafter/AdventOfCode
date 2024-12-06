from typing import Any
from automation.get_input import get_input

input: str = get_input(2024, 4)

def main() -> Any:
    rows = input.split('\n')
    m = len(rows)
    n = len(rows[0])

    def check(r, c):
        if rows[r][c] != 'A':
            return False
        ul = rows[r-1][c-1]
        ur = rows[r-1][c+1]
        dl = rows[r+1][c-1]
        dr = rows[r+1][c+1]
        return sorted([ul, ur, dl, dr]) == ['M', 'M', 'S', 'S'] and ul != dr

    return sum(check(r, c) for r in range(1, m-1) for c in range(1, n-1))
