"""Utils module for DreamState package manager."""

from rich import print

from ._create import _create_project
from ._download import _download_template


def __display_info() -> None:
    print("[bold blue]DreamState Package Manager[/bold blue]")
    print("Version: [green]1.0.0[/green]")
    print("Author: [yellow]RobotzDev[/yellow]")
    print("License: [cyan]MIT[/cyan]")
    print(
        "[yellow]Project Repository: https://github.com/Robotz213/dreamstate [/yellow]",
    )


__all__ = ["_download_template", __display_info, "_create_project"]
