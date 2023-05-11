import argparse
import datetime
from difflib import SequenceMatcher
from typing import *

from transformers import pipeline

import auto_bean
import util
from auto_bean import Account, AccountType
from parse import Parser


class SimpleExpenseBuilder:
    def __init__(self,
                 shared_with=None,
                 from_acnt=None,
                 expn_acnt=None,
                 payee=None,
                 desc=None,
                 amnt=None,
                 crny=auto_bean.USD) -> None:
        self._shared_with: List[str] = shared_with or []
        self._from_acnt = from_acnt
        self._expn_acnt = expn_acnt
        self._desc: str = desc or ""
        self._payee: str = payee or ""
        self._crny = crny
        self._amnt = amnt

        self._date = datetime.date.today()

    def _ready_to_build(self):
        return True if self._from_acnt and self._expn_acnt and self._amnt else False

    def try_build(self):
        if not self._ready_to_build():
            return

        return auto_bean.SimpleExpense(
            self._from_acnt, self._expn_acnt, self._amnt, self._crny,
            self._desc, self._payee, self._date, self._shared_with
        )

    def show(self):
        expn = self.try_build()
        if expn:
            print(str(expn))
        return None

    def with_from_acnt(self, from_acnt: Account) -> Self:
        self._from_acnt = from_acnt
        return self

    def with_expn_acnt(self, expn_acnt: Account) -> Self:
        self._expn_acnt = expn_acnt
        return self

    def with_desc(self, desc: str) -> Self:
        self._desc = desc
        return self

    def with_payee(self, payee: str) -> Self:
        self._payee = payee
        return self

    def with_shared(self, shared: auto_bean.Contact | None) -> Self:
        if shared:
            self._shared_with.append(shared.name)
        return self

    def without_shared(self) -> Self:
        self._shared_with = []
        return self

    def with_amnt(self, amnt: float) -> Self:
        self._amnt = amnt
        return self

    def with_crny(self, crny: auto_bean.Currency) -> Self:
        self._crny = crny
        return self


class InteractiveSimpleExpenseFactory:
    def __init__(self, bean: str) -> None:
        self.bean = bean
        self.store = Parser(bean).acnts()
        self.__refresh_builder()

        self.classifier = pipeline("zero-shot-classification",
                                   model="facebook/bart-large-mnli",
                                   device="mps")

        self.CHANGE_FROM_ACNT = "from"
        self.CHANGE_EXPN_ACNT = "expense"
        self.CHANGE_AMNT = "amount"
        self.CHANGE_PAYEE = "payee"
        self.CHANGE_DESC = "desc"
        self.CHANGE_SHARE = "share"
        self.WRITE = "write"
        self.CHANGE = "change"

    def _parse_change_cmd(self, cmd: str):
        words = cmd.strip().split()
        cmd, arg = words[0], " ".join(words[1:])

        match cmd:
            case self.CHANGE_AMNT:
                amnt = util.extract_first_float(arg)
                self.builder = self.builder.with_amnt(amnt)

            case self.CHANGE_PAYEE:
                self.builder = self.builder.with_payee(arg)

            case self.CHANGE_DESC:
                self.builder = self.builder.with_desc(arg)

            case self.CHANGE_EXPN_ACNT:
                acnt = self.__infer_account(arg, AccountType.EXPENSE)
                self.builder = self.builder.with_expn_acnt(acnt)

            case self.CHANGE_FROM_ACNT:
                acnt = self.__infer_account(arg)
                self.builder = self.builder.with_from_acnt(acnt)

            case self.CHANGE_SHARE:
                contact = self.__infer_contact(arg)
                self.builder = self.builder.with_shared(contact.name)

    def _parse_english(self, text: str):
        self.builder = self.builder.with_amnt(util.extract_first_float(text))\
            .with_desc(text.strip())\
            .with_expn_acnt(self.__infer_account(text, AccountType.EXPENSE))\
            .with_from_acnt(self.__infer_account(text, AccountType.ASSET))\
            .with_shared(self.__infer_share(text))

    def __infer_account(self, text: str, typ: AccountType | None = None):
        choices = self.store.all_of_type(typ) if typ else self.store.all()
        return self.__classify(text, choices)

    def __infer_contact(self, text: str):
        choices = self.store.contacts()
        return self.__classify(text, choices)

    def __infer_share(self, text: str):
        choices = self.store.contacts()
        return self.__classify_with_other(text, choices)

    def __classify(self, text: str, choices):
        labels = {str(x): x for x in choices}
        ret = self.classifier(text, list(labels.keys()))
        return labels[ret['labels'][0]]

    def __classify_with_other(self, text: str, choices, threshold=.7):
        labels = {str(x): x for x in choices}
        ret = self.classifier(text, list(labels.keys()) + ['other'])
        ret = ret['labels'][0] if ret['scores'][0] > threshold else None
        if ret != 'other' and ret is not None:
            return labels[ret]
        return None

    def __refresh_builder(self):
        self.builder = SimpleExpenseBuilder()

    def _write(self):
        try:
            with open(self.bean, '+a') as f:
                ret = self.builder.try_build()
                if ret:
                    f.write(ret.as_str() + '\n\n')
                    self.__refresh_builder()
        except BaseException:
            print("warning: writing failed")

    def show(self):
        self.builder.show()

    def _parse_cmd(self, text: str):
        words = text.split()
        cmd, args = words[0], " ".join(words[1:])

        match cmd:
            case self.WRITE:
                self._write()
            case self.CHANGE:
                self._parse_change_cmd(args)
            case _:
                self._parse_english(text)

    def interact(self):
        while True:
            text = input("> ")
            self._parse_cmd(text)
            self.show()
            print("looks good?")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    inter = InteractiveSimpleExpenseFactory(args.filename)
    inter.interact()
