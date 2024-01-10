import os
from pathlib import Path


# Проверка на пустоту каталога
def empty_or_not(path):
    return next(os.scandir(path), None)


# Проверка запрашиваемого пути
def check_path(path):
    if os.path.exists(path):
        return True
    else:
        return False
