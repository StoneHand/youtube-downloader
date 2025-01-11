from yt_dlp import YoutubeDL
from utils.file_utils import get_download_folder

def download_video(youtube_url, quality="media", progress_callback=None):
    """
    Descarga un video de YouTube en formato MP4 con la calidad especificada.
    
    Args:
        youtube_url (str): Enlace del video de YouTube.
        progress_callback (func): Función de callback para manejar el progreso.
        quality (str): Calidad del video. Opciones: "baja", "media", "alta".
    """
    # Obtiene la carpeta de descargas para video
    output_folder = get_download_folder("video")

    # Mapeo de calidades
    quality_map = {
        'baja': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4][height<=360]',
        'media': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]',
        'alta': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]',
    }

    # Opciones para yt_dlp
    ydl_opts = {
        'format': quality_map.get(quality, quality_map['media']),  # Selección de calidad
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',  # Plantilla de salida
        'merge_output_format': 'mp4',  # Formato final
        'progress_hooks': [progress_callback] if progress_callback else [],  # Callback de progreso
    }

    # Descarga el video usando yt_dlp
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        title = info_dict.get('title', 'video')  # Obtiene el título del video
        ydl.download([youtube_url])  # Inicia la descarga

    print(f"Video descargado exitosamente: {title}")
    return title
