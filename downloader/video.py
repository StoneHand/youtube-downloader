import os
import shutil
import subprocess

from yt_dlp import YoutubeDL

from downloader.common import get_base_ydl_opts, run_with_cookie_fallback
from utils.file_utils import get_download_folder


def _mp4_format(height):
    """
    Prefiere H.264 + AAC, que Windows reproduce sin códecs extra. El mejor video/audio
    por defecto de YouTube suele ser AV1/VP9 + Opus, que muchos reproductores no abren en MP4.
    """
    return (
        f"bv*[vcodec^=avc1][height<={height}]+ba[acodec^=mp4a]"
        f"/bv*[height<={height}]+ba/b[height<={height}]"
    )


QUALITY_MAP = {
    "baja": _mp4_format(360),
    "media": _mp4_format(720),
    "alta": _mp4_format(1080),
    "360p": _mp4_format(360),
    "720p": _mp4_format(720),
    "1080p": _mp4_format(1080),
}


def _audio_codec(info):
    """Códec de audio del archivo descargado (ej: 'mp4a.40.2' u 'opus')."""
    for fmt in info.get("requested_formats") or [info]:
        codec = fmt.get("acodec")
        if codec and codec != "none":
            return codec
    return None


def _ensure_aac_audio(filepath, info):
    """Si el audio no quedó en AAC (por ejemplo Opus), lo convierte sin tocar el video."""
    codec = _audio_codec(info)
    ffmpeg = shutil.which("ffmpeg")
    if not codec or codec.startswith("mp4a") or not ffmpeg or not os.path.isfile(filepath):
        return

    temp_path = f"{filepath}.aac.mp4"
    subprocess.run(
        [ffmpeg, "-y", "-i", filepath, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", temp_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    os.replace(temp_path, filepath)


def download_video(youtube_url, quality="media", progress_callback=None):
    """
    Descarga un video de YouTube en formato MP4 con la calidad especificada.

    Args:
        youtube_url (str): Enlace del video de YouTube.
        quality (str): Calidad del video. Opciones: baja/media/alta o 360p/720p/1080p.
        progress_callback (func): Función de callback para manejar el progreso.
    """
    output_folder = get_download_folder("video")

    def run(use_cookies):
        ydl_opts = {
            **get_base_ydl_opts(use_cookies),
            "format": QUALITY_MAP.get(quality, QUALITY_MAP["media"]),
            "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
            "merge_output_format": "mp4",
            "progress_hooks": [progress_callback] if progress_callback else [],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
        for download in info_dict.get("requested_downloads") or []:
            _ensure_aac_audio(download.get("filepath"), info_dict)
        return info_dict.get("title", "video")

    title = run_with_cookie_fallback(run)

    print(f"Video descargado exitosamente: {title}")
    return title
