from pathlib import Path


def read_file(filepath: Path) -> str:
    with open(filepath, "r") as f:
        return f.read()

def get_input(year: int, day: int) -> str:
    p = Path(f"years/{year}/inputs/input_{day:02}.txt")
    return read_file(p)
