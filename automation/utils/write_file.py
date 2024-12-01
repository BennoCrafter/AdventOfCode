from pathlib import Path
import click


def write_file(inputs_dir_path, puzzle_name, input_data):
    inputs_dir_path = Path(inputs_dir_path)
    inputs_dir_path.mkdir(parents=True, exist_ok=True)

    file_path = inputs_dir_path / f"input_{puzzle_name}.txt"

    try:
        with open(file_path, "w") as file:
            file.write(input_data)
        click.echo(click.style(f"Data written successfully to {file_path}", fg="green"))

    except Exception as e:
        click.echo(click.style(f"An error occurred while writing the file: {e}", fg="red"), err=True)
