from yt_dlp import YoutubeDL
from utils.file_utils import get_download_folder

def download_video(youtube_url, quality="720p"):
    output_folder = get_download_folder("video")
    quality_map = {
        '360p': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4][height<=360]',
        '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]',
        '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]',
    }
    ydl_opts = {
        'format': quality_map.get(quality, quality_map['720p']),
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    print(f"Video descargado exitosamente en {output_folder}.")
