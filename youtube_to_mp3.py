import os
from yt_dlp import YoutubeDL
from pathlib import Path
import subprocess

DEFAULT_VIDEO_FORMAT = ".temp.mp4"
DEFAULT_AUDIO_FOLDER = "audio"
DEFAULT_VIDEO_FOLDER = "video"

def download_audio(youtube_url, download_folder):
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'keepvideo': False,  # Mantener el archivo de video original
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }]
    }
    
    with YoutubeDL(ydl_opts) as ydl_audio:
        info_dict = ydl_audio.extract_info(youtube_url, download=False)
        title = info_dict.get('title', None)
        ydl_audio.download([youtube_url])
        print(f"Audio descargado: {title}")
        return title
    
def download_video(youtube_url, download_folder):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4][height<=720]',
        'outtmpl': os.path.join(download_folder, '%(title)s.temp.%(ext)s'),
        'merge_output_format': 'mp4',
        'keepvideo': True
    }

    with YoutubeDL(ydl_opts) as ydl_video:
        info_dict = ydl_video.extract_info(youtube_url, download=False)
        title = info_dict.get('title', None)
        ydl_video.download([youtube_url])
        print(f"Video descargado: {title}")
        return title
    
def merge_video_audio(video_path, audio_path, output_path):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-c', 'copy',
        '-movflags', '+faststart',
        output_path
    ]
    subprocess.run(command)
    print(f"Video fusionado guardado como: {output_path}")
    os.remove(video_path)
    os.remove(audio_path)

def main():
    download_audio_folder = str(Path.cwd() / DEFAULT_AUDIO_FOLDER)
    download_video_folder = str(Path.cwd() / DEFAULT_VIDEO_FOLDER)

    while True:
        youtube_url = input("Introduce el enlace del video de YouTube (o 'salir' para terminar): ")
        if youtube_url.lower() == 'salir':
            break
        choice = input("¿Deseas descargar el audio (1) o el video (2)? ")
        if choice == '1':
            title = download_audio(youtube_url, download_audio_folder)
        elif choice == '2':
            audio_title = download_audio(youtube_url, download_audio_folder)
            video_title = download_video(youtube_url, download_video_folder)
            audio_path = os.path.join(download_audio_folder, f"{audio_title}.mp3")
            video_path = os.path.join(download_video_folder, video_title + DEFAULT_VIDEO_FORMAT)
            output_path = os.path.join(download_video_folder, f"{video_title}.mp4")
            merge_video_audio(video_path, audio_path, output_path)
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
