import requests
from dotenv import load_dotenv
import os
import click
from automation.utils.write_to_env import write_to_env


# Load environment variables
load_dotenv()

AOC_SESSION = os.getenv("AOC_SESSION")

def fetch_input(year: int, day: int) -> str:
    global AOC_SESSION
    """Fetch the input for the given Advent of Code year and day."""
    if not AOC_SESSION:
        click.echo(click.style("AOC_SESSION environment variable is not set!", fg="yellow"), err=True)
        AOC_SESSION = click.prompt("Please enter your AOC_SESSION Token to fetch input file")
        write_to_env("AOC_SESSION", str(AOC_SESSION).strip())

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, cookies={"session": AOC_SESSION})

    if response.status_code != 200:
        raise Exception(f"Failed to fetch input for {year} Day {day}. Status Code: {response.status_code} Is your Session cookie valid?")

    return response.text
