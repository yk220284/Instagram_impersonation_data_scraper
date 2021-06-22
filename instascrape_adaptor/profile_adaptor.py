from typing import Optional, Dict, Tuple

from instascrape_adaptor.scraper_adaptor import ScraperAdaptor


class ProfileAdaptor(ScraperAdaptor):
    def __init__(self, scraper):
        super().__init__(scraper)
        self.username = scraper.source

    def to_dict(self) -> Tuple[Dict[str, any], bool]:
        if self._scrape():
            return self._scraper.to_dict(), True
        return {'username': self.username}, False

    def save_media(self, dir_path: str) -> bool:
        if self._scrape():
            json_dict, _ = self.to_dict()
            file_path = self.create_path(dir_path, json_dict['username'])
            self.download_image(file_path, json_dict['profile_pic_url_hd'])
            return True
        return False
