import os

# Return true if file have read acces
def IsFolderAvailable(folder):
    return os.access(folder, os.R_OK)

# Return true if file exists
def IsFileExists(file):
    return os.path.exists(file) and os.path.isfile(file)

# Return true if folder exists
def IsFolderExists(folder):
    return os.path.exists(folder) and os.path.isdir(folder)

# Reading file to string and return his
def ReadAllFile(file):
    if IsFileExists(file):
        f = open(file, 'r')
        data = f.read(file)
        f.close()
        return data
    else:
        return ''