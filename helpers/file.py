import os


def write_file(path_file_name: str, bytes_content: bytes):
    """Write the file with bytes content in the disk.

    Args:
        path_file_name (str): File destination locate
        bytes_content (bytes): File content
    """
    with open(path_file_name, 'wb') as file_obj:
        file_obj.write(bytes_content)

    if os.path.isfile(path_file_name):
        #TODO Voir si c'est possible de mettre des messages de succès dans Blender
        print('FILE IS WRITED !!!')
    else:
        #TODO Renvoyer l'erreur dans l'interface de blender !!!
        print('FILE IS NOT WRITED !!!')


def check_local_path_file(path_file_name: str):
    """Check if local path file is exist or not.

    Args:
        path_file_name (str): local path file
    """
    return os.path.isfile(path_file_name)
