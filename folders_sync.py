from itertools import groupby
import shutil
import os

import backupted_tools as bct
import folder_tools as ft

# Синхронизация папок с бекапами
# Проверяет наличие бекапов в папках и в случае если в друой папке нет бекапа он копируется
def SartSyncFolders():
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

                    



            
            
