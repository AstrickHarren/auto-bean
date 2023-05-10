import datetime
import unittest

import auto_bean


class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.expense = auto_bean.Account("expense")

        self.food = auto_bean.Account("food", self.expense)
        self.life = auto_bean.Account("life", self.expense)

        self.dine = auto_bean.Account("dine", self.food)
        self.usd = auto_bean.Currency("usd")
        self.good_trans = auto_bean.Transaction(
            [
                auto_bean.Leg(self.food, -100, self.usd),
                auto_bean.Leg(self.life, 100, self.usd),
            ],
            desc="sport clothes",
            tags=[auto_bean.Tag("share-YYX")]
        )
        self.bad_trans = auto_bean.Transaction([
            auto_bean.Leg(self.food, -100, self.usd),
            auto_bean.Leg(self.life, 120, self.usd),
        ])

    def test_account(self):
        self.assertEqual(
            self.expense.root(),
            self.expense
        )

        self.assertEqual(
            self.life.root(),
            self.expense
        )

        self.assertEqual(
            self.dine.as_str(),
            "expense:food:dine"
        )

    def test_transaction_verify(self):
        self.assertTrue(self.good_trans.verify())
        self.assertFalse(self.bad_trans.verify())

    def test_transaction_display(self):
        print(self.good_trans.as_str())


if __name__ == "__main__":
    # unittest.main()
    test = TestStringMethods()
    test.setUp()
    test.test_transaction_display()
