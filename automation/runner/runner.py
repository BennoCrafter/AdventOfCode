from pathlib import Path
from abc import ABC
from automation.run import Run

# Base class for runners
class Runner(ABC):
    def __init__(self, file_path: Path, function_name: str) -> None:
        self.file_path = file_path
        self.function_name = function_name

    def run(self) -> Run:
        return Run(error=False, time=0.0, result="", file_path=self.file_path, function_name=self.function_name)
