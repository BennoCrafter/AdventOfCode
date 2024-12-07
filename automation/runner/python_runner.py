import click
from automation.utils.importer import import_from_path
from automation.runner.runner import Runner
from automation.run import Run
import time


class PythonRunner(Runner):
    def run(self) -> Run:
        module = import_from_path(self.file_path.name, self.file_path.absolute())

        if hasattr(module, 'main'):
            start_time = time.perf_counter_ns()
            result = module.main()
            end_time = time.perf_counter_ns()

            return Run(error=False, time=(end_time - start_time), result=result, file_path=self.file_path, function_name=self.function_name)

        click.echo(click.style(f"No 'main' function found in {module.__file__}", fg="red"), err=True)

        return Run(error=True, time=0.0, result="", file_path=self.file_path, function_name=self.function_name)
