from yt_dlp import YoutubeDL

from downloader.common import get_base_ydl_opts
from utils.file_utils import get_download_folder


def download_audio(youtube_url, progress_callback=None):
    """
    Descarga el audio de un video de YouTube en formato MP3.

    Args:
        youtube_url (str): Enlace del video de YouTube.
        progress_callback (func): Función de callback para manejar el progreso.
    """
    output_folder = get_download_folder("audio")

    ydl_opts = {
        **get_base_ydl_opts(),
        "format": "bestaudio/best",
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "progress_hooks": [progress_callback] if progress_callback else [],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        title = info_dict.get("title", "audio")
        ydl.download([youtube_url])

    print(f"Audio descargado exitosamente: {title}")
    return title
