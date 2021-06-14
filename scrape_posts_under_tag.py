import concurrent.futures
import time
from typing import List

import pandas as pd
from instascrape import Post

from instascrape_adaptor.json_processor import JsonDict
from instascrape_adaptor.post_adaptor import PostAdaptor


def timing(func):
    def wrapper(*arg, **kw):
        t1 = time.perf_counter()
        res = func(*arg, **kw)
        t2 = time.perf_counter()
        print(f'Finished in {t2 - t1} seconds by {func.__name__}')
        return res

    return wrapper


def download_post(post_code: str, dir_path: str) -> dict:
    print(f"saving {post_code}")
    post = PostAdaptor(Post(post_code))
    post.save_media(dir_path)
    print(f"post {post_code} saved...")
    return post.to_dict()


@timing
def scrape_posts(post_codes: List[str], post_json_file, post_img_file):
    # for code in codes:
    # download_post(post_codes)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        args = [(code, post_img_file) for code in post_codes]
        results = executor.map(lambda p: download_post(*p), args)
        JsonDict.save([result for result in results if result], post_json_file)


if __name__ == '__main__':
    df = pd.read_csv("data/fake_account_posts_0614.csv", header=None)
    codes = df[0].unique()
    scrape_posts(codes, 'data/post_0614.json', 'data/img_0614')
    print(f"scraped {len(codes)} posts")
