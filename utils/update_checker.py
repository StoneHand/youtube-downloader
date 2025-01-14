import subprocess
import sys
import json

def check_and_update_yt_dlp():
    """
    Verifica si hay una nueva versión de `yt-dlp` y la actualiza si es necesario.
    """
    try:
        print("Buscando actualizaciones de componentes.")

        # Verificar la versión instalada
        installed_version = subprocess.check_output(
            [sys.executable, "-m", "pip", "show", "yt-dlp"],
            text=True
        )
        installed_version = next(
            (line.split(": ")[1] for line in installed_version.splitlines() if "Version" in line), None
        )

        # Obtener la última versión de PyPI usando pip list --outdated
        outdated_packages = subprocess.check_output(
            [sys.executable, "-m", "pip", "list", "--outdated", "--format", "json"],
            text=True
        )
        outdated_packages = json.loads(outdated_packages)
        latest_version = next(
            (pkg["latest_version"] for pkg in outdated_packages if pkg["name"] == "yt-dlp"),
            None
        )

        # Comparar las versiones e intentar actualizar si es necesario
        if installed_version and latest_version and installed_version != latest_version:
            print(f"Actualizando yt-dlp de la versión {installed_version} a {latest_version}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
            print("Actualización completada.")
        else:
            print("yt-dlp ya está actualizado.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar un comando: {e}")
    except Exception as e:
        print(f"Error al verificar o actualizar yt-dlp: {e}")
