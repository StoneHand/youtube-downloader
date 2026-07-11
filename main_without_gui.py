from downloader.audio import download_audio
from downloader.video import download_video
from utils.environment import print_environment_status
from utils.update_checker import check_and_update_yt_dlp

QUALITY_CHOICES = {
    "1": ("baja", "360p"),
    "2": ("media", "720p"),
    "3": ("alta", "1080p"),
}


def main():
    check_and_update_yt_dlp()
    print_environment_status()

    while True:
        youtube_url = input(
            "Introduce el enlace del video de YouTube (o 'salir' para terminar): "
        ).strip()
        if youtube_url.lower() == "salir":
            break

        choice = input("¿Deseas descargar el audio (1) o el video (2)? ").strip()
        if choice == "1":
            try:
                download_audio(youtube_url)
            except Exception as error:
                print(f"Error al descargar audio: {error}")
        elif choice == "2":
            quality_choice = input(
                "Selecciona el número para la calidad del video (baja=1, media=2, alta=3): "
            ).strip()
            quality_key, quality_label = QUALITY_CHOICES.get(
                quality_choice, ("media", "720p")
            )
            print(f"Seleccionaste calidad {quality_key} ({quality_label}).")
            try:
                download_video(youtube_url, quality=quality_key)
            except Exception as error:
                print(f"Error al descargar video: {error}")
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
