import os

import folders_sync
import backup_ted

if __name__ == '__main__':
    print('BackupTED Started!')

    backupted = backup_ted.BackupTED()
    backupted.CreateBackups()
    backupted.ClearTempDir()

    fsync = folders_sync.TEDSyncFolders()
    fsync.SyncFolders()
    fsync.ClearOldBackups()
