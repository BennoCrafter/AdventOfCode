from pathlib import Path
import datetime


class Run:
    def __init__(self, result: str, error: bool, time: float, file_path: Path, function_name: str = "", timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        self.result = result
        self.time = time
        self.error = error
        self.file_path = file_path
        self.function_name = function_name
        self.timestamp = timestamp

    def time_in_ms(self) -> float:
        return self.time / 1_000_000

    def time_in_s(self) -> float:
        return self.time_in_ms() / 1000

    def formatted_time(self) -> str:
        if self.time_in_s() < 1:
            return f"{self.time_in_ms():.2f} ms"
        elif self.time_in_s() < 60:
            return f"{self.time_in_s():.2f} s"
        else:
            return f"{self.time_in_s():.2f} min"

    def display(self) -> str:
        if self.error:
            return "Error!"

        return f"Result: {self.result}\nTime: {self.time_in_ms()} ms\n"

    def display_result(self) -> str:
        return f"Result: {self.result}"

    @staticmethod
    def from_dict(d: dict) -> "Run":
        return Run(
            d["result"],
            d["error"],
            d["time"],
            Path(d["file_path"]),
            d["function_name"],
            d["timestamp"]
        )

    def to_dict(self) -> dict:
        return {
            "result": self.result,
            "error": self.error,
            "time": self.time,
            "file_path": self.file_path.as_posix(),
            "function_name": self.function_name,
            "timestamp": self.timestamp
        }
