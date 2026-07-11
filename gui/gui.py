import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from downloader.audio import download_audio
from downloader.common import get_base_ydl_opts
from downloader.video import download_video
from yt_dlp import YoutubeDL


class YouTubeDownloaderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Youtube Downloader")
        self.root.geometry("600x200")
        self.root.resizable(False, False)
        self._download_in_progress = False

        self.link_frame = tk.Frame(self.root)
        self.link_frame.pack(pady=10)

        self.link_label = tk.Label(self.link_frame, text="Link de YouTube:", font=("Arial", 12))
        self.link_label.pack(side=tk.LEFT, padx=5)
        self.link_entry = tk.Entry(self.link_frame, width=50, font=("Arial", 10))
        self.link_entry.pack(side=tk.LEFT, padx=5)

        self.paste_button = tk.Button(
            self.link_frame,
            text="Pegar",
            font=("Arial", 10),
            bg="yellow",
            command=self.paste_link,
        )
        self.paste_button.pack(side=tk.LEFT, padx=5)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=20)

        self.audio_button = tk.Button(
            self.buttons_frame,
            text="Descargar Audio",
            bg="lightgreen",
            font=("Arial", 10),
            command=self.handle_audio_download,
        )
        self.audio_button.grid(row=0, column=0, padx=10)

        self.video_button = tk.Button(
            self.buttons_frame,
            text="Descargar Video",
            bg="lightblue",
            font=("Arial", 10),
            command=self.handle_video_download,
        )
        self.video_button.grid(row=0, column=1, padx=10)

        self.quality_label = tk.Label(self.buttons_frame, text="Calidad:", font=("Arial", 10))
        self.quality_label.grid(row=0, column=2, padx=5)
        self.quality_combo = ttk.Combobox(
            self.buttons_frame,
            values=["baja", "media", "alta"],
            state="readonly",
            width=10,
        )
        self.quality_combo.grid(row=0, column=3, padx=5)
        self.quality_combo.set("media")

        self.progress_label = tk.Label(self.root, text="Progreso:", font=("Arial", 10))
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(
            self.root, orient="horizontal", length=400, mode="determinate"
        )
        self.progress_bar.pack(pady=10)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.status_label.pack()

    def fetch_title(self, youtube_url):
        """Obtiene el título del video de YouTube sin descargarlo."""
        try:
            with YoutubeDL({**get_base_ydl_opts(), "quiet": True}) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                return info.get("title", "Video desconocido")
        except Exception:
            return None

    def show_confirmation(self, title, action):
        """Muestra un popup de confirmación antes de proceder con la descarga."""
        return messagebox.askyesno(
            "Confirmación",
            f"¿Deseas descargar el {action} con el nombre:\n\n'{title}'?",
        )

    def paste_link(self):
        """Pega el contenido del portapapeles en el cuadro de entrada del enlace."""
        try:
            clipboard_content = self.root.clipboard_get()
            self.link_entry.delete(0, tk.END)
            self.link_entry.insert(0, clipboard_content)
        except tk.TclError:
            self.show_message("No se pudo pegar el enlace del portapapeles.")

    def _set_download_state(self, in_progress):
        self._download_in_progress = in_progress
        state = tk.DISABLED if in_progress else tk.NORMAL
        self.audio_button.config(state=state)
        self.video_button.config(state=state)
        self.paste_button.config(state=state)
        self.quality_combo.config(state="disabled" if in_progress else "readonly")

    def _reset_progress(self):
        self.progress_bar["value"] = 0
        self.status_label.config(text="")

    def handle_audio_download(self):
        if self._download_in_progress:
            return

        youtube_url = self.link_entry.get().strip()
        if not youtube_url:
            self.show_message("Por favor, ingresa un enlace de YouTube.")
            return

        title = self.fetch_title(youtube_url)
        if not title:
            self.show_message("Error al obtener el título del video.")
            return

        if not self.show_confirmation(title, "audio"):
            return

        self._set_download_state(True)
        self.progress_bar["value"] = 0
        self.status_label.config(text="Descargando audio...")

        threading.Thread(
            target=self._download_audio_worker,
            args=(youtube_url,),
            daemon=True,
        ).start()

    def handle_video_download(self):
        if self._download_in_progress:
            return

        youtube_url = self.link_entry.get().strip()
        if not youtube_url:
            self.show_message("Por favor, ingresa un enlace de YouTube.")
            return

        title = self.fetch_title(youtube_url)
        if not title:
            self.show_message("Error al obtener el título del video.")
            return

        if not self.show_confirmation(title, "video"):
            return

        quality = self.quality_combo.get()
        self._set_download_state(True)
        self.progress_bar["value"] = 0
        self.status_label.config(text="Descargando video...")

        threading.Thread(
            target=self._download_video_worker,
            args=(youtube_url, quality),
            daemon=True,
        ).start()

    def _download_audio_worker(self, youtube_url):
        try:
            download_audio(youtube_url, self.progress_hook)
            self.root.after(0, lambda: self.show_message("Audio descargado exitosamente."))
        except Exception as error:
            self.root.after(
                0,
                lambda: self.show_message(f"Error al descargar audio: {error}"),
            )
        finally:
            self.root.after(0, self._finish_download)

    def _download_video_worker(self, youtube_url, quality):
        try:
            download_video(youtube_url, quality, self.progress_hook)
            self.root.after(0, lambda: self.show_message("Video descargado exitosamente."))
        except Exception as error:
            self.root.after(
                0,
                lambda: self.show_message(f"Error al descargar video: {error}"),
            )
        finally:
            self.root.after(0, self._finish_download)

    def _finish_download(self):
        self._reset_progress()
        self._set_download_state(False)

    def progress_hook(self, progress_data):
        if progress_data.get("status") != "downloading":
            return

        downloaded_bytes = progress_data.get("downloaded_bytes", 0)
        total_bytes = progress_data.get(
            "total_bytes", progress_data.get("total_bytes_estimate", 0)
        )
        if total_bytes <= 0:
            return

        progress = int(downloaded_bytes / total_bytes * 100)

        def update_ui():
            self.progress_bar["value"] = progress
            self.status_label.config(text=f"Progreso: {progress}%")

        self.root.after(0, update_ui)

    def show_message(self, message):
        messagebox.showinfo("Información", message)

    def run(self):
        self.root.mainloop()
