import json

from datetime import datetime
from datetime import timedelta


ACCESS_TOKEN = {
    'token': str,
    'expire_at': datetime
}
REFRESH_TOKEN: str


def next_expire_time(expires_in: int) -> datetime.datetime:
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