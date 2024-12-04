from automation.run import Run
from automation.runner.python_runner import PythonRunner
from pathlib import Path


def run_puzzle_part(year: int, day: int, part: int) -> Run:
    runner = PythonRunner(Path(f"years/{year}/solutions/{day:02}/part_{part}.py"), "main")

    return runner.run()
