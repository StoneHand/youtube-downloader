import json
import subprocess
import sys


def _get_installed_version():
    output = subprocess.check_output(
        [sys.executable, "-m", "pip", "show", "yt-dlp"],
        text=True,
        stderr=subprocess.DEVNULL,
    )
    for line in output.splitlines():
        if line.startswith("Version:"):
            return line.split(": ", 1)[1].strip()
    return None


def _install_or_upgrade_yt_dlp():
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp[default]"],
        stdout=subprocess.DEVNULL,
    )


def check_and_update_yt_dlp():
    """
    Instala yt-dlp si no está presente y lo actualiza cuando hay una versión nueva.
    """
    try:
        print("Buscando actualizaciones de componentes.")

        try:
            installed_version = _get_installed_version()
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("yt-dlp no está instalado. Instalando...")
            _install_or_upgrade_yt_dlp()
            print("Instalación completada.")
            return

        outdated_packages = subprocess.check_output(
            [sys.executable, "-m", "pip", "list", "--outdated", "--format", "json"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        outdated_packages = json.loads(outdated_packages)
        latest_version = next(
            (pkg["latest_version"] for pkg in outdated_packages if pkg["name"] == "yt-dlp"),
            None,
        )

        if latest_version and installed_version != latest_version:
            print(
                f"Actualizando yt-dlp de la versión {installed_version} a {latest_version}..."
            )
            _install_or_upgrade_yt_dlp()
            print("Actualización completada.")
        else:
            print("yt-dlp ya está actualizado.")
    except subprocess.CalledProcessError as error:
        print(f"Error al ejecutar un comando: {error}")
    except Exception as error:
        print(f"Error al verificar o actualizar yt-dlp: {error}")
