import os
import json
import bpy

from .statics import APP_NAME
from .settings import DownloadMode


class FBlenderProfile:

    APP_KEY = ''
    APP_SECRET = ''
    LOCAL_STORAGE_FOLDER = ''
    ACCESS_TOKEN = ''
    REFRESH_TOKEN = ''
    EXPIRE_TOKEN = ''
    DOWNLOAD_MODE = DownloadMode.STORE.value.get("id")
    profiles_path = ''
    profiles_file = ''
    json_settings = [
        'APP_KEY',
        'APP_SECRET',
        'LOCAL_STORAGE_FOLDER',
        'ACCESS_TOKEN',
        'REFRESH_TOKEN',
        'EXPIRE_TOKEN',
        'DOWNLOAD_MODE',
    ]

    @classmethod
    def reset_profile(cls):
        for setting in cls.json_settings:
            setattr(cls, setting, '')

    @classmethod
    def read_json(cls):
        """Updates the settings from the JSON file."""

        cls.reset_profile()
        config_json = get_profiles_data(cls.profiles_path, cls.profiles_file)
        for key, value in config_json.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
            else:
                print(f'Skipping key {key} from profile JSON')

    @classmethod
    def save_profiles_data(cls):
        """Saves the profiles data to JSON."""
        if cls.profiles_file != '':
            data = {}
            for setting in cls.json_settings:
                data[setting] = getattr(cls, setting)

            with open(cls.profiles_file, 'w', encoding='utf8') as outfile:
                json.dump(data, outfile, sort_keys=True)
        else:
            raise AttributeError('FBlenderProfile has an empty `profiles_file` attribute.')


def make_profiles_path():
    profiles_path = bpy.utils.user_resource('CONFIG', path=APP_NAME, create=True)
    profiles_file = os.path.join(profiles_path, 'profiles.json')
    FBlenderProfile.profiles_file = profiles_file
    FBlenderProfile.profiles_path = profiles_path


def _create_default_config(prof_path, prof_file):
    """Create the default json config file with"""
    default_data = {
        'APP_SECRET': '',
        'APP_KEY': '',
        'LOCAL_STORAGE_FOLDER': '',
        'ACCESS_TOKEN': '',
        'REFRESH_TOKEN': '',
        'EXPIRE_TOKEN': '',
        'DOWNLOAD_MODE': DownloadMode.STORE.value.get("id")
    }

    os.makedirs(prof_path, exist_ok=True)

    # Populate the file, ensuring that its permissions are restrictive enough.
    # `old_umask = os.umask(0o077)`: La fonction `os.umask()` définit le masque d'autorisation actuel et retourne l'ancienne valeur du masque. Ici, le masque est défini sur `0o077`, ce qui signifie que les permissions par défaut pour le fichier seront réglées sur `0o600` (lecture et écriture uniquement pour le propriétaire, sans accès pour les autres).

    # 2. `try: ... finally: ...`: Cette structure `try-finally` garantit que le masque d'autorisation sera rétabli à sa valeur précédente, même en cas d'erreur pendant l'écriture des données dans le fichier.

    # 3. `with open(profiles_file, 'w', encoding='utf8') as outfile: ...`: Ouvre le fichier spécifié dans le mode d'écriture (`'w'`) et avec l'encodage UTF-8 (`'utf8'`). Le fichier est référencé par la variable `outfile` dans ce contexte.

    # 4. `json.dump(profiles_default_data, outfile)`: Utilise la fonction `json.dump()` pour écrire les données JSON contenues dans `profiles_default_data` dans le fichier `outfile`.

    # 5. `os.umask(old_umask)`: Rétablit le masque d'autorisation précédent en utilisant la valeur stockée dans `old_umask`. Cela garantit que les masques d'autorisation par défaut ne sont pas modifiés de façon permanente après avoir écrit les données dans le fichier.
    old_umask = os.umask(0o077)
    try:
        with open(prof_file, 'w', encoding='utf8') as outfile:
            json.dump(default_data, outfile)
    finally:
        os.umask(old_umask)
    return default_data


def get_profiles_data(prof_path, prof_file):
    """Returns the profiles.json content from a fblender_sync folder in the
    Blender config directory. If the file does not exist we create one with the
    basic data structure.
    """

    # if the file does not exist
    if not os.path.exists(prof_file):
        return _create_default_config(prof_path, prof_file)

    # try parsing the file
    with open(prof_file, 'r', encoding='utf8') as jsonfile:
        try:
            file_data = json.load(jsonfile)
            file_data['APP_SECRET']
            file_data['APP_KEY']
            file_data['LOCAL_STORAGE_FOLDER']
            file_data['ACCESS_TOKEN']
            file_data['REFRESH_TOKEN']
            file_data['DOWNLOAD_MODE']
            return file_data
        except (ValueError,  # malformed json data
                KeyError):  # it doesn't have the expected content
            print(
                '(%s) '
                'Warning: profiles.json is either empty or malformed. '
                'The file will be reset.' % APP_NAME
            )
            # overwrite the file
            return _create_default_config(prof_path, prof_file)
