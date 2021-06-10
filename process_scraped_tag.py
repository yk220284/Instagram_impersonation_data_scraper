import concurrent.futures
import time

import pandas as pd
from instascrape import Post

from post_adaptor import PostAdaptor

df = pd.read_csv("data/fake_account_posts.csv")

t1 = time.perf_counter()


def download_post(post_code):
    print(f"saving {post_code}")
    post = PostAdaptor(Post(post_code))
    post.save_media(f"data/img/{post_code}.png")
    print(f"post {post_code} saved...")


codes = df['code'].unique()[:30]
# for code in codes:
#     download_image(code)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_image, codes)

t2 = time.perf_counter()

print(f'Finished in {t2 - t1} seconds')
