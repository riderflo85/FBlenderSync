from pathlib import Path
from enum import Enum

from ..i18n import get_label as gt_


PROJECT_ROOT_DIR = Path(__file__).resolve().parents[1]

CONFIG_FILE = ''.join([str(PROJECT_ROOT_DIR), '/', 'env.json'])

DROPBOX_OAUTH_URL = 'https://www.dropbox.com/oauth2/authorize'

DROPBOX_API_URL = 'https://api.dropboxapi.com'

DROPBOX_CONTENT_URL = 'https://content.dropboxapi.com'


class FileMoreRecentIn(Enum):
    DRB = {
        "value": "dropbox",
        "description": gt_("FMRI-DRB-desc"),
        "icon": "KEYTYPE_BREAKDOWN_VEC",
    }
    LOCAL = {
        "value": "local",
        "description": gt_("FMRI-Local-desc"),
        "icon": "KEYTYPE_JITTER_VEC",
    }
    MISSING_LOCAL = {
        "value": "missing_local",
        "description": gt_("FMRI-MissingLocal-desc"),
        "icon": "KEYTYPE_MOVING_HOLD_VEC",
    }

    @classmethod
    def values(cls):
        return [e.value for e in cls]


class DownloadMode(Enum):
    STORE = {
        "name": gt_("DM-Store-name"),
        "desc": gt_("DM-Store-desc"),
    }
    STORE_OPEN = {
        "name": gt_("DM-StoreOpen-name"),
        "desc": gt_("DM-StoreOpen-desc"),
    }

    @classmethod
    def items_enum_prop(cls):
        return (
            (
                DownloadMode.STORE.name,
                DownloadMode.STORE.value.get("name"),
                DownloadMode.STORE.value.get("desc"),
            ),
            (
                DownloadMode.STORE_OPEN.name,
                DownloadMode.STORE_OPEN.value.get("name"),
                DownloadMode.STORE_OPEN.value.get("desc"),
            ),
        )

    @classmethod
    def get_desc(cls, enum_name: str):
        enum_item = getattr(cls, enum_name)
        return enum_item.value.get("desc")
