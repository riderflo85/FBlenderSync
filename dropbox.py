import webbrowser
import requests

from helpers import ACCESS_TOKEN
from helpers import REFRESH_TOKEN
from settings import HOST
from settings import PORT
from server import create_socket
from server import wait_authorization_code


class DropboxError(Exception):
    """Custom exception class to DropBox API"""
    
    def __init__(self, err: str, *args: object) -> None:
        super().__init__(*args)
        self.err = err

    def __str__(self) -> str:
        return f"The DropBox API return this error :\n\t{self.err}"


class DropboxAPI:
    DRB_OAUTH_URL = 'https://www.dropbox.com/oauth2/authorize'
    DRB_API = 'https://api.dropboxapi.com'
    REDIRECT_URI = f"http://{HOST}:{str(PORT)}"

    def __init__(self, app_key: str, app_secret: str) -> None:
        self.app_key = app_key
        self.app_secret = app_secret
        self.oauth_code = ''

    def _authorization_app(self):
        """
        Open the web browser with authoriation web page to allow FBlenderSync connect to your account.
        """
        url_auth_app = f"{self.DRB_OAUTH_URL}?client_id={self.app_key}&token_access_type=offline&response_type=code&redirect_uri={self.REDIRECT_URI}"
        webbrowser.open(url_auth_app)

        sock_serv = create_socket(HOST, PORT)
        nb_request = 0
        while self.oauth_code == '' or nb_request < 1:
            code = wait_authorization_code(sock_serv)
            if code and len(code) == 1:
                self.oauth_code = code[0]
            else:
                nb_request += 1

    def get_access_token(self):
        """Get dropbox access token"""
        url = f"{self.DRB_API}/oauth2/token"
        payload = {
            'code': self.oauth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.REDIRECT_URI, # Not used to redirect again
            'client_id': self.app_key,
            'client_secret': self.app_secret
        }
        res = requests.post(url, data=payload)
        # data for good response is:
        # {
        # "access_token": "...",
        # "expires_in": 14400,
        # "token_type": "bearer",
        # "scope": "account_info.read files.content.read files.content.write files.metadata.read",
        # "refresh_token": "...",
        # "account_id": "...",
        # "uid": "..."
        # }
        data = res.json()

        if res.status_code != 200:
            #TODO Renvoyer l'erreur dans l'interface de blender !!!
            raise DropboxError(res.text)
        else:
            r_fields = ['access_token', 'refresh_token', 'expires_in']
            return {
                k: v for k, v in data.items() if k in r_fields
            }


    def refresh_api_token(self):
        """Refresh the access token"""
        url = f"{self.DRB_API}/oauth2/token"
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.app_key,
            'client_secret': self.app_secret
        }
