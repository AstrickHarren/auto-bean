import datetime
from enum import Enum
from typing import *


class Account:
    def __init__(self, name: str, parent=None) -> None:
        self.parent: Account = parent
        self.name = name

    def ancestors(self) -> List["Account"]:
        if self.parent != None:
            return self.parent.ancestors() + [self.parent]
        return []

    def root(self):
        if len(self.ancestors()) > 0:
            return self.ancestors()[0]
        return self

    def is_ancestor_of(self, other) -> bool:
        if self in other.ancestors():
            return True
        return False

    def as_str(self) -> str:
        return ":".join(
            map(
                lambda x: x.name,
                self.ancestors() + [self]
            )
        )

    def __str__(self) -> str:
        return self.as_str()

    def __eq__(self, __value: object) -> bool:
        return __value is not None and self.as_str() == __value.as_bean_str()

    def __hash__(self) -> int:
        return hash(self.as_str())


class AccountType(Enum):
    INCOME = Account("Income")
    EXPENSE = Account("Expenses")
    LIABILITY = Account("Liabilities")
    EQUITY = Account("Equity")
    ASSET = Account("Assets")


class AccountStore:
    def __init__(self, acnts: List[Account]) -> None:
        self._acnts = set(acnts)
        self._roots = set()
        self._leafs = set()

        self._process_roots()
        self._process_leafs()

    def all(self):
        return self._acnts

    def roots(self):
        return self._roots

    def leafs(self):
        return self._leafs

    def leafs_of(self, acnt: Account):
        ret = set()
        for other in self.all():
            if acnt.is_ancestor_of(other):
                ret.add(other)
        return ret.intersection(self.leafs())

    def all_of_type(self, type: AccountType):
        return self.leafs_of(type.value)

    def _process_roots(self):
        for acnt in self._acnts:
            self._roots.add(acnt.root())

    def _process_leafs(self):
        non_leafs = set()
        for acnt in self._acnts:
            for acnt in acnt.ancestors():
                non_leafs.add(acnt)
        self._leafs = self._acnts.difference(non_leafs)


class Currency:
    def __init__(self, name: str) -> None:
        self.name = name


class Leg:
    def __init__(self, acnt: Account, amnt: float) -> None:
        self.acnt = acnt
        self.amnt = amnt


class Transaction:
    def __init__(self, legs: List[Leg], date: datetime.date = datetime.date.today()) -> None:
        self.date = date
        self.legs = legs

    def verify(self) -> bool:
        return sum(map(lambda leg: leg.amnt, self.legs)) == 0


class Contact:
    def __init__(self, name: str, lia_acnt: Account) -> None:
        self.name = name
        self.lib_acnt = lia_acnt
