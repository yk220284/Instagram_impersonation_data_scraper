import concurrent.futures

import pandas as pd
from instascrape import Post

from instascrape_adaptor.json_processor import JsonDict
from instascrape_adaptor.post_adaptor import PostAdaptor
from utils import timing


def download_post(post_code: str, dir_path: str) -> dict:
    print(f"saving {post_code}")
    post = PostAdaptor(Post(post_code))
    post.save_media(dir_path)
    print(f"post {post_code} saved...")
    return post.to_dict()


@timing
def scrape_posts(posts_csv_file: str, post_json_file, post_img_file):
    df = pd.read_csv(posts_csv_file, header=None)
    post_codes = df[0].unique()
    # for code in post_codes:
    #     download_post(code, post_img_file)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        args = [(code, post_img_file) for code in post_codes]
        results = executor.map(lambda p: download_post(*p), args)
        rlt = [result for result in results if result]
        JsonDict.save(rlt, post_json_file)
    print(f"scraped {len(rlt)} posts")


if __name__ == '__main__':
    scrape_posts("data/fake_account_posts_0615.csv", 'data/post_0615.json', 'data/img/0615')
