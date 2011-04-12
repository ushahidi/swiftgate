from ConfigParser import ConfigParser
from environment import ENV
import sys
import os
import re

def get_config(environment):
    config_dir = "%s/%s" % (re.sub('configuration\.(py|pyc)', '', os.path.abspath(__file__)), environment)
    config_files = os.listdir(config_dir)
    config_files = ["%s/%s" % (config_dir, file_name) for file_name in config_files]
    configuration = ConfigParser()
    configuration.read(config_files)
    return configuration

config = get_config(ENV)

