"""Console script for pyutils."""

import typer
from rich.console import Console


app = typer.Typer()
console = Console()


@app.command()
def main() -> None:
    """Console script for pyutils."""
    console.print("Replace this message by putting your code into pyutils.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")


if __name__ == "__main__":
    app()
