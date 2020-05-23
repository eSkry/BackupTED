from datetime import datetime
from datetime import timezone
import sqlite3
import zipfile
import os

import folder_tools as ft
import db_tools as db
import backupted_tools as bct
import folders_sync as fsync
import ted_config_reader as ted_conf

class BackupTED(object):

    def __init__(self):
        self.conf = ted_conf.TEDConfigReader('./config/config.conf')
        self.temp_zip_dir = self.conf.GetTempDir()
        self.backup_sources = self._getAvaibleSyncSourceFolders()
        self.backup_dest = self.conf.GetDestinaionMarks()
        self.ignore_size_file = int(self.conf.GetIgnoreFileSize()) * 1024 * 1024
        self.ignore_types = self.conf.GetIgnoreFileTypes()

        self.conn = db.CreateDB('initdb.sql')

    def CreateBackups(self):
        zip_files = []
        ft.MakeDirs(self.temp_zip_dir)

        for key in self.backup_sources.keys():
            copy_source = self.backup_sources[key]
            
            if self._needBackup( db.GetLastBackupTime(self.conn, copy_source) ):
                print(f'Start backup: [{copy_source}]')
                timestamp = bct.GetUnixTimestamp()
                file_time = str(datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y_%H-%M-%S'))
                zip_filename = f'{key}_{file_time}.bted'
                zip_temp_path = os.path.join(self.temp_zip_dir, zip_filename)
                self._writeToArchive(copy_source, zip_temp_path, b'12345')
                db.InsertNewBackupInfo(self.conn, timestamp, copy_source, zip_filename)
                zip_files.append(zip_temp_path)

        for dest in self.backup_dest:
            if dest == 'local':            
                dest_folders = self.conf.GetLocalDestinationFolders()
                dest_folders.remove(self.temp_zip_dir)
                for dest_f in dest_folders:
                    ft.CopyFiles(zip_files, dest_f)
                    
            if dest == 'GDrive':
                pass

    def ClearTempDir(self):
        if self._backupToLocalExists():
            return

        files = os.listdir(self.temp_zip_dir)
        for item in files:
            if item.endswith('.bted'):
                os.remove(os.path.join(self.temp_zip_dir, item))

    def _getAvaibleSyncSourceFolders(self):
        config_sources = self.conf.GetBackupSources()
        avaible_folders = {}

        for lable in config_sources.keys():
            if ft.IsFolderAvailable( config_sources[lable] ):
                avaible_folders[lable] = config_sources[lable]

        return avaible_folders

    def _needBackup(self, date): 
        days = self.conf.GetEachBackup()
        dist = datetime.fromtimestamp(bct.GetUnixTimestamp()) - datetime.fromtimestamp(date)

        if dist.days >= days:
            return True
            
        return False

    def _writeToArchive(self, path, zip_name, password):
        ziph = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(path):
            for file in files:
                if self._isFileIgnore(file):
                    continue
                
                filePath = os.path.join(root, file)

                if os.path.getsize(filePath) >= self.ignore_size_file:
                    continue

                ziph.write(filePath)
        
        ziph.setpassword(password)

    def _isFileIgnore(self, fileName): 
        for fileType in self.ignore_types:
            if fileName.endswith(fileType):
                return True
        
        if fileName.startswith('~'): # Игнорировать файлы блокировки (Windows)
            return True

        return False

    def _backupToLocalExists(self):
        dests = self.conf.GetDestinaionMarks()
        for dest in dests:
            if dest == 'local':
                return True
        
        return False