from instascrape import Profile

from profile_adaptor import ProfileAdaptor

profile = ProfileAdaptor(Profile("annaraya_6697"))
print(profile.json_str())
profile.save_media("data/profile_pic")
