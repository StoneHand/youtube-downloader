import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from downloader.audio import download_audio
from downloader.common import get_base_ydl_opts, run_with_cookie_fallback
from downloader.video import download_video
from utils.error_messages import friendly_error
from utils.url_utils import normalize_youtube_url
from yt_dlp import YoutubeDL


FONT = ("Arial", 16)
FONT_BOLD = ("Arial", 16, "bold")


class YouTubeDownloaderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Descargar videos de YouTube")
        self.root.resizable(False, False)
        self._download_in_progress = False
        self._configure_fonts()

        self.link_frame = tk.Frame(self.root)
        self.link_frame.pack(padx=20, pady=(20, 10))

        self.link_label = tk.Label(self.link_frame, text="Link de YouTube:", font=FONT)
        self.link_label.pack(side=tk.LEFT, padx=5)
        self.link_entry = tk.Entry(self.link_frame, width=40, font=FONT)
        self.link_entry.pack(side=tk.LEFT, padx=5, ipady=6)

        self.paste_button = tk.Button(
            self.link_frame,
            text="Pegar",
            font=FONT_BOLD,
            bg="yellow",
            width=8,
            height=2,
            command=self.paste_link,
        )
        self.paste_button.pack(side=tk.LEFT, padx=5)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(padx=20, pady=20)

        self.audio_button = tk.Button(
            self.buttons_frame,
            text="Descargar Audio",
            bg="lightgreen",
            font=FONT_BOLD,
            width=16,
            height=2,
            command=self.handle_audio_download,
        )
        self.audio_button.grid(row=0, column=0, padx=10)

        self.video_button = tk.Button(
            self.buttons_frame,
            text="Descargar Video",
            bg="lightblue",
            font=FONT_BOLD,
            width=16,
            height=2,
            command=self.handle_video_download,
        )
        self.video_button.grid(row=0, column=1, padx=10)

        self.quality_label = tk.Label(self.buttons_frame, text="Calidad:", font=FONT)
        self.quality_label.grid(row=0, column=2, padx=(20, 5))
        self.quality_combo = ttk.Combobox(
            self.buttons_frame,
            values=["baja", "media", "alta"],
            state="readonly",
            width=8,
            font=FONT,
        )
        self.quality_combo.grid(row=0, column=3, padx=5)
        self.quality_combo.set("media")

        self.progress_label = tk.Label(self.root, text="Progreso:", font=FONT)
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(
            self.root, orient="horizontal", length=700, mode="determinate"
        )
        self.progress_bar.pack(pady=10)

        self.status_label = tk.Label(self.root, text="", font=FONT)
        self.status_label.pack(pady=(0, 20))

        self._center_window()

    def _configure_fonts(self):
        """Letra grande también en la lista de calidades y en los cuadros de mensaje."""
        self.root.option_add("*TCombobox*Listbox.font", FONT)
        self.root.option_add("*Dialog.msg.font", FONT)
        self.root.option_add("*Dialog.msg.wrapLength", "6i")
        style = ttk.Style(self.root)
        style.configure("TButton", font=FONT_BOLD, padding=8)

    def _center_window(self):
        self.root.update_idletasks()
        width, height = self.root.winfo_reqwidth(), self.root.winfo_reqheight()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 3
        self.root.geometry(f"+{x}+{y}")

    def fetch_title(self, youtube_url):
        """Obtiene el título del video sin descargarlo. Devuelve (título, error)."""
        def fetch(use_cookies):
            with YoutubeDL({**get_base_ydl_opts(use_cookies), "quiet": True}) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                return info.get("title", "Video desconocido")

        try:
            return run_with_cookie_fallback(fetch), None
        except Exception as error:
            print(f"Error al obtener el título: {error}")
            return None, error

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
            self.show_error("No se pudo pegar el enlace.\n\nPrimero copia el enlace del video en YouTube.")

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
        self._start_download("audio")

    def handle_video_download(self):
        self._start_download("video")

    def _start_download(self, kind):
        if self._download_in_progress:
            return

        youtube_url = normalize_youtube_url(self.link_entry.get())
        if not youtube_url:
            self.show_error(
                "Por favor, pega un enlace de YouTube.\n\n"
                "Copia el enlace del video y presiona el botón Pegar."
            )
            return

        quality = self.quality_combo.get()
        self._set_download_state(True)
        self.progress_bar["value"] = 0
        self.status_label.config(text="Buscando el video, espera un momento...")

        threading.Thread(
            target=self._fetch_title_worker,
            args=(youtube_url, kind, quality),
            daemon=True,
        ).start()

    def _fetch_title_worker(self, youtube_url, kind, quality):
        title, error = self.fetch_title(youtube_url)
        self.root.after(
            0, lambda: self._on_title_fetched(youtube_url, kind, quality, title, error)
        )

    def _on_title_fetched(self, youtube_url, kind, quality, title, error):
        if error is not None:
            self._finish_download()
            self.show_error(friendly_error(error))
            return

        if not self.show_confirmation(title, kind):
            self._finish_download()
            return

        self.status_label.config(text=f"Descargando {kind}...")
        threading.Thread(
            target=self._download_worker,
            args=(youtube_url, kind, quality),
            daemon=True,
        ).start()

    def _download_worker(self, youtube_url, kind, quality):
        try:
            if kind == "audio":
                download_audio(youtube_url, self.progress_hook)
            else:
                download_video(youtube_url, quality, self.progress_hook)
        except Exception as error:
            print(f"Error al descargar {kind}: {error}")
            # `error` se borra al salir del except: se guarda el texto antes de usarlo en after().
            message = friendly_error(error)
            self.root.after(0, lambda: self.show_error(message))
        else:
            self.root.after(
                0, lambda: self.show_message(f"{kind.capitalize()} descargado exitosamente.")
            )
        finally:
            self.root.after(0, self._finish_download)

    def _finish_download(self):
        self._reset_progress()
        self._set_download_state(False)

    def progress_hook(self, progress_data):
        if progress_data.get("status") != "downloading":
            return

        downloaded_bytes = progress_data.get("downloaded_bytes") or 0
        total_bytes = (
            progress_data.get("total_bytes")
            or progress_data.get("total_bytes_estimate")
            or 0
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

    def show_error(self, message):
        messagebox.showerror("Ocurrió un problema", message)

    def run(self):
        self.root.mainloop()
