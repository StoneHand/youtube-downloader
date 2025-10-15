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
            quality = input("Selecciona el número para la calidad del video (baja=1, media=2, alta=3): ")
            if quality not in ['1', '2', '3']:
                print("Calidad no válida. Usando 720p por defecto.")
                quality = '720p'
            elif quality == '1':
                print("Seleccionaste baja calidad (360p).")
                quality = '360p'
            elif quality == '3':
                print("Seleccionaste alta calidad (1080p).")
                quality = '1080p'
            else:
                print("Seleccionaste calidad media (720p).")
                quality = '720p'
            download_video(youtube_url, quality=quality)
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
