import os
import time
from datetime import datetime
from time import sleep

import requests

from instascrape_adaptor.json_processor import JsonDict
from utils import Authenticator


class TagScraper:
    POST_ID_KEY = "code"
    MAX_ID_KEY = "next_max_id"

    def __init__(self, tag: str, max_id_file: str = '', authenticator=Authenticator("auth.yaml")):
        self._headers = {"sessionid": authenticator.read_config('session_id')}
        self.base_url = f"https://www.instagram.com/explore/tags/{tag}/?__a=1"
        self.max_id = ''
        self.post_codes = []
        if max_id_file and os.path.isfile(max_id_file):
            self.read_max_id_from_file(max_id_file)

    def read_max_id_from_file(self, max_id_file: str):
        with open(max_id_file, 'r') as f:
            max_id_str = f.readline()
            if not max_id_str.endswith("=="):
                raise Exception("max_id_str should end with \'==\'")
            self.max_id = max_id_str

    def scrape_page(self):
        url = self.base_url + f"&max_id={self.max_id}" if self.max_id else self.base_url
        response = requests.get(url, cookies=self._headers)
        json_dict = JsonDict(response.json())
        rlt = json_dict.collect_values(self.POST_ID_KEY, self.MAX_ID_KEY)
        try:
            new_max_id, *_ = list(
                filter(lambda s: isinstance(s, str) and s.endswith("==") and s != self.max_id, rlt[self.MAX_ID_KEY]))
        except Exception as err:
            new_max_id = self.max_id
            print(f"err: {err} max_id: {new_max_id}")
        self.max_id = new_max_id
        self.post_codes.extend(rlt[self.POST_ID_KEY])
        print(f"have {len(self.post_codes)} posts")

    def save_record(self, post_file: str, max_id_file: str):
        with open(post_file, 'a+') as file:
            for code in self.post_codes:
                file.write(code)
                file.write('\n')
        with open(max_id_file, 'w+') as file:
            file.write(self.max_id)

    def scrape_pages(self, page_cnt: int, sleep_interval: int = 1):
        for i in range(0, page_cnt):
            ts = int(time.time())
            print(f"scraping tag at page {i + 1} {datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}")
            self.scrape_page()
            sleep(sleep_interval)


def scrape_tags(hashtag, max_id_file, post_csv_file):
    fake_account_tag = TagScraper(hashtag, max_id_file)
    fake_account_tag.scrape_pages(page_cnt=1, sleep_interval=2)
    fake_account_tag.save_record(post_csv_file, max_id_file)


if __name__ == '__main__':
    # fake_account_tag = TagScraper('fakeaccount', max_id_file)
    fake_account_tag = TagScraper('fakeaccount')
    fake_account_tag.scrape_pages(page_cnt=5, sleep_interval=2)
    fake_account_tag.save_record("data/fake_account_posts_0615.csv", 'data/max_id.txt')
