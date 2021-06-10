from typing import Dict, Optional

from scraper_adaptor import ScraperAdaptor


class PostAdaptor(ScraperAdaptor):
    TARGET_ATTRIBUTES = ['shortcode', 'display_url', 'username', 'full_name', 'upload_date']

    def __init__(self, scraper):
        super().__init__(scraper)

    def to_dict(self) -> Optional[Dict[str, any]]:
        self._scrape()
        if self._has_data:
            json_dict = self._scraper.to_dict()
            return {k: json_dict[k] for k in self.TARGET_ATTRIBUTES}

    def save_media(self, dir_path: str):
        self._scrape()
        if self._has_data:
            file_path = self.create_path(dir_path, self.to_dict().get('shortcode'))
            self._scraper.download(file_path)
