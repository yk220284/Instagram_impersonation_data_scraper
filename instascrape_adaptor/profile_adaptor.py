from typing import Optional, Dict, Tuple

from instascrape_adaptor.scraper_adaptor import ScraperAdaptor


class ProfileAdaptor(ScraperAdaptor):
    TARGET_ATTRIBUTES = ["followers",
                         "following",
                         "username",
                         "full_name",
                         "business_category_name",
                         "overall_category_name",
                         "is_business_account",
                         "is_verified",
                         "profile_pic_url",
                         "profile_pic_url_hd",
                         "posts"]

    def __init__(self, scraper):
        super().__init__(scraper)
        self.username = scraper.source

    def to_dict(self) -> Tuple[Dict[str, any], bool]:
        if self._scrape():
            json_dict = self._scraper.to_dict()
            return {k: json_dict[k] for k in self.TARGET_ATTRIBUTES}, True
        return {'username': self.username}, False

    def save_media(self, dir_path: str) -> bool:
        if self._scrape():
            json_dict, _ = self.to_dict()
            file_path = self.create_path(dir_path, json_dict['username'])
            self.download_image(file_path, json_dict['profile_pic_url_hd'])
            return True
        return False
