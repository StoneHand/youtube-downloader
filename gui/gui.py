import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from downloader.audio import download_audio
from downloader.video import download_video

class YouTubeDownloaderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Descargador de YouTube")
        self.root.geometry("500x250")
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
        self.quality_combo = ttk.Combobox(self.root, values=["360p", "720p", "1080p"], state="readonly", width=10)
        self.quality_combo.pack(pady=5)
        self.quality_combo.set("720p")  # Valor predeterminado

        # Barra de progreso
        self.progress_label = tk.Label(self.root, text="Progreso:", font=("Arial", 10))
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

    def handle_audio_download(self):
        youtube_url = self.link_entry.get()
        if not youtube_url:
            self.show_message("Por favor, ingresa un enlace de YouTube.")
            return
        try:
            self.progress_bar.start()
            download_audio(youtube_url)
            self.progress_bar.stop()
            self.show_message("Audio descargado exitosamente.")
        except Exception as e:
            self.progress_bar.stop()
            self.show_message(f"Error al descargar audio: {e}")

    def handle_video_download(self):
        youtube_url = self.link_entry.get()
        if not youtube_url:
            self.show_message("Por favor, ingresa un enlace de YouTube.")
            return
        quality = self.quality_combo.get()
        try:
            self.progress_bar.start()
            download_video(youtube_url, quality)
            self.progress_bar.stop()
            self.show_message("Video descargado exitosamente.")
        except Exception as e:
            self.progress_bar.stop()
            self.show_message(f"Error al descargar video: {e}")

    def show_message(self, message):
        # Ventana emergente con un mensaje
        tk.messagebox.showinfo("Información", message)

    def run(self):
        self.root.mainloop()
