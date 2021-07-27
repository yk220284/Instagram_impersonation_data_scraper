import os

from instascrape_adaptor.json_processor import JsonDict


def delete_failed_posts_and_media(unprocessed_post_json_file, processed_post_json_file, img_dir):
    unprocessed_post_json_dicts = JsonDict.loads(unprocessed_post_json_file)
    processed_post_json_dicts = JsonDict.loads(processed_post_json_file)

    # remove everything that's not in this set
    processed_post_shortcodes = set([post['shortcode'] for post in processed_post_json_dicts])

    # remove posts from post.json
    failed_posts_shortcode = [post['shortcode'] for post in unprocessed_post_json_dicts if
                              post['shortcode'] not in processed_post_shortcodes]
    JsonDict.delete(unprocessed_post_json_file, failed_posts_shortcode)

    # remove images from img/
    scrapped_imgs = list(filter(lambda file: file.endswith('.png'), os.listdir(img_dir)))
    failed_imgs = [img_file for img_file in scrapped_imgs if
                   img_file.rsplit('_', 1)[0] not in processed_post_shortcodes]
    for img_file in failed_imgs:
        img_path = os.path.join(img_dir, img_file)
        if os.path.exists(img_path):
            os.remove(img_path)
        else:
            print(f"{img_file} does not exist")
