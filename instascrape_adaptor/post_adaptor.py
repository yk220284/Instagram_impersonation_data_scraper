from typing import Dict, Tuple

from instascrape import Profile

from instascrape_adaptor.profile_adaptor import ProfileAdaptor
from instascrape_adaptor.scraper_adaptor import ScraperAdaptor


class PostAdaptor(ScraperAdaptor):
    TARGET_ATTRIBUTES = ['shortcode', 'display_url', 'profile_pic_url', 'username', 'full_name', 'upload_date',
                         'caption', 'hashtags', 'is_video', 'tagged_users']

    def __init__(self, scraper, getProfile=True):
        super().__init__(scraper)
        self.shortcode = scraper.source
        self.getProfile = getProfile
        self.profile = None

    def to_dict(self) -> Tuple[Dict[str, any], bool]:
        if self._scrape():
            json_dict = self._scraper.to_dict()
            profile_dict = {}
            if self.getProfile:
                self.profile = ProfileAdaptor(Profile(json_dict['username']))
                # if cannot scrape profile, reset getProfile to false
                profile_dict, self.getProfile = self.profile.to_dict()
                if not self.getProfile:
                    print(f"Can't collect profile for {self.shortcode}")
                    return {'shortcode': self.shortcode}, False
                profile_dict = {"profile": profile_dict} if self.getProfile else {}
            return {**{k: json_dict[k] for k in self.TARGET_ATTRIBUTES}, **profile_dict}, True
        return {'shortcode': self.shortcode}, False

    def save_media(self, dir_path: str) -> bool:
        if self._scrape():
            d, success = self.to_dict()
            if not success or d['is_video']:
                return False
            try:
                display_url_path = self.create_path(dir_path, f"{d.get('shortcode')}_post")
                self.download_image(display_url_path, d['display_url'])
                if self.getProfile:
                    profile_pic_url_path = self.create_path(dir_path, f"{d.get('shortcode')}_profile")
                    self.download_image(profile_pic_url_path, d['profile']['profile_pic_url_hd'])
            except Exception as err:
                print(f"Error: {err} when saving post {d}\n")
                return False
            return True
        return False
