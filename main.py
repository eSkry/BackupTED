from datetime import datetime
from datetime import timezone
import configparser
import sqlite3
import zipfile
import os

import folder_tools as ft
import db_tools as db
import backupted_tools as bct

## Config
conf = configparser.ConfigParser()
conf.read("./config/config.conf")

## Variables
backup_sources = bct.GetAvaibleSyncSourceFolders(str(conf['Backup']['source']).replace("'", '').split(';'))
temp_zip_dir = str(conf['Backup']['temp_dir']).replace("'", '')
backup_dest = str(conf['Backup']['dest']).replace("'", '').split(';')

## Sqlite3
conn = db.CreateDB('initdb.sql')


def CreateBackups():
    zip_files = []

    for source in backup_sources:
        if bct.NeedBackup( db.GetLastBackupTime(conn, source) ):
            print('Start backup: [{}]'.format(source))
            timestamp = bct.GetUnixTimestamp()
            file_time = str(datetime.utcfromtimestamp(timestamp).strftime('%d_%m_%Y_%H_%M_%S'))
            zip_filename = '{}.zip'.format(file_time)
            zip_temp_path = os.path.join(temp_zip_dir, zip_filename)

            bct.zipdir(source, zip_temp_path, b'12345')
            db.InsertNewBackupInfo(conn, timestamp, source, zip_filename)
            zip_files.append(zip_temp_path)

    for dest in backup_dest:
        if dest == 'local':
            dest_path = os.path.join(temp_zip_dir, str(conf['local']['path']).replace("'", ''))
            ft.CopyFiles(zip_files, dest_path)


def ClearTempDir():
    files = os.listdir(temp_zip_dir)
    for item in files:
        if item.endswith('.zip'):
            os.remove(os.path.join(temp_zip_dir, item))


if __name__ == '__main__':
    print('BackupTED Started!')
    CreateBackups()
    ClearTempDir()

