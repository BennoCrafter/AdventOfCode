import click
import time
from automation.puzzle import create_puzzle_template, open_puzzle
from automation.utils.date_utils import get_current_year, get_current_day, is_advent_time, days_until_december
from automation.utils.importer import import_from_path
from automation.compare import get_comparison
from automation.utils.write_to_env import write_to_env

base_url = "https://adventofcode.com/%s/day/%s"

@click.group()
def cli():
    pass

@cli.command()
@click.option("--year", "-y", type=int, default=None, help="Specify the year of the Advent puzzle. Defaults to the current year.")
@click.option("--day", "-d", type=int, default=None, help="Specify the day of the Advent puzzle. Defaults to the current day.")
@click.option("--force", "-f", type=bool, default=False, is_flag=True, help="Specify if should force overwrite if needed.")
@click.option("--open", "-o", type=bool, default=False, is_flag=True, help="Whether to open the file in the browser.")
def puzzle(year, day, force, open):
    """Generate the Advent of Code puzzle template for a specific year and day."""
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
    if open:
        open_puzzle(url)

@cli.command()
@click.option("--year", type=int, default=None, help="Specify the year of the Advent puzzle. Defaults to the current year.")
@click.option("--day", type=int, default=None, help="Specify the day of the Advent puzzle. Defaults to the current day.")
@click.option("--part", type=int, default=1, help="Specify the part of which the Advent puzzle should get executed. Defaults to 1")
def execute(year, day, part):
    """Execute the specified part of the Advent puzzle."""
    year = year or get_current_year()
    day = day or get_current_day()

    if part not in [1, 2]:
        click.echo(click.style("Invalid part specified! Part must be 1 or 2.", fg="red"))
        return

    click.echo(f"Executing Part {part} of puzzle for {click.style(f'Day {day}, {year}', fg='blue')}...")

    name = f"part_{part}.py"
    module = import_from_path(f"{name}", f"years/{year}/solutions/{day:02}/{name}")

    if hasattr(module, 'main'):
        start_time = time.time()
        result = module.main()
        end_time = time.time()

        click.echo(click.style(f"Execution time: {(end_time - start_time):.5f} seconds. Equivalent to {get_comparison(end_time - start_time)[1]}", fg="green"))
        click.echo(click.style(f"Result: {result}", fg="blue"))
    else:
        print(f"No 'main' function found in {module.__file__}")

@cli.command()
@click.argument('key')
@click.argument('value')
def set(key: str, value: str):
    """Set an environment variable in the .env file."""
    write_to_env(key, value)
    click.echo(f"Set {key}={value} in .env file.")


if __name__ == "__main__":
    cli()
