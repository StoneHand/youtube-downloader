import os

def get_download_folder(subfolder=""):
    """
    Obtiene la carpeta de descargas del usuario y opcionalmente agrega un subdirectorio.
    :param subfolder: Subcarpeta dentro de Downloads (por ejemplo, "audio" o "video").
    :return: Ruta completa de la carpeta.
    """
    downloads_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    if subfolder:
        folder_path = os.path.join(downloads_path, subfolder)
        os.makedirs(folder_path, exist_ok=True)  # Crear la carpeta si no existe
        return folder_path
    return downloads_path
