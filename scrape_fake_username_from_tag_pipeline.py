import os

from instagram_scraper.tag_scraper import TagScraper
from scrape_posts_under_tag import scrape_posts
from text_extraction import find_similar_names_from_posts

"""
Configuring Destinations
"""
# DATA_DIR = 'data/0615'
DATA_DIR = 'data/0721'
if not os.path.isdir(DATA_DIR):
    os.mkdir(DATA_DIR)
MAX_ID_FILE = os.path.join(DATA_DIR, 'max_id.txt')
POST_CODE___CSV = os.path.join(DATA_DIR, 'post_code.csv')

POST___JSON = os.path.join(DATA_DIR, 'post.json')
IMG_DIR = os.path.join(DATA_DIR, 'img')
PROCESSED_POST___JSON = os.path.join(DATA_DIR, 'processed_post.json')

"""
Scraping posts' shortcode under a tag
"""
# fake_account_tag = TagScraper('fakeaccount', MAX_ID_FILE)
# fake_account_tag.scrape_pages(page_cnt=10, sleep_interval=2)
# fake_account_tag.save_record(POST_CODE___CSV, MAX_ID_FILE)

"""
Scrape posts 
"""
scrape_posts(POST_CODE___CSV, POST___JSON, IMG_DIR)
# find_similar_names_from_posts(POST___JSON, IMG_DIR, PROCESSED_POST___JSON)
