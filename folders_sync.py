from itertools import groupby
import datetime
import shutil
import os

import backupted_tools as bct
import folder_tools as ft

# Синхронизация папок с бекапами
# Проверяет наличие бекапов в папках и в случае если в друой папке нет бекапа он копируется
def SyncFolders():
    if bct.BackupToLocalExists():
        local_folders = bct.GetLocalDestinationFolders()
        main_flist = []

        for current_folder in local_folders:
            main_flist = ft.GetBackupsList(current_folder)

            for folder in local_folders:
                if folder == current_folder:
                    continue
                
                for x in main_flist:
                    if not ft.IsFileExists(os.path.join(folder, x)):
                        ft.CopyFile(os.path.join(current_folder, x), folder)

                    
def ClearOldBackups():
    clean_days = bct.GetCleanDays()
    local_folders = bct.GetLocalDestinationFolders()
    current_date = datetime.datetime.fromtimestamp(bct.GetUnixTimestamp())

    for folder in local_folders:
        bted_list = ft.GetBackupsList(folder)
        
        for b_ted in bted_list:
            fpath = os.path.join(folder, b_ted)
            create_date = datetime.datetime.fromtimestamp(os.path.getctime(fpath))
            modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(fpath))
            
            if (current_date - create_date).days >= clean_days or (current_date - modified_date).days >= clean_days:
                os.remove(fpath)
