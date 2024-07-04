import os
from datetime import datetime


def write_file(path_file_name: str, bytes_content: bytes):
    """Write the file with bytes content in the disk.

    Args:
        path_file_name (str): File destination locate
        bytes_content (bytes): File content
    """
    with open(path_file_name, 'wb') as file_obj:
        file_obj.write(bytes_content)

    return check_local_path_file(path_file_name)


def check_local_path_file(path_file_name: str) -> bool:
    """Check if local path file is exist or not.

    Args:
        path_file_name (str): local path file
    """
    return os.path.isfile(path_file_name)


def check_or_create_local_root_path(root_path: str) -> bool:
    """Check if local root path is exist or not.
    If root path does not exist this method create it.

    Args:
        root_path (str): _description_
    """
    if not os.path.exists(root_path):
        os.makedirs(root_path)
        return True
    else:
        return True


def get_modified_date_file(path_file: str):
    """Return the modified date of the local file.

    Args:
        path_file (str): local path file
    """
    timestamp = os.path.getmtime(path_file)
    return datetime.fromtimestamp(timestamp)
