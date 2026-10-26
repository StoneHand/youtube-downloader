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

    xdg_download = os.environ.get("XDG_DOWNLOAD_DIR") or _read_user_dirs_download()
    if xdg_download:
        return Path(xdg_download)

    return Path.home() / "Downloads"


def _read_user_dirs_download():
    """Lee la carpeta de descargas de ~/.config/user-dirs.dirs (ej: ~/Descargas en Ubuntu en español)."""
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    try:
        lines = (config_home / "user-dirs.dirs").read_text(encoding="utf-8").splitlines()
    except OSError:
        return None

    for line in lines:
        if line.startswith("XDG_DOWNLOAD_DIR="):
            value = line.split("=", 1)[1].strip().strip('"')
            return value.replace("$HOME", str(Path.home())) or None
    return None
