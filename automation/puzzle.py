import subprocess
import shutil
import click
from pathlib import Path
from automation.fetch_input import fetch_input
from automation.utils.read_file import read_file
from automation.utils.write_file import write_file

def create_input_file(year: int, day: int, inputs_dir_path: Path, puzzle_name: str) -> bool:
    try:
        input_data = fetch_input(year, day)
    except Exception as e:
        click.echo(click.style(f"Error fetching input: {str(e)}", fg="red"))
        return False

    # Create input.txt file
    write_file(inputs_dir_path / f"input_{puzzle_name}.txt", input_data)
    return True

def open_puzzle(url: str):
    """Open the Advent of Code puzzle in Safari."""
    subprocess.run(["open", "-a", "Safari", url])

def create_puzzle_template(input_url: str, year: int, day: int, is_forced: bool):
    """Create the puzzle template (folders and files) for a given year and day."""
    puzzle_name = f"{day:02}"
    puzzle_template_path = Path("assets/puzzle_template.txt")

    year_dir_path = Path(f"years/{year}")
    year_dir_path.mkdir(parents=True, exist_ok=True)

    solutions_dir_path = year_dir_path / "solutions"
    solutions_dir_path.mkdir(parents=True, exist_ok=True)

    inputs_dir_path = year_dir_path / "inputs"
    inputs_dir_path.mkdir(parents=True, exist_ok=True)

    puzzle_dir_path = solutions_dir_path / puzzle_name

    if not create_input_file(year, day, inputs_dir_path, puzzle_name):
        return

    # Handle forced overwriting
    if puzzle_dir_path.exists():
        if is_forced:
            click.echo(click.style(f"Directory {puzzle_dir_path} already exists. Overwriting...", fg="yellow"))
            shutil.rmtree(puzzle_dir_path)
        else:
            click.echo(click.style(f"The directory {puzzle_dir_path} already exists. Use '--force' to overwrite.", fg="yellow"))
            return

    puzzle_dir_path.mkdir(parents=True)

    # Create part_1.py and part_2.py files
    for part in range(1, 3):
        part_file_path = puzzle_dir_path / f"part_{part}.py"
        write_file(part_file_path, read_file(puzzle_template_path) % (year, day))

    click.echo(click.style(f"Puzzle template created for Year {year}, Day {day}!", fg="green"))
