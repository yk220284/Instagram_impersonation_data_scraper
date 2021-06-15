import concurrent.futures
import heapq
from typing import List, Dict

import pytesseract
import textdistance
from PIL import Image

from instascrape_adaptor.json_processor import JsonDict
from scrape_posts_under_tag import timing


class ImageTextExtractor:
    def __init__(self, img_path: str):
        self.img = Image.open(img_path)
        self.words = None

    def extract_words(self):
        if self.words is None:
            self.words = pytesseract.image_to_string(self.img).split()
        return self.words

    def find_closest_words(self, target: str, top_k: int, distance_threshold: float = float('inf')) \
            -> Dict[str, List[dict]]:
        """

        :param distance_threshold:
        :param target: word to compare to
        :param top_k: most similar k words
        :return: list of most similar words of size top_k, element in the format of
        {target word: [{extracted similar word from image: distance}] }
        """
        rlt = []
        for word in self.extract_words():
            d = textdistance.levenshtein(target, word)
            if d < distance_threshold:
                heapq.heappush(rlt, (d, word))
                if len(rlt) > top_k:
                    heapq.heappop(rlt)
        # format
        return {target: [{word: distance} for distance, word in rlt]}


def extract_fake_username(json_dict, img_dir, top_k=2, distance_threshold=4):
    username = json_dict['username']
    if not isinstance(username, str):
        # NaN username 
        return None
    print(f"processing username: {json_dict['username']}, code: {json_dict['shortcode']}")
    img_path = f"{img_dir}/{json_dict['shortcode']}.png"
    try:
        image = ImageTextExtractor(img_path)
    except Exception as err:
        print(err)
        return None
    rlt = image.find_closest_words(username, top_k, distance_threshold)
    if rlt[username]:
        # image contain words
        json_dict['fake_names'] = rlt[username]
        return json_dict
    return None


@timing
def find_similar_names(json_dicts, img_dir, rlt_file):
    # for json_dict in json_dicts:
    #     extract_fake_username(json_dict, img_dir)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        args = [(json_dict, img_dir) for json_dict in json_dicts]
        results = executor.map(lambda p: extract_fake_username(*p), args)

        rlt = [result for result in results if result]

        print(f"Found {len(rlt)} pair")
        JsonDict.save(rlt, rlt_file)


if __name__ == '__main__':
    json_dicts = JsonDict.loads("data/post_0614.json")
    find_similar_names(json_dicts, "data/img_0614", "data/fake_username_0614.json")
