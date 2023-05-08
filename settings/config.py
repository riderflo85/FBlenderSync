from pathlib import Path


PROJECT_ROOT_DIR = Path(__file__).resolve().parents[1]

CONFIG_FILE = ''.join([str(PROJECT_ROOT_DIR), '/', 'env.json'])
