import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from downloader.audio import download_audio
from downloader.video import download_video

class YouTubeDownloaderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Youtube Downloader")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        # Campo de entrada para el enlace de YouTube
        self.link_label = tk.Label(self.root, text="Link de YouTube:", font=("Arial", 12))
        self.link_label.pack(pady=10)
        self.link_entry = tk.Entry(self.root, width=60, font=("Arial", 10))
        self.link_entry.pack(pady=5)

        # Frame para botones
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=20)

        # Botón para descargar audio
        self.audio_button = tk.Button(
            self.buttons_frame,
            text="Descargar Audio",
            bg="lightgreen",
            font=("Arial", 10),
            command=self.handle_audio_download
        )
        self.audio_button.grid(row=0, column=0, padx=10)

        # Botón para descargar video
        self.video_button = tk.Button(
            self.buttons_frame,
            text="Descargar Video",
            bg="lightblue",
            font=("Arial", 10),
            command=self.handle_video_download
        )
        self.video_button.grid(row=0, column=1, padx=10)

        # Selección de calidad para video
        self.quality_label = tk.Label(self.root, text="Calidad de video:", font=("Arial", 10))
        self.quality_label.pack()
        self.quality_combo = ttk.Combobox(self.root, values=["baja", "media", "alta"], state="readonly", width=10)
        self.quality_combo.pack(pady=5)
        self.quality_combo.set("media")  # Valor predeterminado

        # Barra de progreso
        self.progress_label = tk.Label(self.root, text="Progreso:", font=("Arial", 10))
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Etiqueta para mostrar estado
        self.status_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.status_label.pack()

    def fetch_title(self, youtube_url):
        """
        Obtiene el título del video de YouTube sin descargarlo.
        """
        from yt_dlp import YoutubeDL
        try:
            with YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                return info.get('title', 'Video desconocido')
        except Exception as e:
            return None

    def show_confirmation(self, title, action):
        """
        Muestra un popup de confirmación antes de proceder con la descarga.
        """
        return messagebox.askyesno(
            "Confirmación",
            f"¿Deseas descargar el {action} con el nombre:\n\n'{title}'?"
        )

    def handle_audio_download(self):
        youtube_url = self.link_entry.get()
        if not youtube_url:
            self.show_message("Por favor, ingresa un enlace de YouTube.")
            return

        title = self.fetch_title(youtube_url)
        if not title:
            self.show_message("Error al obtener el título del video.")
            return

        if not self.show_confirmation(title, "audio"):
            return

        try:
            self.progress_bar["value"] = 0
            self.status_label.config(text="Descargando audio...")
            download_audio(youtube_url, self.progress_hook)
            self.show_message("Audio descargado exitosamente.")
        except Exception as e:
            self.show_message(f"Error al descargar audio: {e}")
        finally:
            self.progress_bar["value"] = 0
            self.status_label.config(text="")

    def handle_video_download(self):
        youtube_url = self.link_entry.get()
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
        try:
            self.progress_bar["value"] = 0
            self.status_label.config(text="Descargando video...")
            download_video(youtube_url, quality, self.progress_hook)
            self.show_message("Video descargado exitosamente.")
        except Exception as e:
            self.show_message(f"Error al descargar video: {e}")
        finally:
            self.progress_bar["value"] = 0
            self.status_label.config(text="")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            downloaded_bytes = d.get('downloaded_bytes', 0)
            total_bytes = d.get('total_bytes', d.get('total_bytes_estimate', 0))
            if total_bytes > 0:
                progress = int(downloaded_bytes / total_bytes * 100)
                self.progress_bar["value"] = progress
                self.status_label.config(text=f"Progreso: {progress}%")
                self.root.update_idletasks()

    def show_message(self, message):
        # Ventana emergente con un mensaje
        messagebox.showinfo("Información", message)

    def run(self):
        self.root.mainloop()
