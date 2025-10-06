"""DreamState CLI module."""

import shutil
from pathlib import Path
from typing import NoReturn

from rich import print
from typer import Typer

ds = Typer(
    name="DreamState Package Manager",
    help="DreamState Package Manager CLI.",
)


def _raise_error() -> NoReturn:
    raise ValueError(
        message="Argumento boilerplate precisa conter '<framework>@'<version>' (exemplo: 'flask@default')",
    )


@ds.command(
    name="create-app",
    help="Start a project based on the provided boilerplate.",
)
def create_app(
    boilerplate: str = "flask@default",
    project_name: str = "my_project",
) -> None:
    """Create a new DreamState project based on the provided boilerplate."""
    if "@" not in boilerplate:
        _raise_error()

    boiler_app, version = boilerplate.split("@")
    boilername = f"{boiler_app}_{version}"
    parent = Path(__file__).parent.resolve()
    path_template = parent.joinpath("templates", boilername)

    for root, _, files in shutil.walk(path_template):
        relative_path = Path(root).relative_to(path_template)
        target_dir = Path.cwd().joinpath(project_name, relative_path)
        target_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            src_file = Path(root).joinpath(file)
            dest_file = target_dir.joinpath(file)
            shutil.copy2(src_file, dest_file)

    print(
        f"[bold green]Projeto '{project_name}' criado com sucesso![/bold green]",
    )
