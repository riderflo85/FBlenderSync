import webbrowser
import requests
import os
import json

from typing import Literal

from ..helpers import load_json_config
from ..helpers import next_expire_time
from ..helpers import write_json_config
from ..settings import CONFIG_FILE
from ..settings import DROPBOX_API_URL as DRB_API
from ..settings import DROPBOX_CONTENT_URL as DRB_CONTENT
from ..settings import DROPBOX_OAUTH_URL as DRB_OAUTH
from ..settings import HOST
from ..settings import PORT
from ..settings import REDIRECT_WEB_URI as REDIRECT_URI
from .web import create_socket
from .web import wait_authorization_code


class DropboxError(Exception):
    """Custom exception class to DropBox API"""
    
    def __init__(self, err: str, *args: object) -> None:
        super().__init__(*args)
        self.err = err

    def __str__(self) -> str:
        return f'The DropBox API return this error :\n\t{self.err}'


class DropboxAPI:

    def __init__(self, app_key: str, app_secret: str, in_blender: bool=False, **kwargs) -> None:
        self.app_key = app_key
        self.app_secret = app_secret
        self.oauth_code = ''
        self.in_blender = in_blender
        self.fbl_profile_klass = kwargs.get('fbl_profile_klass', False)
        self.bl_preferences = kwargs.get('bl_preferences', False)

    def _authorization_app(self):
        """
        Open the web browser with authoriation web page to allow FBlenderSync connect to your account.
        """
        url_auth_app = f'{DRB_OAUTH}?client_id={self.app_key}&token_access_type=offline&response_type=code&redirect_uri={REDIRECT_URI}'

        response_oauth = requests.get(url_auth_app)
        if response_oauth.status_code != 200:
            raise DropboxError(f'Invalid client_id : {self.app_key}')

        webbrowser.open(url_auth_app)

        sock_serv = create_socket(HOST, PORT)
        nb_request = 0
        while self.oauth_code == '' or nb_request < 1:
            code = wait_authorization_code(sock_serv)
            if code and len(code) == 1:
                self.oauth_code = code[0]
            else:
                nb_request += 1

    @staticmethod
    def _make_headers(token: str, **kwargs) -> dict:
        """Create the headers requests.
        Add access token.

        Args:
            token (str): User Access Token

        Returns:
            dict: headers for request
        """
        kw_copy = kwargs.copy()
        for k in kwargs.keys():
            if '_' in k:
                kw_copy[k.replace('_', '-')] = kw_copy.pop(k)

        headers = {
            'Authorization': f'Bearer {token}',
            **kw_copy
        }
        return headers

    def _is_expired_token(self, response: requests.Response) -> dict:
        """Check if the DropBox response return a expired access token error.
        If raise this error when get new access token with refresh token and
        execute the callback function.

        Args:
            response (requests.Response): DropBox API response object with status code and body.

        Returns:
            dict: return fallback boolean with new token or with error message
        """
        if response.status_code == 401:
            error = response.json()
            error_accepted = ('expired_access_token', 'invalid_access_token')
            if error['error']['.tag'] in error_accepted:
                new_token = self.refresh_api_token()
                return {'fallback': True, 'new_token': new_token}
            else:
                return {'fallback': False, 'error': str(error)}
        elif response.status_code != 200:
            return  {'fallback': False, 'error': response.text}
        else:
            return {'fallback': False}

    def get_access_token(self):
        """Get dropbox access token"""
        if not self.oauth_code:
            self._authorization_app()

        url = f'{DRB_API}/oauth2/token'
        payload = {
            'code': self.oauth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI, # Not used to redirect again
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

        if res.status_code == 200:
            data = res.json()
            r_fields = ['access_token', 'refresh_token', 'expires_in']
            return {
                k: v for k, v in data.items() if k in r_fields
            }
        else:
            #TODO Renvoyer l'erreur dans l'interface de blender !!!
            raise DropboxError(res.text)

    def refresh_api_token(self):
        """Refresh the access token"""
        url = f'{DRB_API}/oauth2/token'
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.bl_preferences.refresh_token if self.in_blender else load_json_config(CONFIG_FILE)['REFRESH_TOKEN'],
            'client_id': self.app_key,
            'client_secret': self.app_secret
        }
        res = requests.post(url, data=payload)

        if res.status_code == 200:
            data = res.json()
            end_validation = next_expire_time(data['expires_in'])
            to_update_config = {
                'ACCESS_TOKEN': data['access_token'],
                'TOKEN_END_VALIDATION': end_validation
            }
            expire_token = end_validation.isoformat()
            if self.in_blender:
                self.fbl_profile_klass.ACCES_TOKEN = data['access_token']
                self.fbl_profile_klass.EXPIRE_TOKEN = expire_token
                self.fbl_profile_klass.save_profiles_data()
                self.bl_preferences.token = data['access_token']
                self.bl_preferences.expire_token = expire_token
            else:
                config = load_json_config(CONFIG_FILE)
                os.environ['ACCESS_TOKEN'] = data['access_token']
                os.environ['TOKEN_END_VALIDATION'] = expire_token
                write_json_config(CONFIG_FILE, config, to_update_config)
            return data['access_token']
        else:
            #TODO Renvoyer l'erreur dans l'interface de blender !!!
            raise DropboxAPI(res.text)

    def get_content_folder(self, token: str, path: str) -> list:
        """Get the Dropbox content folder.
        To use this method to navigate in the Dropbox managed folders.

        Args:
            token (str): User Access Token
            path (str): Dropbox folder path

        Returns:
            list: List object with folder name, folder content, folder type, folder id and folder path.
        """
        url = f'{DRB_API}/2/files/list_folder'
        payload = {
            'path': path, 
            'recursive': False, 
            'include_media_info': False, 
            'include_deleted': False, 
            'include_has_explicit_shared_members': False, 
            'include_mounted_folders': True, 
            'include_non_downloadable_files': False
        }
        h = self._make_headers(token)
        res = requests.post(url, json=payload, headers=h)
        # data for good response is :
        # {
        #     "entries": [
        #         {
        #             ".tag": "folder",
        #             "name": "test-sync",
        #             "path_lower": "/projets-blender/test-sync",
        #             "path_display": "/Projets-Blender/test-sync",
        #             "id": "id:3BmObzd4dHcAA"
        #         }
        #     ],
        #     "cursor": "WCOi340_Ghw3B5VCW5-MKZNs6LhaJ2vUDwj_ha_g",
        #     "has_more": false
        # }
        result = self._is_expired_token(res)
        if not result.get('error') and not result['fallback']:
            res_data = res.json()
            #TODO Voir pour gérer la pagination avec les valeurs `has_more` et `cursor`
            return res_data['entries']
        elif not result.get('error') and result['fallback']:
            return self.get_content_folder(result['new_token'], path)
        else:
            #TODO Renvoyer l'erreur dans l'interface de blender !!!
            raise DropboxError(result['error'])

    def download_file(self, token: str, path: str):
        """Download DropBox file.

        Args:
            token (str): User Access Token
            path (str): Dropbox folder path with filename

        Returns:
            tuple: Dict file informations and file bytes content
        """
        url = f'{DRB_CONTENT}/2/files/download'
        h = self._make_headers(token, Dropbox_API_Arg=f'{{"path": "{path}"}}')
        res = requests.get(url, headers=h)

        result = self._is_expired_token(res)
        if not result.get('error') and not result['fallback']:
            return json.loads(res.headers.get('Dropbox-Api-Result')), res.content
        elif not result.get('error') and result['fallback']:
            return self.download_file(result['new_token'], path)
        else:
            #TODO Renvoyer l'erreur dans l'interface de blender !!!
            raise DropboxError(result['error'])

    def upload_file(
        self,
        token: str,
        path_file: str,
        dropbox_path_folder: str,
        mode: Literal['add', 'overwrite']
    ) -> str:
        """Upload the file on DropBox folder sync.

        Args:
            token (str): User Access Token
            path_file (str): Local path file with file name and extension
            dropbox_path_folder (str): The folder path to Dropbox account
            mode (Literal['add', 'overwrite']): The write file Dropbox mode.
                See https://www.dropbox.com/developers/documentation/http/documentation#files-upload

        Returns:
            str: Finish state operation
        """
        url = f'{DRB_CONTENT}/2/files/upload'
        data = {
            'autorename': False,
            'mute': False,
            'strict_conflict': False,
            'mode': mode,
            'path': f'{dropbox_path_folder}/{path_file.split("/")[-1]}'
        }
        h = self._make_headers(
            token,
            Dropbox_API_Arg=json.dumps(data),
            Content_Type='application/octet-stream'
        )
        file_req = open(path_file, 'rb')
        res = requests.post(url, headers=h, data=file_req)
        file_req.close()

        result = self._is_expired_token(res)
        if not result.get('error') and not result['fallback']:
            return 'done'
        elif not result.get('error') and result['fallback']:
            return self.upload_file(result['new_token'], path_file, dropbox_path_folder, mode)
        else:
            #TODO Renvoyer l'erreur dans l'interface de blender !!!
            raise DropboxError(result['error'])

    def create_folder(self, token: str, path: str) -> dict:
        """Create the new folder with path.

        Args:
            token (str): User Access Token
            path (str): DropBox path for new folder
            
        Returns:
            dict: DropBox response with new folder metadata.
        """
        url = f'{DRB_API}/2/files/create_folder_v2'
        h = self._make_headers(token)
        data = {
            "autorename": True,
            "path": path,
        }
        res = requests.post(url, headers=h, json=data)
        result = self._is_expired_token(res)
        if not result.get('error') and not result['fallback']:
            res_data = res.json()
            return res_data["metadata"]
        elif not result.get('error') and result['fallback']:
            return self.create_folder(result['new_token'], path)
        else:
            raise DropboxError(result['error'])

    def get_storage_infos(self, token: str) -> tuple:
        """Get the DropBox storage space usage infos.

        Args:
            token (str): User Access Token
            
        Returns:
            tuple: allocated and used.
        """
        url = f'{DRB_API}/2/users/get_space_usage'
        h = self._make_headers(token)
        res = requests.post(url, headers=h)
        result = self._is_expired_token(res)
        if not result.get('error') and not result['fallback']:
            res_data = res.json()
            bytes_allocated = res_data['allocation']['allocated']
            bytes_used = res_data['used']
            return bytes_allocated, bytes_used
        elif not result.get('error') and result['fallback']:
            return self.get_storage_infos(result['new_token'])
        else:
            raise DropboxError(result['error'])

    def delete_file_or_folder(self, token: str, id_target: str) -> str:
        """Delete a file or folder on DropBox with specified DropBox ID.

        Args:
            token (str): User Access Token.
            id_target (str): DropBox ID to delete item.

        Returns:
            str: `done` or error.
        """
        url = f'{DRB_API}/2/files/delete_v2'
        h = self._make_headers(token)
        data = {'path': id_target}
        res = requests.post(url, headers=h, json=data)
        result = self._is_expired_token(res)
        if not result.get('error') and not result['fallback']:
            return 'done'
        elif not result.get('error') and result['fallback']:
            return self.delete_file_or_folder(result['new_token'])
        else:
            raise DropboxError(result['error'])
