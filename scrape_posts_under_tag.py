import concurrent.futures
from typing import Tuple

import pandas as pd
from instascrape import Post

from instascrape_adaptor.json_processor import JsonDict
from instascrape_adaptor.post_adaptor import PostAdaptor
from utils import timing


def download_post(post_code: str, dir_path: str) -> Tuple[dict, bool]:
    print(f"saving {post_code}")
    post = PostAdaptor(Post(post_code))
    post.save_media(dir_path)
    return post.to_dict()


@timing
def scrape_posts(posts_csv_file: str, post_json_file, post_img_file):
    df = pd.read_csv(posts_csv_file, header=None)
    post_codes = df[0].unique()
    saved_codes = set([post['shortcode'] for post in JsonDict.loads(post_json_file)])
    unsaved_codes = [code for code in post_codes if code not in saved_codes]
    unsaved_codes = unsaved_codes[:20]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        args = [(code, post_img_file) for code in unsaved_codes]
        results = executor.map(lambda p: download_post(*p), args)
        valid_results = []
        invalid_codes = []
        for r, success in results:
            if success:
                valid_results.append(r)
            else:
                invalid_codes.append(r['shortcode'])
    dff = df[df[0].isin(invalid_codes) == False]
    dff.to_csv(posts_csv_file, index=False, header=False)
    JsonDict.extend(valid_results, post_json_file)
    print(f"scraped {len(valid_results)} posts")


if __name__ == '__main__':
    print(download_post("CQIq5azHL6B", "data/0615/img"))
# a = Authenticator()
# session_id = a.read_config('session_id')
#
# google = Profile('https://www.instagram.com/google/')
#
# headers = {
#     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
#     "cookie": f"sessionid={session_id};"}
#
# google.scrape(headers=headers)
#
# print(google.followers)
