from datetime import datetime
from datetime import timezone
import configparser
import sqlite3
import zipfile
import time
import os

import folder_tools as ft
import db_tools as db
import backupted_tools as bct

## Config
conf = configparser.ConfigParser()
conf.read("./config/config.conf")

## Variables
backup_sources = bct.GetAvaibleSyncSourceFolders(str(conf['Folders']['source']).replace("'", '').split(';'))
backup_destination = bct.GetAvaibleSyncSourceFolders(str(conf['Folders']['dest']).replace("'", '').split(';'))
temp_zip_dir = str(conf['Backup']['temp_dir']).replace("'", '')

## Sqlite3
conn = db.CreateDB('initdb.sql')


def NeedBackup(date):
    days = int(str(conf['Backup']['each'])[:-1])
    dist = date - datetime.now()

    if dist.days >= days:
        return True
        
    return False


if __name__ == '__main__':
    print('BackupTED Started!')

    for source in backup_sources:
        if NeedBackup( db.GetLastBackupTime(conn, source) ):
            print('Start backup: [{}]'.format(source))
            timestamp = int(time.time())
            file_time = str(datetime.utcfromtimestamp(timestamp).strftime('%d_%m_%Y_%H_%M_%S'))
            zip_filename = '{}.zip'.format(file_time)
            zip_temp_path = temp_zip_dir + '/' + zip_filename

            bct.zipdir(source, zip_temp_path, b'12345')
            db.InsertNewBackupInfo(conn, timestamp, source, zip_filename)

