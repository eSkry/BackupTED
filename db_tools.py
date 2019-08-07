from datetime import datetime
import configparser
import sqlite3
import os

import folder_tools as ft

config = configparser.ConfigParser()
config.read('./config/config.conf')

DB_NAME = str(config['Database']['name'])

# Возвращает соединение с базой данных
def CreateDB(sql_file: str):
    if (ft.IsFileExists(DB_NAME)):
        return sqlite3.connect(DB_NAME)

    conn = sqlite3.connect(DB_NAME)

    if ft.IsFileExists(sql_file):
        sql = ft.ReadAllFile(sql_file)
        conn.executescript(sql)

    return conn


def GetLastBackupTime(conn: sqlite3.Connection, _source):
    cur = conn.cursor()
    result = cur.execute('SELECT *, max(date) FROM sync WHERE source=\'{}\';'.format(_source))

    if result.rowcount == -1:
        return datetime.utcfromtimestamp(0)

    return datetime.utcfromtimestamp( result.fetchone()[1] )


def InsertNewBackupInfo(conn: sqlite3.Connection, _date, _source, _zip_name):
    cur = conn.cursor()
    cur.execute('INSERT INTO sync (date, source, zip_name) VALUES ({}, {}, {})'.format(_date, _source, _zip_name))
