
# YouTube Downloader

Un proyecto simple para descargar videos y audio de YouTube, desarrollado en Python con una interfaz gráfica usando Tkinter.

## Características

- **Descarga de audio** en formato MP3 con calidad de 128 kbps.
- **Descarga de video** en formato MP4 con opciones de calidad (360p, 720p, 1080p).
- Interfaz gráfica intuitiva con barra de progreso.
- Organización modular del código para fácil mantenimiento y escalabilidad.

## Requisitos

1. **Python** (versión 3.10 o superior)
2. **Librerías de Python**:
   - `yt-dlp`
   - `tkinter`
3. **FFmpeg**:
   - Necesario para la conversión de audio y la fusión de video y audio.

## Instalación

1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/usuario/youtube-downloader.git
   cd youtube-downloader
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Descarga e instala FFmpeg**:
   - [Descarga FFmpeg aquí](https://ffmpeg.org/download.html).
   - Añade FFmpeg al PATH del sistema para que esté accesible desde la línea de comandos.

## Uso

### **Interfaz Gráfica**
1. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```
2. Ingresa el enlace de YouTube en el campo correspondiente.
3. Selecciona:
   - **Descargar audio**: Guarda el archivo como MP3.
   - **Descargar video**: Guarda el archivo como MP4 con la calidad seleccionada.

### **Opciones de Calidad de Video**
- La aplicación permite elegir entre:
  - **360p**
  - **720p**
  - **1080p**
- Si la calidad no está disponible para un video, se seleccionará automáticamente la más cercana.

## Organización del Proyecto

El proyecto sigue un **patrón modular** para mantener la separación de responsabilidades:

```
youtube-downloader/
│
├── downloader/
│   ├── audio.py       # Lógica para descargar audio
│   ├── video.py       # Lógica para descargar video
│   └── utils.py       # Funciones auxiliares compartidas
│
├── gui/
│   └── gui.py         # Interfaz gráfica con Tkinter
│
├── main.py            # Punto de entrada principal
├── requirements.txt   # Lista de dependencias
└── README.md          # Documentación del proyecto
```

## Contribuciones

Si deseas contribuir, sigue estos pasos:

1. Haz un fork de este repositorio.
2. Crea una rama para tu feature:
   ```bash
   git checkout -b feature-nueva-funcionalidad
   ```
3. Realiza un pull request detallando tus cambios.

## Licencia

Este proyecto está bajo la [Licencia MIT](https://opensource.org/licenses/MIT). Siéntete libre de usarlo, modificarlo y distribuirlo.

---

### Contacto

Si tienes alguna pregunta o sugerencia, ¡no dudes en contactarme!
