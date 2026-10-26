from urllib.parse import urlparse

YOUTUBE_HOSTS = ("youtube.com", "youtu.be", "youtube-nocookie.com")


def normalize_youtube_url(text):
    """
    Devuelve una URL de YouTube lista para usar, o None si el texto no parece un enlace de YouTube.
    Acepta enlaces sin "https://" (por ejemplo "www.youtube.com/watch?v=...").
    """
    text = (text or "").strip()
    if not text or " " in text:
        return None

    if "://" not in text:
        text = f"https://{text}"

    hostname = (urlparse(text).hostname or "").lower()
    if any(hostname == host or hostname.endswith(f".{host}") for host in YOUTUBE_HOSTS):
        return text
    return None
