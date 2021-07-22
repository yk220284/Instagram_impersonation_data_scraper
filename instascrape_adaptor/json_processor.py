import json
import simplejson
from collections import deque
from typing import Dict, List


class JsonDict:
    @staticmethod
    def save(json_dicts: List[dict], file_path):
        with open(file_path, 'w') as f:
            simplejson.dump(json_dicts, f, sort_keys=True, indent=4, default=str, ignore_nan=True)

    @staticmethod
    def extend(json_dicts: List[dict], file_path):
        with open(file_path, 'r+') as file:
            file_data = json.load(file)
            file_data.extend(json_dicts)
            file.seek(0)
            simplejson.dump(file_data, file, sort_keys=True, indent=4, default=str, ignore_nan=True)

    def __init__(self, json_dict: dict):
        """
        Adaptor for python dictionary to handle dictionary json conversion and utilities
        :param json_dict: python dictionary of JSON object
        """
        if not isinstance(json_dict, dict):
            raise Exception("require json dictionary")
        self.json_dict = json_dict

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.json_dict.__repr__()

    def __getitem__(self, item):
        return self.json_dict[item]

    def to_json(self) -> str:
        return simplejson.dumps(self.json_dict, indent=4, default=str, ignore_nan=True)

    def collect_values(self, *target_keys: str) -> Dict[str, list]:
        """
        Collect values according to a key from a nested dict
        :param target_keys: list of strings representing keys to be extracted from nested JSON dict
        :return: a pair of key and a list of values with that key in nested jJSON
        """
        rlt = {key: list() for key in target_keys}
        q = deque([])
        q.append(self.json_dict)
        while q:
            parent = q.popleft()
            if isinstance(parent, dict):
                for k, v in parent.items():
                    if k in rlt:
                        rlt[k].append(v)
                    if isinstance(v, (list, dict)):
                        q.append(v)
            else:
                for v in parent:
                    if isinstance(v, (list, dict)):
                        q.append(v)
        return rlt

    @staticmethod
    def loads(file_path: str) -> dict:
        with open(file_path, "r") as file:
            return json.load(file)
