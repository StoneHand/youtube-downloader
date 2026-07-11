import os
import shutil

from downloader.common import get_base_ydl_opts


def check_environment():
    """
    Verifica que el entorno tenga las dependencias necesarias para descargar de YouTube.
    Devuelve (errores, advertencias).
    """
    errors = []
    warnings = []

    if not shutil.which("ffmpeg"):
        errors.append(
            "FFmpeg no está instalado o no está en el PATH. "
            "Descárgalo en https://ffmpeg.org/download.html"
        )

    if not shutil.which("deno") and not shutil.which("node"):
        warnings.append(
            "No se encontró Deno ni Node.js. YouTube requiere un runtime JavaScript "
            "(recomendado: Deno). Instálalo desde https://docs.deno.com/runtime/"
        )

    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        errors.append(
            "yt-dlp no está instalado. Ejecuta: pip install -r requirements.txt"
        )

    cookies_browser = os.environ.get("YTDLP_COOKIES_BROWSER")
    cookies_file = os.environ.get("YTDLP_COOKIES_FILE")
    if not cookies_browser and not cookies_file:
        warnings.append(
            "Si YouTube pide verificación, configura cookies con la variable "
            "YTDLP_COOKIES_BROWSER (ej: chrome, firefox, edge) o YTDLP_COOKIES_FILE "
            "con la ruta a un archivo de cookies exportado."
        )

    return errors, warnings


def print_environment_status():
    errors, warnings = check_environment()
    for warning in warnings:
        print(f"Advertencia: {warning}")
    for error in errors:
        print(f"Error: {error}")
    return len(errors) == 0
