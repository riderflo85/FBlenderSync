from pathlib import Path


PROJECT_ROOT_DIR = Path(__file__).resolve().parents[1]

CONFIG_FILE = ''.join([str(PROJECT_ROOT_DIR), '/', 'env.json'])

#TODO Penser à utiliser la valeur de l'input du champs dans la config du module dans Blender
LOCAL_STORAGE_FOLDER = ''
