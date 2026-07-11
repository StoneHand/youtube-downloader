from gui.gui import YouTubeDownloaderApp
from utils.environment import print_environment_status
from utils.update_checker import check_and_update_yt_dlp


def main():
    check_and_update_yt_dlp()
    print_environment_status()
    print("Iniciando el descargador de YouTube...")
    app = YouTubeDownloaderApp()
    app.run()

if __name__ == "__main__":
    main()

