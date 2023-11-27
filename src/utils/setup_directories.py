from os import makedirs
from os.path import exists

from ..config import DATA_PATH, CACHE_PATH, MODELS_PATH, EVALUATION_DATA

def setup_directories():
    paths = [DATA_PATH, CACHE_PATH, MODELS_PATH, EVALUATION_DATA]
    for path in paths:
        if not exists(path):
            makedirs(path)
            print(f"Created directory: {path}")
        else:
            print(f"Directory already exists: {path}")