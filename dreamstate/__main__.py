"""DreamState CLI for package management."""

import sys

import typer

from dreamstate import cli

__all__ = ["cli"]


def main() -> None:
    cli.about()


if __name__ == "__main__":
    if len(sys.argv[1:]) == 0:
        typer.run(main)

cli.ds()
