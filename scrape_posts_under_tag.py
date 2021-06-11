import concurrent.futures
import time

import pandas as pd
from instascrape import Post

from instascrape_adaptor.post_adaptor import PostAdaptor

df = pd.read_csv("data/fake_account_posts.csv")

t1 = time.perf_counter()


def download_post(post_code: str, dir_path="data/img") -> str:
    print(f"saving {post_code}")
    post = PostAdaptor(Post(post_code))
    post.save_media(dir_path)
    print(f"post {post_code} saved...")
    return post.json_str()


codes = df['code'].unique()[:30]
# for code in codes:
#     download_image(code)

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(download_post, codes)

print(list(results))
t2 = time.perf_counter()

print(f'Finished in {t2 - t1} seconds')
