import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

AOC_SESSION = os.getenv("AOC_SESSION")

def fetch_input(year: int, day: int) -> str:
    """Fetch the input for the given Advent of Code year and day."""
    if not AOC_SESSION:
        raise ValueError("AOC_SESSION environment variable is not set!")

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, cookies={"session": AOC_SESSION})

    if response.status_code != 200:
        raise Exception(f"Failed to fetch input for {year} Day {day}. Status Code: {response.status_code} Is your Session cookie valid?")

    return response.text
