import os.path

from instascrape_adaptor.json_processor import JsonDict


def create_scraping_folder(DATA_DIR):
    POST_CODE___CSV = os.path.join(DATA_DIR, 'post_code.csv')
    MAX_ID_FILE = os.path.join(DATA_DIR, 'max_id.txt')
    POST___JSON = os.path.join(DATA_DIR, 'post.json')
    PROCESSED_POST___JSON = os.path.join(DATA_DIR, 'processed_post.json')
    IMG_DIR = os.path.join(DATA_DIR, 'img')
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    if not os.path.exists(POST___JSON):
        JsonDict.save([], POST___JSON)
    if not os.path.exists(PROCESSED_POST___JSON):
        JsonDict.save([], PROCESSED_POST___JSON)
    if not os.path.isdir(DATA_DIR):
        os.mkdir(IMG_DIR)
    return POST_CODE___CSV, MAX_ID_FILE, POST___JSON, PROCESSED_POST___JSON, IMG_DIR
