from shutil import copyfile
import shutil
import os
import re

# Return true if file have read acces
def IsFolderAvailable(folder):
    return os.access(folder, os.R_OK)

# Return true if file exists
def IsFileExists(file):
    return os.path.exists(file) and os.path.isfile(file)

# Return true if folder exists
def IsFolderExists(folder):
    return os.path.exists(folder) and os.path.isdir(folder)

# Reading file to string and return his
def ReadAllFile(file: str):
    if IsFileExists(file):
        f = open(file, 'r')
        data = f.read()
        f.close()
        return data
    else:
        return ''

def MakeDirs(path):
    if IsFolderAvailable(path):
        return
    os.makedirs(path)

def CopyFile(source, destination):
    if not IsFolderExists(destination):
        os.makedirs(destination)
    
    shutil.copy2(source, destination)


def CopyFiles(sources, destination):
    for source in sources:
        CopyFile(source, destination)

def GetBackupsList(backup_folder):
    files = os.listdir(backup_folder)
    backups = []
    for f in files:
        if f.endswith('bted'):
            backups.append(f)

    return backups
            