import re
import tempfile
import zipfile
from pathlib import Path
from typing import NoReturn

import requests
from rich import print


class URLNotFoundError(RuntimeError):
    def __init__(self, message: str, *args, **kwargs) -> None:
        super().__init__(message, *args, **kwargs)


def _raise_error() -> NoReturn:
    raise URLNotFoundError(
        message="❌ Não foi possível encontrar a URL do arquivo .zip da última release.",
    )


def _download_template(
    path_template: Path,
    boilername: str = "flask_default",
    boilerplate_creator: str = "Robotz213",
    version: str = "latest",
) -> None:
    """Download the template if it does not exist locally."""
    # URL da página da última release
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

    # 3️⃣ Faz o download do .zip
    zip_resp = requests.get(zip_url, stream=True, timeout=120)
    zip_resp.raise_for_status()

    # 4️⃣ Salva no disco

    temp_dir = Path(tempfile.mkdtemp()).joinpath("source.zip")

    with temp_dir.open("wb") as f:
        for chunk in zip_resp.iter_content(chunk_size=8192):
            f.write(chunk)

    # 5️⃣ Extrai o conteúdo do .zip
    with zipfile.ZipFile(temp_dir, "r") as zip_ref:
        for member in zip_ref.namelist():
            # Remove the top-level directory from the path
            parts = Path(member).parts
            if len(parts) > 1:
                target_path = path_template.joinpath(*parts[1:])
            else:
                target_path = path_template.joinpath(*parts)
            if member.endswith("/"):
                target_path.mkdir(parents=True, exist_ok=True)
            else:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                with zip_ref.open(member) as source:
                    Path(target_path).write_bytes(source.read())
