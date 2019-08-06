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



if __name__ == '__main__':
    print('BackupTED Started!')