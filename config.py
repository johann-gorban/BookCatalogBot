import pathlib

BASE_DIR = pathlib.Path().cwd()
STORAGE_PATH = BASE_DIR / 'data'
DB_PATH = STORAGE_PATH / 'db' / 'data.db'
FILE_PATH = STORAGE_PATH / 'images'