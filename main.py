import os

from helpers import load_json_config
from helpers import next_expire_time
from helpers import write_file
from helpers import write_json_config
from server import DropboxAPI
from settings import CONFIG_FILE


if __name__ == '__main__':
    config = load_json_config(CONFIG_FILE)
    local_storage_folder = config.get('LOCAL_STORAGE_FOLDER', '')

    if not os.path.isdir(local_storage_folder):
        #TODO Renvoyer l'erreur dans l'interface de blender !!!
        print('FILE LOCAL STORAGE DOES NOT EXIST !!!')
        exit()

    drb = DropboxAPI(config['APP_KEY'], config['APP_SECRET'])

    if not config['ACCESS_TOKEN']:
        token_obj = drb.get_access_token()
        end_validation = next_expire_time(token_obj['expires_in'])
        to_add_config = {
            'ACCESS_TOKEN': token_obj['access_token'],
            'REFRESH_TOKEN': token_obj['refresh_token'],
            'TOKEN_END_VALIDATION': end_validation
        }
        write_json_config(CONFIG_FILE, config, to_add_config)
        os.environ['ACCESS_TOKEN'] = token_obj['access_token']
    else:
        os.environ['ACCESS_TOKEN'] = config['ACCESS_TOKEN']


    print('\nQue veux-tu faire ?')
    print('\t1) Consulter tes dossiers sur ton cloud.')
    print('\t2) Télécharger un fichier de ton cloud.')
    print('\t0) Arreter le programme.')
    close = False

    while not close:
        token = os.environ.get('ACCESS_TOKEN')
        user_choice = input('>> ')

        if user_choice == '1':
            print('\tIndique le chemin du dossier que tu veux consulter ! (Pour consulter la racine, tu peux valider sans rien écrire)')
            folder_path = input('>>> ')

            files_drb = drb.get_content_folder(token, folder_path)
            struct_folder = [
                {'name': f['name'], 'type': f['.tag'], 'path': f['path_lower']}
                for f in files_drb
            ]

            print('\tDropbox files : ')
            for index, folder in enumerate(struct_folder):
                print('\t ', index, '. ', folder)

        elif user_choice == '2':
            print('\tIndique le chemin complet du fichier que tu veux télécharger !')
            folder_file_path = input('>>> ')
            
            file_infos, file_bytes = drb.download_file(token, folder_file_path)
            file_name = f'{local_storage_folder}/{file_infos.get("name")}'
            write_file(file_name, file_bytes)

        elif user_choice in ('exit', '0'):
            close = True
        else:
            print('Tu as fais un mauvais choix, recommence !')
