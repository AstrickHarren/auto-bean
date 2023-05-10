import re
from difflib import SequenceMatcher
from typing import List


def extract_floats(words: str) -> List[float]:
    ret = re.findall(r'[-+]?(?:\d*\.*\d+)', words)
    return list(map(lambda x: float(x), ret))


def extract_first_float(words: str) -> float | None:
    ret = extract_floats(words)
    if len(ret) == 0:
        return
    else:
        return ret[0]


def similarity(a, b):
    SequenceMatcher(None, a, b).ratio()


def argmax(iterable):
    return max(enumerate(iterable), key=lambda x: x[1])[0]
