import configparser
import os

from utils.utilstool import _format_path, str_to_bool


def getconf(file_path):
    config = configparser.ConfigParser()
    config.read(file_path,encoding='UTF-8')

    conf_dict = {}
    for section in config.sections():
        for option in config.options(section):
            value = config.get(section, option)
            conf_dict[f'{option}'] = value

    return conf_dict

if __name__ == '__main__':
    conf_dict = getconf(r'D:\Project\tgMessage\config.ini')
    for key, value in conf_dict.items():
        print(f"{key}:{value}")
        if key == 'edit_lastseen':
            edit_lastseen = str_to_bool(value)
            print(edit_lastseen)