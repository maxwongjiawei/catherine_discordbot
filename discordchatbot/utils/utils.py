import os
from configparser import ConfigParser


def initiate_config():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.dirname(current_directory)
    config_filepath = dir_path + "\\config.ini"
    print(config_filepath)

    exists = os.path.exists(config_filepath)
    config = None

    if exists:
        print("--------config.ini file found at ", config_filepath)
        config = ConfigParser()
        config.read(config_filepath)
    else:
        print("---------config.ini file not found at ", config_filepath)

    return config
