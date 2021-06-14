import concurrent.futures
import heapq
import math
from typing import List, Tuple, Dict

from PIL import Image
import pytesseract
import textdistance

from instascrape_adaptor.json_processor import JsonDict
from scrape_posts_under_tag import timing


# json_dict = json_dicts[0]
class ImageTextExtractor:
    def __init__(self, img_path: str):
        self.img = Image.open(img_path)
        self.words = None

    def extract_words(self):
        if self.words is None:
            self.words = pytesseract.image_to_string(self.img).split()
        return self.words

    def find_closest_words(self, target: str, top_k: int, distance_threshold: float = float('inf')) -> Dict[
        str, List[dict]]:
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


def extract_fake_username(json_dict, top_k=2, distance_threshold=4):
    print(f"processing {json_dict['username']} code {json_dict['shortcode']}")
    img_path = f"data/img/{json_dict['shortcode']}.png"
    try:
        image = ImageTextExtractor(img_path)
    except Exception as err:
        print(err)
        return None
    username = json_dict['username']
    if isinstance(username, str):
        rlt = image.find_closest_words(username, top_k, distance_threshold)
        return rlt if rlt[username] else None


@timing
def find_similar_names(json_dicts):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(extract_fake_username, json_dicts)
        JsonDict.save([result for result in results if result], "data/fake_username_close.json")


if __name__ == '__main__':
    json_dicts = JsonDict.loads("data/posts.json")
    find_similar_names(json_dicts)
