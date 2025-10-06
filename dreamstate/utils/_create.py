import shutil
import sys
from pathlib import Path
from typing import NoReturn

import inquirer
import toml
from rich import print

from ._download import _download_template


def _raise_error() -> NoReturn:
    raise ValueError(
        message="The boilerplate argument must contain '<framework>@<version>' (example: 'flask@default').",
    )


def _create_project(
    boilerplate: str = "flask@default:latest",
    boilerplate_creator: str = "Robotz213",
) -> None:
    if "@" not in boilerplate:
        _raise_error()

    ask_list = [
        inquirer.Text(
            "project_name",
            message="Project name (default: my_project)",
            default="my_project",
            autocomplete="my_project",
        ),
    ]

    answers = inquirer.prompt(ask_list)
    project_name: str = (
        answers["project_name"]
        if answers and answers.get("project_name")
        else "my_project"
    )

    if " " in project_name:
        project_name = "_".join(project_name.split(" "))

    boiler_app, version = boilerplate.split("@")
    boilername = f"{boiler_app}_{version.split(':')[0]}"
    parent = Path(__file__).parent.resolve()
    path_template = parent.joinpath("templates", boilername)

    if not path_template.exists():
        _download_template(
            path_template=path_template,
            boilername=boilername,
            boilerplate_creator=boilerplate_creator,
            version="latest",
        )

    pyproject = None
    toml_pyproject = path_template.joinpath("pyproject.toml")

    if toml_pyproject.exists():
        with toml_pyproject.open("rb") as fp:
            pyproject = toml.load(fp)

        pyproject["project"]["name"] = project_name
        pyproject["project"]["requires-python"] = f">={sys.version}"

        with toml_pyproject.open("wb") as fp:
            toml.dump(pyproject, fp)

    for root, _, files in path_template.walk():
        relative_path = Path(root).relative_to(path_template)
        target_dir = Path.cwd().joinpath(project_name, relative_path)
        target_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            src_file = Path(root).joinpath(file)
            dest_file = target_dir.joinpath(file)
            shutil.copy2(src_file, dest_file)

    print(
        f"[bold green]Project '{project_name}' created successfully![/bold green]",
    )
