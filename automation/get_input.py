import click
from pathlib import Path
from automation.utils.read_file import read_file
from automation.fetch_input import fetch_input
from automation.utils.write_file import write_file


def get_input(year: int, day: int) -> str:
    puzzle_name = f"{day:02}"
    inputs_dir_path = Path(f"years/{year}/inputs/")

    p = inputs_dir_path / f"input_{puzzle_name}.txt"

    if not p.exists():
        click.echo(click.style(f"Input file for Day {day}, {year} does not exist! Generating it..", fg="yellow"))
        write_file(p, fetch_input(year, day))

    return read_file(p).strip()
