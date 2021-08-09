# Instagram Impersonation Data Scraper

This script focuses on data scrapping. Data persistence, exploration and labelling is dealt
by [this Angular app] (https://github.com/yk220284/instagram-data-viewer).

## Scrapping pipeline

`main.py` contains the main scrapping pipeline. Below are components contained.

### Tag scrapper

`instagram_scraper/tag_scraper.py` contains `TagScrapper` class that scrape shortcode for posts under a hashtag.

### Post scrapper

`instagram_scraper/scrape_posts_under_tag.py` contains the main logic to scrap posts given the shortcode, utilising

1. `instascrape_adaptor/post_adaptor.py` an adaptor for `instascrape.Post`
2. `instascrape_adaptor/profile_adaptor.py` an adaptor for `instascrape.Profile`

### Post pre-processing

`instagram_preprocessing.text_extraction.py` conducts and initial filtering on irrelevant posts and extract texts from
posts and propose a list of fake usernames to reduce workload for manual labelling

## Helper Classes

`Authenticator` in `utils.py` can handle credentials such as API keys and Cookies stored in yaml file.
`JsonDict` from `instascrape_adaptor.json_processor` handle miscellaneous tasks handling json processing, formatting,
persisting etc.