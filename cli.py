import click
import requests
import subprocess
import importlib
import importlib.util
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import shutil
from types import ModuleType
from automation.date_utils import get_current_year, is_advent_time, get_current_day, days_until_december


load_dotenv()
base_url = "https://adventofcode.com/%s/day/%s"
AOC_SESSION = os.getenv("AOC_SESSION")

def open_puzzle(url: str):
    subprocess.run(["open", "-a", "Safari", url])

def create_puzzle_template(input_url: str, year: int, day: int, is_forced: bool):
    # Check if year exists
    puzzle_name = f"{day:02}"

    year_dir_path = Path(f"years/{year}")
    year_dir_path.mkdir(parents=True, exist_ok=True)

    solutions_dir_path = year_dir_path / "solutions"
    solutions_dir_path.mkdir(parents=True, exist_ok=True)

    inputs_dir_path = year_dir_path / "inputs"
    inputs_dir_path.mkdir(parents=True, exist_ok=True)

    puzzle_dir_path = solutions_dir_path / puzzle_name

    # Handle forced overwriting
    if puzzle_dir_path.exists():
        if is_forced:
            click.echo(click.style(f"Directory {puzzle_dir_path} already exists. Overwriting...", fg="yellow"))
            # Remove the existing directory and all its contents
            shutil.rmtree(puzzle_dir_path)
        else:
            click.echo(click.style(f"The directory {puzzle_dir_path} already exists. Use '--force' to overwrite.", fg="yellow"))
            return

    # Create a new puzzle directory
    puzzle_dir_path.mkdir(parents=True)

    # Fetch input file from the provided URL
    if not input_url:
        click.echo(click.style("No input URL provided.", fg="red"))
        return

    resp = requests.get(input_url, cookies={"session": AOC_SESSION if AOC_SESSION else ""})
    if resp.status_code != 200:
        click.echo(click.style(f"Oh no! Couldn't fetch input file. Status code: {resp.status_code}", fg="red"))
        return

    # Save the input to the puzzle directory
    with open(inputs_dir_path / f"input_{puzzle_name}.txt", "w") as file:
        file.write(resp.text)

    # Create part_1.py and part_2.py files
    for part in range(1, 3):
        part_file = puzzle_dir_path / f"part_{part}.py"
        part_file.write_text(f"from automation.fetcher.get_input import get_input\n\ninput = get_input({year}, {day})\n\ndef main():\n\tpass\n")

    click.echo(click.style(f"Puzzle template created for Year {year}, Day {day}!", fg="green"))


@click.group()
def cli():
    pass

@cli.command()
@click.option("--year", type=int, default=None, help="Specify the year of the Advent puzzle. Defaults to the current year.")
@click.option("--day", type=int, default=None, help="Specify the day of the Advent puzzle. Defaults to the current day.")
@click.option("--force", type=bool, default=False, is_flag=True, help="Specify if should force overwrite if needed.")
def puzzle(year, day, force):
    """Generate the Advent of Code puzzle template for a specific year and day."""

    # Check if it's Advent time
    if not is_advent_time():
        click.echo(
            f"{click.style('It\'s not Advent time yet!', fg='red')} "
            f"There are {click.style(str(days_until_december()), fg='green')} days left until December 1st."
        )
        return

    year = year or get_current_year()
    day = day or get_current_day()

    if not (1 <= day <= 25):
        click.echo(click.style("Invalid day specified! Day must be between 1 and 25.", fg="red"))
        return

    url = base_url % (year, day)

    click.echo(f"Generating puzzle for {click.style(f'Day {day}, {year}', fg='blue')}...")

    create_puzzle_template(f"{url}/input", year, day, force)

    open_puzzle(url)

@cli.command()
@click.option("--year", type=int, default=None, help="Specify the year of the Advent puzzle. Defaults to the current year.")
@click.option("--day", type=int, default=None, help="Specify the day of the Advent puzzle. Defaults to the current day.")
@click.option("--part", type=int, default=1, help="Specify the part of which the Advent puzzle shoud get executed. Defaults to 1")
def execute(year, day, part):
    year = year or get_current_year()
    day = day or get_current_day()

    if not part in range(1, 2 + 1):
        click.echo(click.style("Invalid part specified! Part must be between 1 and 2.", fg="red"))
        return

    click.echo(f"Executing Part {part} of puzzle for {click.style(f'Day {day}, {year}', fg='blue')}...")

    name = f"part_{part}.py"

    module = import_from_path(f"{name}", f"years/{year}/solutions/{day:02}/{name}")

    if hasattr(module, 'main'):
        print(module.main())
    else:
        print(f"No 'main' function found in {module.__file__}")


def import_from_path(module_name, file_path) -> ModuleType:
    """Import a module given its name and file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)

    if spec is None:
        raise ValueError(f"Could not create module spec for {file_path}")

    if spec.loader is None:
        raise ValueError(f"Loader is None for module spec of {module_name}")

    module = importlib.util.module_from_spec(spec)

    sys.modules[module_name] = module

    spec.loader.exec_module(module)

    return module

if __name__ == "__main__":
    cli()
