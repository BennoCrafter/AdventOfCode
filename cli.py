import click
import urllib.request
import os
import subprocess
from dotenv import load_dotenv
from automation.puzzle import create_puzzle_template, open_puzzle
from automation.utils.date_utils import get_current_year, get_current_day, is_advent_time, days_until_december
from automation.run_puzzle_part import run_puzzle_part
from automation.run import Run
from automation.utils.write_to_env import write_to_env
from pathlib import Path
import json
import atexit
import time

base_url = "https://adventofcode.com/%s/day/%s"
runs: list[Run] = []

# Load environment variables from .env file
load_dotenv()
AOC_SESSION = os.getenv("AOC_SESSION")

# Set up Click CLI
@click.group()
def cli():
    pass

# Command to generate puzzle template
@cli.command()
@click.option("--year", "-y", type=int, default=get_current_year(), help="Specify the year of the Advent puzzle. Defaults to the current year.")
@click.option("--day", "-d", type=int, default=get_current_day(), help="Specify the day of the Advent puzzle. Defaults to the current day.")
@click.option("--force", "-f", type=bool, default=False, is_flag=True, help="Specify if should force overwrite if needed.")
@click.option("--open", "-o", type=bool, default=False, is_flag=True, help="Whether to open the file in the browser.")
def puzzle(year, day, force, open):
    """Generate the Advent of Code puzzle template for a specific year and day."""
    if not is_advent_time():
        click.echo(f"{click.style('It\'s not Advent time yet!', fg='red')} There are {click.style(str(days_until_december()), fg='green')} days left until December 1st.")
        return

    if not (1 <= day <= 25):
        click.echo(click.style("Invalid day specified! Day must be between 1 and 25.", fg="red"))
        return

    url = base_url % (year, day)
    click.echo(click.style(f"== 🎄 Advent of Code {year} - Day {day} 🎁 == \n", fg="green", bold=True))

    create_puzzle_template(f"{url}/input", year, day, force)
    if open:
        open_puzzle(url)

# Command to execute the Advent puzzle
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

    run: Run = run_puzzle_part(year, day, part)
    runs.append(run)

    click.echo(click.style(f"Run time: {run.formatted_time()}", fg="green"))
    click.echo(click.style(run.display_result(), fg="blue"))

# Command to set environment variables
@cli.command()
@click.argument('key')
@click.argument('value')
@click.option("--file", "-f", type=str, default=".env", help="Specify the file to write the environment variable to. Defaults to .env")
def set(key: str, value: str, file: str):
    """Set an environment variable in the .{file} file."""
    write_to_env(key, value, Path(file))
    click.echo(f"Set {key}={value} in {file} file.")

# Command to commit puzzle solution to git
@cli.command()
@click.option("--year", "-y", type=int, default=get_current_year(), help="Specify the year of the Advent puzzle. Defaults to the current year.")
@click.option("--day", "-d", type=int, default=get_current_day(), help="Specify the day of the Advent puzzle. Defaults to the current day.")
def commit(year, day):
    """Commit a new puzzle"""
    p = Path(f"years/{year}/solutions/{day:02}")
    subprocess.run(["git", "add", p])
    subprocess.run(["git", "commit", "-m", f"Added solution for day {day} of year {year}"])
    subprocess.run(["git", "push"])

# Command to submit a puzzle solution
@cli.command()
@click.option("--year", "-y", type=int, default=get_current_year(), help="Specify the year of the Advent puzzle. Defaults to the current year.")
@click.option("--day", "-d", type=int, default=get_current_day(), help="Specify the day of the Advent puzzle. Defaults to the current day.")
@click.option("--part", "-p", type=int, default=1, help="Specify the part of the Advent puzzle. Defaults to 1")
def submit(year, day, part):
    """Submit a solution for the Advent puzzle."""
    run = run_puzzle_part(year, day, part)
    runs.append(run)

    if run.error:
        return

    headers = {"Cookie": f"session={AOC_SESSION}"}
    request = urllib.request.Request(
        f"https://adventofcode.com/{year}/day/{day}/answer",
        headers=headers,
        method="POST",
        data=f"level={part}&answer={run.result}".encode("ascii"),
    )
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")
    print(data)

# Command to display run history
@cli.command()
def history():
    """Show history of runs"""

    if not runs:
        click.echo("No runs recorded in this session.")
        return

    click.echo("\nRun History:")
    for i, run in enumerate(runs, 1):
        click.echo(f"\n{i}. {run.file_path} Function {run.function_name}")
        click.echo(f"   Result: {run.display_result()}")
        click.echo(f"   Time: {run.formatted_time()}")

# Function to save run history to a JSON file
history_file = Path(".aoc_history")

def save_run_history():
    """Save the current runs to history file"""
    if not runs:
        return

    history = []
    for run in runs:
        history.append(run.to_dict())

    # Keep only the last 30 runs
    history = history[-30:]

    with open(history_file, "w") as f:
        json.dump(history, f)

# Function to load run history from a JSON file
def load_run_history():
    """Load previous runs from history file"""
    if not history_file.exists():
        return

    with open(history_file, "r") as f:
        try:
            history = json.load(f)
            for run_data in history:
                run = Run.from_dict(run_data)
                runs.append(run)
        except json.JSONDecodeError:
            pass

load_run_history()

atexit.register(save_run_history)

if __name__ == "__main__":
    cli()
