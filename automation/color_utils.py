import click

def red(s: str):
    return click.style(s, fg="red")

def green(s: str):
    return click.style(s, fg="green")

def yellow(s: str):
    return click.style(s, fg="yellow")
