import abc
import os
from typing import Optional, Dict, Tuple

import requests

from instascrape_adaptor.json_processor import JsonDict
from utils import Authenticator


class ScraperAdaptor(abc.ABC):
    @staticmethod
    def create_path(dir_path: str, file_name: str):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        return os.path.join(dir_path, file_name)

    @staticmethod
    def download_image(file_path: str, img_url: str):
        img_bytes = requests.get(img_url).content
        img_name = f'{file_path}.png'
        with open(img_name, 'wb') as img_file:
            img_file.write(img_bytes)

    def __init__(self, scraper, authenticator=Authenticator("auth.yaml")):
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
            "cookie": f'sessionid={authenticator.read_config("session_id")};'
        }
        self._scraper = scraper
        self._has_data = False
        self.__attempt_scrape = False

    def _scrape(self) -> bool:
        """
        Use scraper passed in to scrape
        :return: bool status indicates whether scrape is successful
        """
        if not self.__attempt_scrape:
            self.__attempt_scrape = True
            try:
                self._scraper.scrape(headers=self._headers)
            except Exception as err:
                print(f"failed scrape {self._scraper.source}, {self._scraper.source} err: {err}")
                return False
            self._has_data = True
            return True
        return self._has_data

    def json_str(self) -> str:
        d, _ = self.to_dict()
        return str(JsonDict(d))

    @abc.abstractmethod
    def to_dict(self) -> Tuple[Dict[str, any], bool]:
        raise NotImplementedError

    @abc.abstractmethod
    def save_media(self, dir_path: str) -> bool:
        raise NotImplementedError
