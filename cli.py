import click
import requests
import subprocess
from pathlib import Path
from automation.date_utils import get_current_year, is_advent_time, get_current_day, days_until_december
from automation.color_utils import red, green, yellow

base_url = "https://adventofcode.com/%s/day/%s"

def open_puzzle(url: str):
    subprocess.run(["open", "-a", "Safari", url])

def create_puzzle_template(input_url: str):
    # check if year exists
    year_dir_path: Path = Path(f"years/{get_current_year()}")

    if not year_dir_path.exists():
        year_dir_path.mkdir(parents=True, exist_ok=True)

    puzzle_dir_path: Path = year_dir_path / f"{get_current_day():02}"

    if puzzle_dir_path.exists():
        click.echo(f"{yellow(f"The directory {puzzle_dir_path} already exists.")}")
        return

    puzzle_dir_path.mkdir(parents=True)

    # read input file
    resp = requests.get(input_url)
    if resp.status_code != 200:
        click.echo(f"{red("Oh no! Could'nt fetch input file.")} {resp.status_code}")
        return

    with open(puzzle_dir_path / "input.txt", "w") as file:
        file.write(resp.text)


@click.group()
def cli():
    pass

@cli.command()
def generate():
    """Generate latest code of event puzzle"""

    if  is_advent_time():
        click.echo(f"{red("It's not Advent time yet!")} There are {green(str(days_until_december()))} days left until December 1st.")
        return

    url = base_url % (get_current_year(), get_current_day())

    # open_puzzle(url)

    create_puzzle_template(f"{url}/input")


if __name__ == "__main__":
    cli()
