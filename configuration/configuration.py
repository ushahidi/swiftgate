from ConfigParser import ConfigParser
from environment import ENV
import sys
import os

def get_config(environment):
    config_dir = "%s/configuration/%s" % (sys.path[0], environment)
    config_files = os.listdir(config_dir)
    config_files = ["%s/%s" % (config_dir, file_name) for file_name in config_files]
    configuration = ConfigParser()
    configuration.read(config_files)
    return configuration

config = get_config(ENV)

