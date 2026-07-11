import os
from pathlib import Path


def get_download_folder(subfolder=""):
    """
    Obtiene la carpeta de descargas del usuario y opcionalmente agrega un subdirectorio.
    Compatible con Windows, Linux y macOS.
    """
    downloads_path = _get_downloads_path()
    if subfolder:
        folder_path = downloads_path / subfolder
        folder_path.mkdir(parents=True, exist_ok=True)
        return str(folder_path)
    return str(downloads_path)


def _get_downloads_path():
    if os.name == "nt":
        base = Path(os.environ.get("USERPROFILE", Path.home()))
        return base / "Downloads"

    xdg_download = os.environ.get("XDG_DOWNLOAD_DIR")
    if xdg_download:
        return Path(xdg_download)

    return Path.home() / "Downloads"
