import configparser
import sqlite3
import os

import folder_tools as ft

config = configparser.ConfigParser()
config.read('./config/config.conf')

DB_NAME = str(config['Database']['name'])

# Возвращает соединение с базой данных
def CreateDB(sql_file):
    if ft.IsFileExists(sql_file):
        sql = ft.ReadAllFile(sql_file)

    conn = sqlite3.connect(DB_NAME)
    return conn