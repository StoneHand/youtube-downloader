import re

ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")
MAX_DETAIL_LENGTH = 200

# (fragmentos en minúsculas del error original, mensaje para el usuario)
KNOWN_ERRORS = [
    (
        ("temporary failure in name resolution", "getaddrinfo failed", "urlopen error",
         "network is unreachable", "timed out", "connection reset", "connection aborted"),
        "No hay conexión a internet.\n\nRevisa que el computador esté conectado y vuelve a intentar.",
    ),
    (
        ("ffmpeg", "ffprobe"),
        "Falta un programa necesario (FFmpeg) para terminar la descarga.\n\n"
        "Pide ayuda para instalarlo.",
    ),
    (
        ("sign in to confirm", "not a bot", "cookies"),
        "YouTube pidió verificar que eres una persona y no dejó descargar este video.\n\n"
        "Intenta de nuevo más tarde o pide ayuda.",
    ),
    (
        ("private video",),
        "Este video es privado y no se puede descargar.",
    ),
    (
        ("confirm your age", "age-restricted", "age restricted"),
        "Este video tiene restricción de edad y no se puede descargar.",
    ),
    (
        ("video unavailable", "video is not available", "has been removed", "this video is unavailable"),
        "Este video no está disponible. Puede que lo hayan borrado o que no se pueda ver en tu país.",
    ),
    (
        ("unsupported url", "is not a valid url", "incomplete youtube id"),
        "El enlace no parece ser de un video de YouTube.\n\nCopia el enlace completo desde YouTube.",
    ),
    (
        ("no space left", "disk full"),
        "No hay espacio suficiente en el disco para guardar el archivo.",
    ),
]


def friendly_error(error):
    """Convierte un error técnico (por lo general de yt-dlp) en un mensaje simple en español."""
    raw = ANSI_ESCAPE.sub("", str(error)).strip()
    lowered = raw.lower()

    for fragments, message in KNOWN_ERRORS:
        if any(fragment in lowered for fragment in fragments):
            return message

    detail = raw[:MAX_DETAIL_LENGTH] + ("..." if len(raw) > MAX_DETAIL_LENGTH else "")
    return (
        "Ocurrió un problema y no se pudo completar la descarga.\n\n"
        "Intenta de nuevo. Si sigue pasando, pide ayuda.\n\n"
        f"Detalle técnico: {detail}"
    )
