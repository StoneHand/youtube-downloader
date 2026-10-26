import threading

from utils.environment import print_environment_status
from utils.update_checker import check_and_update_yt_dlp, ensure_yt_dlp_installed


def main():
    # Solo se bloquea el arranque si falta yt-dlp; las actualizaciones corren en segundo plano.
    ensure_yt_dlp_installed()

    from gui.gui import YouTubeDownloaderApp

    print_environment_status()
    print("Iniciando el descargador de YouTube...")
    app = YouTubeDownloaderApp()
    threading.Thread(target=check_and_update_yt_dlp, daemon=True).start()
    app.run()

if __name__ == "__main__":
    main()
