import json

from datetime import datetime
from datetime import timedelta


def next_expire_time(expires_in: int) -> datetime:
    """Calculate the next expire time to dropbox API token.

    Args:
        expires_in (int): token duration validation

    Returns:
        datetime.datetime: end validation
    """
    start = datetime.now()
    delta = timedelta(seconds=expires_in)
    return start + delta


def token_is_expired(expire_at: timedelta) -> bool:
    """Check if the access token is expired or not.

    Args:
        expire_at (timedelta): the end of access token validation

    Returns:
        bool: result of check
    """
    return datetime.now() < expire_at


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
