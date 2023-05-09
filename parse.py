import time
from typing import *

import auto_bean


class Parser:
    def __init__(self, path) -> None:
        self.path = path
        self._acnts = set()
        self._leafs = set()
        self._parse()

    def acnts(self) -> auto_bean.AccountStore:
        return auto_bean.AccountStore(self._acnts)

    def acnt_leafs(self) -> List[auto_bean.Account]:
        return list(self._leafs)

    def _parse(self):
        with open(self.path) as f:
            for word in f.read().split():
                self._parse_acnt(word)

    def _parse_acnt(self, word: str):
        if ":" in word[1:-1] and '\'' not in word:
            prev = None
            for name in word.split(":"):
                acnt = auto_bean.Account(name, prev)
                self._acnts.add(acnt)
                prev = acnt
            self._leafs.add(prev)
