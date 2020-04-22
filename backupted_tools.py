from datetime import datetime
from datetime import timezone
import configparser
import zipfile
import os

import folder_tools as ft

## Config
conf = configparser.ConfigParser()
conf.read("./config/config.conf")

ignore_types = str(conf['ignore']['types']).split(';')
ignore_size_file = int(conf['ignore']['size']) * 1024 * 1024

# Возвращает unix timestamp -> float
def GetUnixTimestamp():
    return datetime.now().timestamp()


# Принимает на вход словарь лейблов и папок для синхронизации.
# возвращает список доступных папок из переданного массива
def GetAvaibleSyncSourceFolders(config_sources):
    avaible_folders = {}

    for lable in config_sources.keys():
        if ft.IsFolderAvailable( config_sources[lable] ):
            avaible_folders[lable] = config_sources[lable]

    return avaible_folders


# Создает папки если они не существуют
def MakeDestinationFolders(config_destination):
    for folder in config_destination:
        if not ft.IsFolderAvailable(folder):
            os.makedirs(folder)


def zipdir(path, zip_name, password):
    ziph = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            if IsFileIgnore(file):
                continue
            
            filePath = os.path.join(root, file)

            if os.path.getsize(filePath) >= ignore_size_file:
                continue

            ziph.write(filePath)
    
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
        return str(conf['local']['path']).replace("'", '').split(';')[0]

    return str(conf['Backup']['temp_dir']).replace("'", '')


def GetSourcePairs():
    sources = str(conf['Backup']['source']).replace("'", '').split(';')
    pairs = {}

    for val in sources:
        temp = val.split('@')
        pairs[temp[0]] = temp[1]

    return pairs

def GetLocalDestinationFolders():
    return str(conf['local']['path']).replace("'", '').split(';')

def GetIgnoreFileTypes():
    return str(conf['ignore']['types']).split(';')

def IsFileIgnore(fileName):
    for fileType in ignore_types:
        if fileName.endswith(fileType):
            return True
    
    if fileName.startswith('~'): # Игнорировать файлы блокировки (Windows)
        return True

    return False

def GetCleanDays():
    mark = str(conf['Clean']['older'])

    if mark[-1] == 'd':
        return int(mark[:-1])
    if mark[-1] == 'w':
        return int(mark[:-1]) * 7
    if mark[-1] == 'm':
        return int(mark[:-1]) * 28
    
    return 0
    