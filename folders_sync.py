from itertools import groupby
import datetime
import shutil
import os

import backupted_tools as bct
import folder_tools as ft
import ted_config_reader as ted_conf

class TEDSyncFolders(object):
    def __init__(self):
        self.conf = ted_conf.TEDConfigReader('./config/config.conf')

    # Синхронизация папок с бекапами
    # Проверяет наличие бекапов в папках и в случае если в друой папке нет бекапа он копируется
    def SyncFolders(self):
        if self._backupToLocalExists():
            local_folders = self.conf.GetLocalDestinationFolders()
            main_flist = []

            for current_folder in local_folders:
                main_flist = ft.GetBackupsList(current_folder)

                for folder in local_folders:
                    if folder == current_folder:
                        continue
                    
                    for x in main_flist:
                        if not ft.IsFileExists(os.path.join(folder, x)):
                            ft.CopyFile(os.path.join(current_folder, x), folder)

                        
    def ClearOldBackups(self):
        clean_days = self.conf.GetCleanDays()
        local_folders = self.conf.GetLocalDestinationFolders()
        current_date = datetime.datetime.fromtimestamp(bct.GetUnixTimestamp())

        for folder in local_folders:
            bted_list = ft.GetBackupsList(folder)
            
            for b_ted in bted_list:
                fpath = os.path.join(folder, b_ted)
                create_date = datetime.datetime.fromtimestamp(os.path.getctime(fpath))
                
                if (current_date - create_date).days >= clean_days:
                    os.remove(fpath)

    def _backupToLocalExists(self):
        dests = self.conf.GetDestinaionMarks()
        for dest in dests:
            if dest == 'local':
                return True
        
        return False
