# YouTube Downloader

Aplicación de escritorio, hecha en Python con Tkinter, para descargar videos (MP4) o solo el audio (MP3) de YouTube de forma sencilla. Está pensada para personas con poca experiencia en computadores: se pega el enlace, se elige "Descargar Audio" o "Descargar Video" y se confirma.

## Características

- **Descarga de video** en MP4 con tres calidades: baja (360p), media (720p, por defecto) y alta (1080p). Si el video no tiene la calidad pedida, se usa la más cercana disponible.
- **Descarga de audio** en MP3 a 128 kbps.
- Interfaz con letra y botones grandes, botón **Pegar** y barra de progreso.
- Confirmación con el título del video antes de descargar.
- Mensajes de error en español y sin términos técnicos (sin internet, video privado, video no disponible, etc.).
- Solo descarga el video indicado, aunque el enlace pertenezca a una lista de reproducción.
- Revisa y actualiza `yt-dlp` en segundo plano al iniciar, sin retrasar la apertura de la ventana. La versión nueva se usa la próxima vez que se abra la app.

## Dónde quedan los archivos

En la carpeta de descargas del usuario:

- Videos: `Descargas/video/`
- Audio: `Descargas/audio/`

En Linux se respeta el nombre real de la carpeta (por ejemplo `~/Descargas` en Ubuntu en español, leído de `~/.config/user-dirs.dirs`). En Windows es `Downloads` dentro del perfil del usuario.

## Requisitos

| Requisito | Para qué sirve | Obligatorio |
|---|---|---|
| **Python 3.10 o superior**, con Tkinter | Ejecutar la aplicación | Sí |
| **yt-dlp** (`pip install -r requirements.txt`) | Descargar desde YouTube | Sí |
| **FFmpeg** en el PATH | Convertir a MP3 y unir video con audio | Sí |
| **Deno** o **Node.js** en el PATH | YouTube requiere un runtime JavaScript para resolver los enlaces | Recomendado |

## Instalación

### Ubuntu / Debian

```bash
git clone https://github.com/StoneHand/youtube-downloader.git
cd youtube-downloader

sudo apt update
sudo apt install -y python3 python3-pip python3-tk ffmpeg nodejs

pip install -r requirements.txt
```

Si `pip` indica `externally-managed-environment`, usa un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows

1. Instala [Python 3.10+](https://www.python.org/downloads/) marcando **"Add Python to PATH"** (incluye Tkinter).
2. Instala FFmpeg, por ejemplo desde una terminal: `winget install ffmpeg` (o descárgalo desde [ffmpeg.org](https://ffmpeg.org/download.html) y agrega su carpeta `bin` al PATH).
3. Instala [Node.js](https://nodejs.org/) o [Deno](https://docs.deno.com/runtime/).
4. Clona el repositorio e instala las dependencias:
   ```bat
   git clone https://github.com/StoneHand/youtube-downloader.git
   cd youtube-downloader
   python -m pip install -r requirements.txt
   ```

**Instalación guiada en `D:\Dev`:** el script `setup_d_dev.bat` crea `D:\Dev`, clona o actualiza el repositorio (rama `main`), instala las dependencias de Python y avisa si faltan FFmpeg o Deno/Node. No instala FFmpeg ni Deno/Node por ti.

### macOS

```bash
brew install python-tk ffmpeg node
pip3 install -r requirements.txt
```

### Comprobar la instalación

Al iniciar, la aplicación imprime en la consola si falta FFmpeg, un runtime JavaScript o yt-dlp. También puedes comprobarlo a mano:

```bash
python3 --version
ffmpeg -version
node --version
```

## Uso

### Interfaz gráfica

```bash
python main.py
```

1. Copia el enlace del video en YouTube y presiona **Pegar** (o escríbelo en el cuadro).
2. Presiona **Descargar Audio** (MP3) o **Descargar Video** (MP4). Para video, elige antes la **Calidad**.
3. Revisa el título del video en el cuadro de confirmación y acepta.
4. Espera a que termine la barra de progreso y el aviso "descargado exitosamente".

### Sin interfaz (terminal)

```bash
python main_without_gui.py
```

Pide el enlace por consola y permite elegir audio o video, con calidad baja (1), media (2) o alta (3).

## Solución de problemas

| Mensaje o síntoma | Qué hacer |
|---|---|
| "No hay conexión a internet" | Revisar la conexión y reintentar. |
| "Falta un programa necesario (FFmpeg)" | Instalar FFmpeg y confirmar que `ffmpeg -version` funciona en una terminal nueva. |
| "YouTube pidió verificar que eres una persona" | Reintentar más tarde o usar cookies (ver abajo). |
| "No se pudo leer la información de tu navegador" / `Could not copy Chrome cookie database` | Hay una variable `YTDLP_COOKIES_BROWSER` configurada y el navegador no deja leer sus cookies. La app ya reintenta sin cookies; si igual falla, cierra el navegador por completo o elimina la variable (ver abajo). |
| "Este video no está disponible" / "es privado" | El video fue borrado, es privado o está bloqueado en tu país. |
| "El enlace no parece ser de un video de YouTube" | Copiar el enlace completo desde la barra de direcciones o con "Compartir". |
| Se ve pequeña o no se ve la ventana | Los tamaños están en `gui/gui.py` (`FONT` y `FONT_BOLD`). |

### Cookies (cuando YouTube pide verificación)

Las cookies son **opcionales**: solo se usan si defines una de estas variables de entorno antes de ejecutar la aplicación. Si las cookies del navegador no se pueden leer, la app reintenta automáticamente sin ellas.

- `YTDLP_COOKIES_BROWSER`: navegador desde el que leer las cookies (`firefox`, `edge`, `chrome`, ...).
- `YTDLP_COOKIES_FILE`: ruta a un archivo de cookies exportado.

> En Windows, Chrome (y otros navegadores basados en Chromium) bloquean la lectura de sus cookies mientras están abiertos y, en versiones recientes, las cifran de forma que yt-dlp no puede leerlas. Para esos casos es más fiable Firefox o un archivo de cookies exportado.

```bash
# Linux / macOS
YTDLP_COOKIES_BROWSER=firefox python main.py
```

```bat
:: Windows (solo para esta ventana de consola)
set YTDLP_COOKIES_BROWSER=firefox
python main.py
```

**Quitar la variable si quedó configurada de forma permanente en Windows** (por ejemplo con `setx`):

```bat
echo %YTDLP_COOKIES_BROWSER%
reg delete HKCU\Environment /v YTDLP_COOKIES_BROWSER /f
```

Después cierra y vuelve a abrir la consola.

## Actualizar el proyecto

- **Linux / macOS:** `git pull origin main`
- **Windows:** ejecutar `update_proyect.bat`. Guarda tus cambios locales (si los hay), hace `git pull --rebase` y los restaura.

## Organización del proyecto

```
youtube-downloader/
├── downloader/
│   ├── common.py          # Opciones compartidas de yt-dlp (runtime JS, cookies, reintentos)
│   ├── audio.py           # Descarga de audio (MP3)
│   └── video.py           # Descarga de video (MP4) y mapa de calidades
├── gui/
│   └── gui.py             # Interfaz gráfica con Tkinter
├── utils/
│   ├── environment.py     # Comprobación de FFmpeg, runtime JS y yt-dlp
│   ├── error_messages.py  # Traduce errores técnicos a mensajes simples en español
│   ├── file_utils.py      # Carpeta de descargas según el sistema operativo
│   ├── update_checker.py  # Instalación y actualización de yt-dlp
│   └── url_utils.py       # Validación de enlaces de YouTube
├── main.py                # Punto de entrada con interfaz gráfica
├── main_without_gui.py    # Punto de entrada por consola
├── requirements.txt       # Dependencias de Python
├── setup_d_dev.bat        # Instalación guiada en D:\Dev (Windows)
└── update_proyect.bat     # Actualización del repositorio (Windows)
```

## Contribuciones

1. Haz un fork de este repositorio.
2. Crea una rama para tu cambio: `git checkout -b feature-nueva-funcionalidad`
3. Abre un pull request describiendo tus cambios.

## Licencia

Este proyecto está bajo la [Licencia MIT](https://opensource.org/licenses/MIT). Puedes usarlo, modificarlo y distribuirlo.

> Descarga solo contenido que tengas derecho a guardar. Respeta los términos de servicio de YouTube y las leyes de derechos de autor de tu país.
