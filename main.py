from gui.gui import YouTubeDownloaderApp
from utils.update_checker import check_and_update_yt_dlp

def main():
    # Verificar y actualizar yt-dlp antes de ejecutar el programa
    check_and_update_yt_dlp()

    # Continuar con la lógica principal del programa
    print("Iniciando el descargador de YouTube...")
    # Ejecutar gui
    app = YouTubeDownloaderApp()
    app.run()

if __name__ == "__main__":
    main()

