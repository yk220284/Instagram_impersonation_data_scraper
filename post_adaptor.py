import json
from typing import Dict

from scraper_adaptor import ScraperAdaptor


class PostAdaptor(ScraperAdaptor):
    TARGET_ATTRIBUTES = ['shortcode', 'display_url', 'username', 'full_name', 'upload_date']

    def __init__(self, scraper):
        super().__init__(scraper)

    def to_dict(self) -> Dict[str, any]:
        self._scrape()
        json_dict = self._scraper.to_dict()
        return {k: json_dict[k] for k in self.TARGET_ATTRIBUTES}

    def json_str(self) -> str:
        return json.dumps(self.to_dict(), indent=4, default=str)

    def save_media(self, file_name: str):
        self._scrape()
        if self._has_data:
            self._scraper.download(file_name)
