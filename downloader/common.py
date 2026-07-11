"""Opciones compartidas de yt-dlp para descargas actuales de YouTube."""

import os
import shutil


def _find_js_runtime():
    """Busca un runtime JavaScript compatible con yt-dlp (Deno o Node)."""
    for runtime in ("deno", "node"):
        path = shutil.which(runtime)
        if path:
            return runtime, path
    return None, None


def _apply_cookie_options(opts):
    """Aplica cookies desde variables de entorno si están configuradas."""
    cookies_file = os.environ.get("YTDLP_COOKIES_FILE")
    cookies_browser = os.environ.get("YTDLP_COOKIES_BROWSER")

    if cookies_file and os.path.isfile(cookies_file):
        opts["cookiefile"] = cookies_file
    elif cookies_browser:
        opts["cookiesfrombrowser"] = (cookies_browser.strip(),)


def get_base_ydl_opts():
    """
    Devuelve opciones base compatibles con YouTube en 2025+.
    Incluye reintentos, runtime JS y clientes alternativos.
    """
    opts = {
        "noplaylist": True,
        "retries": 10,
        "fragment_retries": 10,
        "ignoreerrors": False,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"],
            }
        },
    }

    runtime, path = _find_js_runtime()
    if runtime:
        opts["js_runtimes"] = {runtime: path} if path else [runtime]

    _apply_cookie_options(opts)
    return opts
