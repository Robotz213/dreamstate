"""DreamState CLI module."""

from typer import Typer

from dreamstate._types import Boilerplate, CreatorBoiler
from dreamstate.utils import __display_info, _create_project

ds = Typer(
    name="DreamState Package Manager",
    help="DreamState Package Manager CLI.",
    rich_markup_mode="rich",
)


@ds.command()
def about() -> None:
    """Display information about the DreamState package manager."""
    __display_info()


@ds.command()
def version() -> None:
    """Display information about the DreamState package manager."""
    __display_info()


@ds.command(
    name="create-app",
    help="Start a project based on the provided boilerplate.",
)
def create_app(
    boilerplate: Boilerplate = "flask@default:latest",
    boilerplate_creator: CreatorBoiler = "Robotz213",
) -> None:
    """Create a new DreamState project based on the provided boilerplate."""
    _create_project(boilerplate, boilerplate_creator)
