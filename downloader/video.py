from yt_dlp import YoutubeDL

from downloader.common import get_base_ydl_opts
from utils.file_utils import get_download_folder

QUALITY_MAP = {
    "baja": "bv*[height<=360]+ba/b[height<=360]",
    "media": "bv*[height<=720]+ba/b[height<=720]",
    "alta": "bv*[height<=1080]+ba/b[height<=1080]",
    "360p": "bv*[height<=360]+ba/b[height<=360]",
    "720p": "bv*[height<=720]+ba/b[height<=720]",
    "1080p": "bv*[height<=1080]+ba/b[height<=1080]",
}


def download_video(youtube_url, quality="media", progress_callback=None):
    """
    Descarga un video de YouTube en formato MP4 con la calidad especificada.

    Args:
        youtube_url (str): Enlace del video de YouTube.
        quality (str): Calidad del video. Opciones: baja/media/alta o 360p/720p/1080p.
        progress_callback (func): Función de callback para manejar el progreso.
    """
    output_folder = get_download_folder("video")

    ydl_opts = {
        **get_base_ydl_opts(),
        "format": QUALITY_MAP.get(quality, QUALITY_MAP["media"]),
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "progress_hooks": [progress_callback] if progress_callback else [],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        title = info_dict.get("title", "video")
        ydl.download([youtube_url])

    print(f"Video descargado exitosamente: {title}")
    return title
