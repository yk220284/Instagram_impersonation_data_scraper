import csv
import time
from datetime import datetime
from time import sleep
import requests

from authenticator import Authenticator
from instascrape_adaptor.json_processor import JsonDict


class TagScraper:
    POST_ID_KEY = "code"
    MAX_ID_KEY = "next_max_id"

    def __init__(self, tag: str, max_id: str = '', authenticator=Authenticator("auth.yaml")):
        self._headers = {"sessionid": authenticator.read_config('session_id')}
        self.base_url = f"https://www.instagram.com/explore/tags/{tag}/?__a=1"
        self.max_id = max_id
        self.post_codes = []

    def scrape_page(self):
        url = self.base_url + f"&max_id={self.max_id}" if self.max_id else self.base_url
        response = requests.get(url, cookies=self._headers)
        json_dict = JsonDict(response.json())
        rlt = json_dict.collect_values(self.POST_ID_KEY, self.MAX_ID_KEY)
        new_max_id, *_ = list(
            filter(lambda s: isinstance(s, str) and s.endswith("==") and s != self.max_id, rlt[self.MAX_ID_KEY]))
        self.max_id = new_max_id
        self.post_codes.extend(rlt[self.POST_ID_KEY])
        print(f"have {len(self.post_codes)} posts")

    def save_record(self, post_file: str, max_id_file: str):
        with open(post_file, 'a') as file:
            for code in self.post_codes:
                file.write(code)
                file.write('\n')
        with open(max_id_file, 'w') as file:
            file.write(self.max_id)


FAKE_TAG_RECORD_FILE = "data/fake_account_posts.csv"
if __name__ == '__main__':
    with open("data/max_id.txt", 'r') as f:
        max_id = f.readline()
    fake_account_tag = TagScraper('fakeaccount', max_id)
    for _ in range(0, 5):
        ts = int(time.time())
        print(f"scraped tag at {datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}")
        fake_account_tag.scrape_page()
        sleep(2)
    fake_account_tag.save_record("data/fake_account_posts_0614.csv", 'data/max_id.txt')
