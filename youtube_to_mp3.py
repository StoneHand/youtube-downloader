import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment
from pathlib import Path

def download_audio(youtube_url, download_folder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'keepvideo': True,  # Mantener el archivo de video original
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        title = info_dict.get('title', None)
        ydl.download([youtube_url])
        return title

def convert_to_mp3(download_folder, title):
    webm_path = os.path.join(download_folder, f"{title}.webm")
    mp3_path = os.path.join(download_folder, f"{title}.mp3")

    if os.path.exists(webm_path):
        print(f"Convirtiendo {webm_path} a {mp3_path}...")
        audio = AudioSegment.from_file(webm_path)
        audio.export(mp3_path, format="mp3", bitrate="128k")
        os.remove(webm_path)  # Eliminar el archivo original después de la conversión
        print(f"Convertido y guardado: {mp3_path}")

def download_video(youtube_url, download_folder):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        title = info_dict.get('title', None)
        ydl.download([youtube_url])
        print(f"Video descargado: {title}.mp4")

def main():
    download_folder = str(Path.home() / "Downloads")

    while True:
        youtube_url = input("Introduce el enlace del video de YouTube (o 'salir' para terminar): ")
        if youtube_url.lower() == 'salir':
            break
        choice = input("¿Deseas descargar el audio en formato MP3 (1) o el video completo (2)? ")
        if choice == '1':
            title = download_audio(youtube_url, download_folder)
            if title:
                convert_to_mp3(download_folder, title)
        elif choice == '2':
            download_video(youtube_url, download_folder)
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
