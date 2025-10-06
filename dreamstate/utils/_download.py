import tempfile
import zipfile
from pathlib import Path
from typing import NoReturn

import requests


class URLNotFoundError(RuntimeError):
    def __init__(self, message: str, *args, **kwargs) -> None:
        """Exception raised when the URL for the .zip file is not found."""
        super().__init__(message, *args, **kwargs)


def _raise_error() -> NoReturn:
    """Raise a URLNotFoundError indicating the .zip file URL was not found.

    Raises:
        URLNotFoundError: If the .zip file URL for the latest release is not found.

    """
    raise URLNotFoundError(
        message="❌ Could not find the .zip file URL for the latest release.",
    )


def _download_template(
    path_template: Path,
    boilername: str = "flask_default",
    boilerplate_creator: str = "Robotz213",
    version: str = "latest",
) -> None:
    """Download the template from a GitHub release if it does not exist locally.

    Args:
        path_template (Path): The path where the template should be extracted.
        boilername (str): The name of the boilerplate repository.
        boilerplate_creator (str): The GitHub username or organization of the boilerplate creator.
        version (str): The release version to download (default is 'latest').

    """
    # URL of the latest release page
    if version == "latest":
        api_url = f"https://api.github.com/repos/{boilerplate_creator}/{boilername}/releases/latest"
    else:
        api_url = f"https://api.github.com/repos/{boilerplate_creator}/{boilername}/releases/tags/{version}"

    resp = requests.get(api_url, timeout=120)
    resp.raise_for_status()
    release_data = resp.json()

    zip_url = release_data.get("zipball_url")
    if not zip_url:
        _raise_error()

    # Download the .zip file
    zip_resp = requests.get(zip_url, stream=True, timeout=120)
    zip_resp.raise_for_status()

    # Save to disk

    temp_dir = Path(tempfile.mkdtemp()).joinpath("source.zip")

    with temp_dir.open("wb") as f:
        for chunk in zip_resp.iter_content(chunk_size=8192):
            f.write(chunk)

    # Extract the contents of the .zip file
    with zipfile.ZipFile(temp_dir, "r") as zip_ref:
        for member in zip_ref.namelist():
            parts = Path(member).parts
            # Ignore the top-level directory
            if len(parts) <= 1:
                continue  # skip files/directories at the top

            target_path = path_template.joinpath(*parts[1:])

            if member.endswith("/"):
                target_path.mkdir(parents=True, exist_ok=True)
                continue

            target_path.parent.mkdir(parents=True, exist_ok=True)
            with zip_ref.open(member) as source:
                Path(target_path).write_bytes(source.read())
