from typing import Any
import time
import click

from automation.utils.importer import import_from_path


def get_result(year: int, day: int, part: int) -> tuple[Any, float]:
    name = f"part_{part}.py"
    module = import_from_path(f"{name}", f"years/{year}/solutions/{day:02}/{name}")

    if hasattr(module, 'main'):
        start_time = time.time()
        result = module.main()
        end_time = time.time()

        return result, (end_time - start_time)
    else:
        click.echo(click.style(f"No 'main' function found in {module.__file__}", fg="red"), err=True)

    return "", float("inf")
