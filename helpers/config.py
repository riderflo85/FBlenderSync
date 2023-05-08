import json

from datetime import datetime


def load_json_config(json_file_path: str) -> dict:
    """Read the json file config.

    Args:
        json_file_path (str): json file object.

    Returns:
        dict: Dict to contain the json file data.
    """
    data = {}
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    return data


def write_json_config(json_file_path: str, original_data: dict, new_data: dict):
    """Write data in json file config.

    Args:
        json_file_path (str): json file object
        original_data (dict): json file data in already present
        new_data (dict): data to write in json file
    """
    serialize_data = {}
    for k, v in new_data.items():
        if isinstance(v, datetime):
            serialize_data[k] = v.isoformat()
        else:
            serialize_data[k] = v

    original_data.update(serialize_data)
    with open(json_file_path, 'w') as json_file:
        json.dump(original_data, json_file, indent=4, sort_keys=True)
