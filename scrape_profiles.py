from instascrape import Profile, Post

from instascrape_adaptor.post_adaptor import PostAdaptor
from instascrape_adaptor.profile_adaptor import ProfileAdaptor

# profile = ProfileAdaptor(Profile("therealjoeldunn"))
# print(profile.json_str())
# profile.save_media("data/profile_pic")

if __name__ == '__main__':
    p = PostAdaptor(Post("CRCG9AmhFm_"))
    print(p.json_str())
