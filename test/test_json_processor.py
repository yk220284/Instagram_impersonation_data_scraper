import json
from unittest import TestCase

from instascrape_adaptor.json_processor import collect_values


class Test(TestCase):
    def test_collect_values(self):
        with open('fakehashtag.json') as f:
            json_dict = json.load(f)
            rlt = collect_values(json_dict, 'code', 'a')
            self.assertEqual(len(rlt['code']), 39)
            self.assertEqual(len(rlt['a']), 0)
