from datetime import datetime
from datetime import timezone
import configparser
import zipfile
import os

import folder_tools as ft

## Config
conf = configparser.ConfigParser()
conf.read("./config/config.conf")


# Возвращает unix timestamp -> float
def GetUnixTimestamp():
    return datetime.now().timestamp()


# Принимает на вход пассив папок для синхронизации.
# возсращает список доступных папок из переданного массива
def GetAvaibleSyncSourceFolders(config_sources):
    avaible_folders = []
    for folder in config_sources:
        if ft.IsFolderAvailable(folder):
            avaible_folders.append(folder)

    return avaible_folders


# Создает папки если они не существуют
def MakeDestinationFolders(config_destination):
    for folder in config_destination:
        if not ft.IsFolderAvailable(folder):
            os.makedirs(folder)


def zipdir(path, zip_name, password):
    ziph = zipfile.ZipFile(zip_name, 'w')
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
    
    ziph.setpassword(password)

def NeedBackup(date):
    days = int(str(conf['Backup']['each'])[:-1])
    dist = datetime.fromtimestamp(GetUnixTimestamp()) - datetime.fromtimestamp(date)

    if dist.days >= days:
        return True
        
    return False


def BackupToLocalExists():
    dests = str(conf['Backup']['dest']).replace("'", '').split(';')
    for dest in dests:
        if dest == 'local':
            return True
    
    return False

def GetTempSaveFolder():
    if BackupToLocalExists():
        return str(conf['local']['path']).replace("'", '')

    return str(conf['Backup']['temp_dir']).replace("'", '')