import webbrowser
import requests

from settings import HOST
from settings import PORT
from server import create_socket
from server import wait_authorization_code



class DropboxAPI:
    DRB_OAUTH_URL = 'https://www.dropbox.com/oauth2/authorize'
    DRB_API = 'https://api.dropboxapi.com'
    
    def __init__(self, app_key: str, app_secret: str) -> None:
        self.app_key = app_key
        self.app_secret = app_secret
        self.oauth_code = ''
        self.access_token: str

    def _authorization_app(self):
        """
        Open the web browser with authoriation web page to allow FBlenderSync connect to your account.
        """
        redirect = f"http://{HOST}:{str(PORT)}"
        url_auth_app = f"{self.DRB_OAUTH_URL}?client_id={self.app_key}&response_type=code&redirect_uri={redirect}"
        webbrowser.open(url_auth_app)
        
        sock_serv = create_socket(HOST, PORT)
        nb_request = 0
        while self.oauth_code == '' or nb_request < 1:
            code = wait_authorization_code(sock_serv)
            if code and len(code) == 1:
                self.oauth_code = code[0]
            else:
                nb_request += 1
