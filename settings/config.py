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
