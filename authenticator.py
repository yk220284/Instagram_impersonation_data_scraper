from typing import Optional

import yaml


class Authenticator:
    def __init__(self, config_file: str = 'auth.yaml'):
        self.__config_file = config_file

    def read_config(self, key: str):
        with open(self.__config_file, 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.BaseLoader)
            return config.get(key, '')


if __name__ == '__main__':
    a = Authenticator()
    print(a.read_config("google"))
