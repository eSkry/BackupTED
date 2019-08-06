import configparser
import os

## Config
conf = configparser.ConfigParser()
conf.read("./config/config.conf")

backup_sources = str(conf['Folders']['source'])