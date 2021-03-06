from create_scraping_folder import create_scraping_folder
from delete_failed_posts_and_media import delete_failed_posts_and_media
from instagram_scraper.tag_scraper import scrape_tags
from instagram_scraper.scrape_posts_under_tag import scrape_posts
from instagram_preprocessing.text_extraction import find_similar_names_from_posts

"""
Configuring Destinations
"""
DATA_DIR = 'data/0809'

if __name__ == '__main__':
    """
    Creating destinations
    """
    POST_CODE___CSV, MAX_ID_FILE, POST___JSON, PROCESSED_POST___JSON, IMG_DIR = create_scraping_folder(DATA_DIR)

    # """
    # Scraping posts' shortcode under a tag
    # possible hashtags are 'fakeaccount', 'fakeaccounts', 'reportthem' and 'scammers'
    # """
    # scrape_tags('fakeaccount', MAX_ID_FILE, POST_CODE___CSV, 2)

    # """
    # Scrape posts
    # """
    # scrape_posts(POST_CODE___CSV, POST___JSON, IMG_DIR)

    # """
    # Process posts
    # """
    # find_similar_names_from_posts(POST___JSON, IMG_DIR, PROCESSED_POST___JSON)

    # """
    # Clear up posts and images
    # """
    # delete_failed_posts_and_media(POST___JSON, PROCESSED_POST___JSON, IMG_DIR)
