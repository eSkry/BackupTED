import configparser
import datetime
import sqlite3
import os

import folder_tools as ft

config = configparser.ConfigParser()
config.read('./config/config.conf')

DB_NAME = str(config['Database']['name'])

# Возвращает соединение с базой данных
def CreateDB(sql_file):
    if (ft.IsFileExists(DB_NAME)):
        return sqlite3.connect(DB_NAME)

    conn = sqlite3.connect(DB_NAME)

    if ft.IsFileExists(sql_file):
        sql = ft.ReadAllFile(sql_file)
        cur = conn.cursor()
        cur.execute(sql)

    return conn


def GetLastBackupTime(conn: sqlite3.Connection):
    cur = conn.cursor()
    result = cur.execute('SELECT *, max(date) FROM sync;')

    if result.rowcount == 0:
        return 0
    
    return result.fetchone()[1]


def InsertNewBackupInfo(conn: sqlite3.Connection, _date, _source, _dest, _zip_name):
    cur = conn.cursor()
    cur.execute('INSERT INTO sync (date, source, dest, zip_name) VALUES ({}, {}, {}, {})'.format(_date, _source, _dest, _zip_name))
