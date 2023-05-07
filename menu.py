from dropbox import DropboxAPI
from helpers import load_json_config


if __name__ == '__main__':
    config = load_json_config('env.json')
    print(config)

    drb = DropboxAPI(config['APP_KEY'], config['APP_SECRET'])
    
    drb._authorization_app()    
