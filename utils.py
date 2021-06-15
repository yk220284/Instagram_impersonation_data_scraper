import time

import yaml


def timing(func):
    def wrapper(*arg, **kw):
        t1 = time.perf_counter()
        res = func(*arg, **kw)
        t2 = time.perf_counter()
        print(f'Finished in {t2 - t1} seconds by {func.__name__}')
        return res

    return wrapper


class Authenticator:
    def __init__(self, config_file: str = 'auth.yaml'):
        self.__config_file = config_file

    def read_config(self, key: str):
        with open(self.__config_file, 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.BaseLoader)
            return config.get(key, '')
