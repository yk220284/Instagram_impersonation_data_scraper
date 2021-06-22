from typing import Dict, Optional, Tuple

from instascrape_adaptor.scraper_adaptor import ScraperAdaptor


class PostAdaptor(ScraperAdaptor):
    TARGET_ATTRIBUTES = ['shortcode', 'display_url', 'username', 'full_name', 'upload_date']

    def __init__(self, scraper):
        super().__init__(scraper)
        self.shortcode = scraper.source

    def to_dict(self) -> Tuple[Dict[str, any], bool]:
        if self._scrape():
            json_dict = self._scraper.to_dict()
            return {k: json_dict[k] for k in self.TARGET_ATTRIBUTES}, True
        return {'shortcode': self.shortcode}, False

    def save_media(self, dir_path: str) -> bool:
        if self._scrape():
            d, _ = self.to_dict()
            file_path = self.create_path(dir_path, f"{d.get('shortcode')}.png")
            self._scraper.download(file_path)
            return True
        return False
