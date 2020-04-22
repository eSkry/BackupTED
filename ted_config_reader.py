import configparser
import os

class TEDConfigReader(object):
    def __init__(self, file):
        self.open(file)

    def open(self, file):
        self.conf = configparser.ConfigParser()
        self.conf.read(file)

    def GetIgnoreFileTypes(self):
        return self._safeGetParameter('ignore', 'types', '')
    
    def GetIgnoreFileSize(self):
        return self._safeGetParameter('ignore', 'size', 0)
    
    def GetDatabaseFile(self):
        return self._safeGetParameter('Database', 'name', None)

    def GetCleanDays(self):
        mark = str(self._safeGetParameter('Clean', 'older', 10))
        if mark[-1] == 'd':
            return int(mark[:-1])
        if mark[-1] == 'w':
            return int(mark[:-1]) * 7
        if mark[-1] == 'm':
            return int(mark[:-1]) * 28
        return 0
            
    def GetBackupSources(self):
        sources = str(self._safeGetParameter('Backup', 'source', '')).replace("'", '').split(';')
        pairs = {}

        for val in sources:
            temp = val.split('@')
            pairs[temp[0]] = temp[1]
        return pairs

    def GetEachBackup(self):
        mark = self._safeGetParameter('Backup', 'each', '7d')
        if mark[-1] == 'd':
            return int(mark[:-1])
        if mark[-1] == 'w':
            return int(mark[:-1]) * 7
        if mark[-1] == 'm':
            return int(mark[:-1]) * 28
        return 7

    def GetDestinaionMarks(self):
        return self._safeGetParameter('Backup', 'dest', 'local')

    def GetZipPassword(self):
        return self._safeGetParameter('Backup', 'zip_pass', None)

    def GetTempDir(self):
        return self._safeGetParameter('Backup', 'temp_dir', './')

    def GetLocalDestinationFolders(self):
        return str(self._safeGetParameter('local', 'path', '')).replace("'", '').split(';')

    def _safeGetParameter(self, section, option, default_value):
        if self.conf.has_section(section) and self.conf.has_option(section, option):
            return self.conf[section][option]
        return default_value



        