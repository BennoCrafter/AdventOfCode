from pathlib import Path

class Runner:
    def __init__(self, file_path: Path, function_name: str) -> None:
        self.file_path = file_path
        self.function_name = function_name

    def run(self):
        pass
