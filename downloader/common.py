"""Opciones compartidas de yt-dlp para descargas actuales de YouTube."""

import os
import re
import shutil


def _find_js_runtime():
    """Busca un runtime JavaScript compatible con yt-dlp (Deno o Node)."""
    for runtime in ("deno", "node"):
        path = shutil.which(runtime)
        if path:
            return runtime, path
    return None, None


def _cookies_configured():
    opts = {}
    _apply_cookie_options(opts)
    return bool(opts)


def _apply_cookie_options(opts):
    """Aplica cookies desde variables de entorno si están configuradas."""
    cookies_file = os.environ.get("YTDLP_COOKIES_FILE")
    cookies_browser = os.environ.get("YTDLP_COOKIES_BROWSER")

    if cookies_file and os.path.isfile(cookies_file):
        opts["cookiefile"] = cookies_file
    elif cookies_browser:
        opts["cookiesfrombrowser"] = (cookies_browser.strip(),)


class _ConsoleLogger:
    """
    Logger de yt-dlp sin ruido: los errores se muestran en la ventana (en español), así que
    no se repiten en la consola. Solo se dejan las advertencias.
    """

    def debug(self, message):
        pass

    def warning(self, message):
        print(f"Advertencia: {message}")

    def error(self, message):
        pass


COOKIE_ERROR = re.compile(r"cookie|secretstorage|keyring|dpapi|decrypt", re.IGNORECASE)
BOT_CHECK_ERROR = re.compile(r"sign in to confirm|not a bot", re.IGNORECASE)


def run_with_cookie_fallback(operation):
    """
    Ejecuta operation(use_cookies). Si las cookies del navegador no se pueden leer
    (por ejemplo Chrome abierto en Windows), reintenta sin cookies.
    """
    try:
        return operation(True)
    except Exception as error:
        message = str(error)
        # La verificación anti-bot también nombra las cookies, pero reintentar sin ellas no la arregla.
        if not (
            _cookies_configured()
            and COOKIE_ERROR.search(message)
            and not BOT_CHECK_ERROR.search(message)
        ):
            raise
        print("No se pudieron leer las cookies del navegador. Continuando sin cookies.")
        return operation(False)


def get_base_ydl_opts(use_cookies=True):
    """
    Devuelve opciones base compatibles con YouTube en 2025+.
    Incluye reintentos y runtime JS. Los clientes de YouTube se dejan en el valor por
    defecto de yt-dlp: forzar "android" dejaba solo 1 formato disponible.
    """
    opts = {
        "noplaylist": True,
        "retries": 10,
        "fragment_retries": 10,
        "ignoreerrors": False,
        "logger": _ConsoleLogger(),
    }

    runtime, path = _find_js_runtime()
    if runtime and path:
        # yt-dlp espera {runtime: {config}}; "path" es la ruta al ejecutable.
        opts["js_runtimes"] = {runtime: {"path": path}}

    if use_cookies:
        _apply_cookie_options(opts)
    return opts
