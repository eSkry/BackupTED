from datetime import datetime
from datetime import timezone
import configparser
import sqlite3
import os

import folder_tools as ft
import db_tools as db

## Config
conf = configparser.ConfigParser()
conf.read("./config/config.conf")

## Variables
backup_sources = str(conf['Folders']['source']).replace("'", '').split(';')
sources_count = len(backup_sources)

backup_destination = str(conf['Folders']['dest']).replace("'", '').split(';')
destination_count = len(backup_destination)

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
        updtime = db.GetLastBackupTime(conn, source)
        
        if NeedBackup(updtime):
            print('Start backup: [{}]'.format(source))
            timestamp = datetime.replace(tzinfo=timezone.utc).timestamp()
            print(timestamp)
            db.InsertNewBackupInfo(conn, timestamp, source, 'afa.zip')

