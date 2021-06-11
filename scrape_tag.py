import csv
import time
from datetime import datetime
from time import sleep
from typing import Optional, List, Tuple

import pandas as pd
import requests
import yaml

from instascrape_adaptor.json_processor import JsonDict


def read_config(config_file: str, key: str) -> Optional[str]:
    with open(config_file, 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
        return config[key]


def scrape_tag(tag_str: str, headers: dict, max_id: str = '') -> Tuple[List[str], str]:
    POST_ID_KEY = "code"
    MAX_ID_KEY = "next_max_id"
    base_url = f"https://www.instagram.com/explore/tags/{tag_str}/?__a=1"
    url = base_url + f"&max_id={max_id}" if max_id else base_url
    response = requests.get(url, cookies=headers)
    json_dict = JsonDict(response.json())
    rlt = json_dict.collect_values(POST_ID_KEY, MAX_ID_KEY)
    new_max_id, *_ = list(filter(lambda s: isinstance(s, str) and s.endswith("==") and s != max_id, rlt[MAX_ID_KEY]))
    return rlt[POST_ID_KEY], new_max_id


def write_record(new_data: list, filename: str):
    with open(filename, 'a') as file:
        w = csv.writer(file)
        for row in new_data:
            w.writerow(row)


INSTAGRAM_CONFIG_FILE = 'auth.yaml'
FAKE_TAG_RECORD_FILE = "data/fake_account_posts.csv"
if __name__ == '__main__':
    headers = {"sessionid": read_config(INSTAGRAM_CONFIG_FILE, 'session_id')}

    df = pd.read_csv(FAKE_TAG_RECORD_FILE)
    # max_id: str = '' if df.size == 0 or pd.isna(df.iloc[-1]['max_id']) else df.iloc[-1]['max_id']
    max_id = ''
    
    for _ in range(0, 40):
        ts = int(time.time())
        print(f"scraped tag at {datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"with max_id {max_id}")
        post_ids, next_max_id = scrape_tag("fakeaccount", headers, max_id)
        print(f"got {len(post_ids)} posts")
        print("complete, writing records")
        write_record([(post_id, ts, max_id) for post_id in post_ids], "data/fake_account_posts.csv")
        max_id = next_max_id
        sleep(2)
