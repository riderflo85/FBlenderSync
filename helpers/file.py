def write_file(path_file: str, bytes_content: bytes):
    """Write the file with bytes content in the disk.

    Args:
        path_file (str): File destination locate
        bytes_content (bytes): File content
    """
    with open(path_file, 'wb') as file_obj:
        file_obj.write(bytes_content)