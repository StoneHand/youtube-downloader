from yt_dlp import YoutubeDL
from utils.file_utils import get_download_folder

def download_audio(youtube_url, progress_callback=None):
    """
    Descarga el audio de un video de YouTube en formato MP3.
    
    Args:
        youtube_url (str): Enlace del video de YouTube.
        progress_callback (func): Función de callback para manejar el progreso.
    """
    # Obtiene la carpeta de descargas para audio
    output_folder = get_download_folder("audio")

    # Opciones para yt_dlp
    ydl_opts = {
        'format': 'bestaudio',  # Descarga solo el mejor audio disponible
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',  # Plantilla de salida
        'progress_hooks': [progress_callback] if progress_callback else [],  # Callback de progreso
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Usa FFmpeg para extraer solo el audio
            'preferredcodec': 'mp3',  # Codificación MP3
            'preferredquality': '128',  # Calidad de audio
        }]
    }

    # Descarga el audio usando yt_dlp
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        title = info_dict.get('title', 'audio')  # Obtiene el título del video
        ydl.download([youtube_url])  # Inicia la descarga

    print(f"Audio descargado exitosamente: {title}")
    return title
