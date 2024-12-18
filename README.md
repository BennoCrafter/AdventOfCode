# AdventOfCode CLI

This repository provides a command-line interface (CLI) for interacting with Advent of Code challenges, including setting environment variables and fetching inputs directly.

## Features

- **Set environment variables**: Easily store and manage your `AOC_SESSION` in a `.env` file.
- **Fetch input for challenges**: Retrieve inputs for Advent of Code challenges with a simple command.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/BennoCrafter/AdventOfCode.git
   cd AdventOfCode
   ```

2. Use command line interface:

  - Build command line interface:
    ```bash
    pip3 install -e .
    ```

  - Run cli:
    ```bash
    aoc --help
    ```

  - Run cli without building:
    ```bash
    python3 cli.py --help
    ```
