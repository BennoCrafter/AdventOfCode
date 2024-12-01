import click
import urllib.request
import os
from dotenv import load_dotenv
from automation.puzzle import create_puzzle_template, open_puzzle
from automation.utils.date_utils import get_current_year, get_current_day, is_advent_time, days_until_december
from automation.compare import get_comparison
from automation.get_result import get_result
from automation.utils.write_to_env import write_to_env

base_url = "https://adventofcode.com/%s/day/%s"
load_dotenv()

AOC_SESSION = os.getenv("AOC_SESSION")

@click.group()
def cli():
    pass

@cli.command()
@click.option("--year", "-y", type=int, default=get_current_year(), help="Specify the year of the Advent puzzle. Defaults to the current year.")
@click.option("--day", "-d", type=int, default=get_current_day(), help="Specify the day of the Advent puzzle. Defaults to the current day.")
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

    if not (1 <= day <= 25):
        click.echo(click.style("Invalid day specified! Day must be between 1 and 25.", fg="red"))
        return

    url = base_url % (year, day)
    click.echo(click.style(f"== 🎄 Advent of Code {year} - Day {day} 🎁 == \n", fg="green", bold=True))

    create_puzzle_template(f"{url}/input", year, day, force)
    if open:
        open_puzzle(url)

@cli.command()
@click.option("--year", "-y", type=int, default=get_current_year(), help="Specify the year of the Advent puzzle. Defaults to the current year.")
@click.option("--day", "-d", type=int, default=get_current_day(), help="Specify the day of the Advent puzzle. Defaults to the current day.")
@click.option("--part", "-p", type=int, default=1, help="Specify the part of which the Advent puzzle should get executed. Defaults to 1")
def run(year, day, part):
    """Execute an Advent puzzle."""

    if part not in [1, 2]:
        click.echo(click.style("Invalid part specified! Part must be 1 or 2.", fg="red"))
        return

    click.echo(f"Running Part {part} of puzzle for {click.style(f'Day {day}, {year}', fg='blue')}...")

    result, elapsed_time = get_result(year, day, part)

    click.echo(click.style(f"Execution time: {(elapsed_time * 1000):.2f} ms. Equivalent to {get_comparison(elapsed_time)[1]}", fg="green"))
    click.echo(click.style(f"Result: {result}", fg="blue"))

@cli.command()
@click.argument('key')
@click.argument('value')
def set(key: str, value: str):
    """Set an environment variable in the .env file."""
    write_to_env(key, value)
    click.echo(f"Set {key}={value} in .env file.")

@cli.command()
@click.option("--year", "-y", type=int, default=get_current_year(), help="Specify the year of the Advent puzzle. Defaults to the current year.")
@click.option("--day", "-d", type=int, default=get_current_day(), help="Specify the day of the Advent puzzle. Defaults to the current day.")
@click.option("--part", "-p", type=int, default=1, help="Specify the part of the Advent puzzle. Defaults to 1")
def submit(year, day, part):
    result, elapsed_time = get_result(year, day, part)

    if elapsed_time == float("inf"):
        return

    headers = {"Cookie": f"session={AOC_SESSION}"}
    request = urllib.request.Request(
        f"https://adventofcode.com/{year}/day/{day}/answer",
        headers=headers,
        method="POST",
        data=f"level={part}&answer={result}".encode("ascii"),
    )
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")
    print(data)


if __name__ == "__main__":
    cli()
