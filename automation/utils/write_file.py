from pathlib import Path
import click


def write_file(path, data):
    file_path = Path(path)

    try:
        with open(file_path, "w") as file:
            file.write(data)
        click.echo(click.style(f"Data written successfully to {file_path}", fg="green"))

    except Exception as e:
        click.echo(click.style(f"An error occurred while writing the file: {e}", fg="red"), err=True)
