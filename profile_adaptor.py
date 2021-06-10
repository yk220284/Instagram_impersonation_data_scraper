from typing import Optional, Dict

from scraper_adaptor import ScraperAdaptor


class ProfileAdaptor(ScraperAdaptor):
    def __init__(self, scraper):
        super().__init__(scraper)

    def to_dict(self) -> Optional[Dict[str, any]]:
        self._scrape()
        if self._has_data:
            return self._scraper.to_dict()

    def save_media(self, dir_path: str):
        self._scrape()
        if self._has_data:
            json_dict = self.to_dict()
            file_path = self.create_path(dir_path, json_dict['username'])
            self.download_image(file_path, json_dict['profile_pic_url_hd'])
