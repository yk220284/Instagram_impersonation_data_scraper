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
    saved_codes = set([post['shortcode'] for post in JsonDict.loads(post_json_file)])
    unsaved_codes = [code for code in post_codes if code not in saved_codes]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        args = [(code, post_img_file) for code in unsaved_codes]
        results = executor.map(lambda p: download_post(*p), args)
        rlt = [result for result in results if result]
        JsonDict.extend(rlt, post_json_file)
    print(f"scraped {len(rlt)} posts")


if __name__ == '__main__':
    download_post("CQHDQ05BZmy", "data/0615/img")
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
