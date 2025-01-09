from downloader.audio import download_audio
from downloader.video import download_video

def main():
    while True:
        youtube_url = input("Introduce el enlace del video de YouTube (o 'salir' para terminar): ")
        if youtube_url.lower() == 'salir':
            break
        choice = input("¿Deseas descargar el audio (1) o el video (2)? ")
        if choice == '1':
            download_audio(youtube_url)
        elif choice == '2':
            quality = input("Selecciona la calidad del video (360p, 720p, 1080p): ")
            if quality not in ['360p', '720p', '1080p']:
                print("Calidad no válida. Usando 720p por defecto.")
                quality = '720p'
            download_video(youtube_url, quality=quality)
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
