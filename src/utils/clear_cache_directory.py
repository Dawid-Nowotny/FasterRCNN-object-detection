import shutil
import os
from ..config import CACHE_PATH

def clear_cache_directory():
    if os.path.exists(CACHE_PATH):
        try:
            for filename in os.listdir(CACHE_PATH):
                file_path = os.path.join(CACHE_PATH, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            return True
        except Exception as e:
            print(f"Nie udało się opróżnić {CACHE_PATH}. Powód: {e}")
            return False
    else:
        return False