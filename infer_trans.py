import re
from typing import *

from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          pipeline)

import auto_bean


class SimpleExpenseFactory:
    def __init__(self, expense_acnts: List[auto_bean.Account]) -> None:
        self.bart = pipeline("zero-shot-classification",
                             model="facebook/bart-large-mnli")
        self.expense_acnts = expense_acnts

    def from_words(self, words: str, from_acnt: auto_bean.Account) -> auto_bean.SimpleExpense:
        amnt = self._amnt_from_words(words) or .0
        expn_acnt = self._expn_acnt_from_words(words)
        crny = auto_bean.USD
        return auto_bean.SimpleExpense(from_acnt, expn_acnt, amnt, crny, desc=words)

    def _expn_acnt_from_words(self, words: str):
        labels = {x.as_str(): x for x in self.expense_acnts}
        ret = self.bart(words, list(labels.keys()))
        return labels[ret['labels'][0]]

    def _amnt_from_words(self, words: str):
        try:
            amnt = re.findall(r'\d+[\.\d+]?', words)[0]
            return float(amnt)
        except:
            print(f"{words}: doesn't contain amounts")
