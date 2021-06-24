import concurrent.futures
import heapq
from typing import List, Dict, Tuple

import pytesseract
import textdistance
from PIL import Image

from instascrape_adaptor.json_processor import JsonDict
from scrape_posts_under_tag import timing
from username_policy import UserName


class ImageTextExtractor:
    def __init__(self, img_path: str, rule=None):
        try:
            self.img = Image.open(img_path)
        except Exception as err:
            print(f"err opening image: {err}")
            self.img = None
        self.words = None
        self.rule = rule

    def extract_words(self):
        if self.words is None:
            self.words = pytesseract.image_to_string(self.img).split()
            if self.rule:
                # remove repeated words
                self.words = set(self.words)
                self.words = list(filter(self.rule, self.words))
        return self.words

    def find_closest_words(self, target: str, top_k: int, distance_threshold: float = float('inf')) \
            -> Tuple[Dict[str, List[dict]], bool]:
        """

        :param distance_threshold:
        :param target: word to compare to
        :param top_k: most similar k words
        :returns
        processed_dict: list of most similar words of size top_k, element in the format of
        {target word: [{extracted similar word from image: distance}] }
        success: bool if request succeeds
        """
        if not isinstance(target, str) or self.img is None:
            return {target: []}, False
        rlt = []
        for word in self.extract_words():
            d = textdistance.levenshtein(target, word)
            if d < distance_threshold:
                heapq.heappush(rlt, (d, word))
                if len(rlt) > top_k:
                    heapq.heappop(rlt)
        # format
        return {target: [{word: distance} for distance, word in rlt]}, bool(rlt)


def extract_fake_username(json_dict, img_dir, top_k=2):
    username = json_dict['username']
    img_path = f"{img_dir}/{json_dict['shortcode']}.png"
    print(f"processing username: {json_dict['username']}, code: {json_dict['shortcode']}")

    image = ImageTextExtractor(img_path, UserName.is_username)

    # set distance threshold
    distance_threshold = len(username) // 2 if isinstance(username, str) else float('inf')

    rlt, success = image.find_closest_words(username, top_k, distance_threshold)
    if success:
        json_dict['fake_names'] = rlt[username]
    return json_dict, success


@timing
def find_similar_names_from_posts(post_json_file, img_dir, rlt_file):
    json_dicts = JsonDict.loads(post_json_file)
    saved_codes = set([post['shortcode'] for post in JsonDict.loads(rlt_file)])
    unsaved_json_dicts = [json_dict for json_dict in json_dicts if json_dict['shortcode'] not in saved_codes]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        args = [(json_dict, img_dir) for json_dict in unsaved_json_dicts]
        results = executor.map(lambda p: extract_fake_username(*p), args)
        rlt = [r for r, success in results if success]
        JsonDict.save(rlt, rlt_file)
