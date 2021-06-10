import abc
from typing import Optional

import yaml


class ScraperAdaptor(abc.ABC):
    @staticmethod
    def read_config(key: str, config_file: str = 'auth.yaml') -> Optional[str]:
        with open(config_file, 'r') as config_file:
            config = yaml.load(config_file, Loader=yaml.BaseLoader)
            return config.get(key, '')

    def __init__(self, scraper):
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
            "cookie": f'sessionid={self.read_config("session_id")};'
        }
        self._scraper = scraper
        self._has_data = False
        self.__attempt_scrape = False

    def _scrape(self):
        if not self.__attempt_scrape:
            self.__attempt_scrape = True
            try:
                self._scraper.scrape(headers=self._headers)
            except Exception as err:
                print(f"failed scrape, err: {err}")
                return
            self._has_data = True

    @abc.abstractmethod
    def to_dict(self):
        raise NotImplementedError

    @abc.abstractmethod
    def json_str(self):
        raise NotImplementedError

    @abc.abstractmethod
    def save_media(self, file_name: str):
        raise NotImplementedError
