from datetime import datetime
from datetime import timezone
import configparser
import sqlite3
import zipfile
import os

import folder_tools as ft
import db_tools as db
import backupted_tools as bct
import folders_sync as fsync

## Config
conf = configparser.ConfigParser()
conf.read("./config/config.conf")

## Variables
backup_sources = bct.GetAvaibleSyncSourceFolders( bct.GetSourcePairs() )
temp_zip_dir = bct.GetTempSaveFolder()
backup_dest = str(conf['Backup']['dest']).replace("'", '').split(';')

## Sqlite3
conn = db.CreateDB('initdb.sql')


def CreateBackups():
    zip_files = []
    ft.MakeDirs(temp_zip_dir)

    for key in backup_sources.keys():
        copy_source = backup_sources[key]
        
        if bct.NeedBackup( db.GetLastBackupTime(conn, copy_source) ):
            print(f'Start backup: [{copy_source}]')
            timestamp = bct.GetUnixTimestamp()
            file_time = str(datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y_%H-%M-%S'))
            zip_filename = f'{key}_{file_time}.bted'
            zip_temp_path = os.path.join(temp_zip_dir, zip_filename)
            bct.zipdir(copy_source, zip_temp_path, b'12345')
            db.InsertNewBackupInfo(conn, timestamp, copy_source, zip_filename)
            zip_files.append(zip_temp_path)

    for dest in backup_dest:
        if dest == 'local':            
            dest_folders = bct.GetLocalDestinationFolders()
            for dest_f in dest_folders:
                ft.CopyFiles(zip_files, dest_f)
                
        if dest == 'GDrive':
            pass


def ClearTempDir():
    if bct.BackupToLocalExists():
        return

    files = os.listdir(temp_zip_dir)
    for item in files:
        if item.endswith('.zip'):
            os.remove(os.path.join(temp_zip_dir, item))


if __name__ == '__main__':
    print('BackupTED Started!')
    CreateBackups()
    ClearTempDir()
    fsync.SartSyncFolders()
