import re
import tempfile
import zipfile
from pathlib import Path
from typing import NoReturn

import requests


def _raise_error() -> NoReturn:
    raise RuntimeError(
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
    latest_url = f"https://github.com/{boilerplate_creator}/{boilername}/releases/{version}"

    # 1️⃣ Pega o HTML da página "latest"
    resp = requests.get(latest_url, timeout=120)
    resp.raise_for_status()
    html = resp.text

    # 2️⃣ Extrai a URL do .zip da última tag usando regex
    zip_url_match = re.search(
        rf'https://github\.com/Robotz213/{boilerplate_creator}/{boilername}/archive/refs/tags/[^"]+\.zip',
        html,
    )
    if not zip_url_match:
        _raise_error()

    zip_url = zip_url_match.group(0)

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
