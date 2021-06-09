from collections import deque
from typing import Dict


def collect_values(json_dict: dict, *target_keys: str) -> Dict[str, list]:
    if not isinstance(json_dict, dict):
        raise Exception("require json dictionary")

    rlt = {key: list() for key in target_keys}
    q = deque([])
    q.append(json_dict)
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
