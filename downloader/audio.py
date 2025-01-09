from yt_dlp import YoutubeDL
from utils.file_utils import get_download_folder

def download_audio(youtube_url):
    output_folder = get_download_folder("audio")
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }]
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    print(f"Audio descargado exitosamente en {output_folder}.")
