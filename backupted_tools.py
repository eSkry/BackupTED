from datetime import datetime
from datetime import timezone
import os

import folder_tools as ft

# Возвращает unix timestamp -> float
def GetUnixTimestamp():
    return datetime.now().timestamp()

# Создает папки если они не существуют
def MakeDestinationFolders(config_destination):
    for folder in config_destination:
        if not ft.IsFolderAvailable(folder):
            os.makedirs(folder)

    