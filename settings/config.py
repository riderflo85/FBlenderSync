from pathlib import Path


PROJECT_ROOT_DIR = Path(__file__).resolve().parents[1]

CONFIG_FILE = ''.join([str(PROJECT_ROOT_DIR), '/', 'env.json'])

DROPBOX_OAUTH_URL = 'https://www.dropbox.com/oauth2/authorize'

DROPBOX_API_URL = 'https://api.dropboxapi.com'

DROPBOX_CONTENT_URL = 'https://content.dropboxapi.com'
