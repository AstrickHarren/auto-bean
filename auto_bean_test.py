import datetime
import unittest

import auto_bean


class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.expense = auto_bean.Account("expense")

        self.food = auto_bean.Account("food", self.expense)
        self.life = auto_bean.Account("life", self.expense)

        self.dine = auto_bean.Account("dine", self.food)

    def test_transaction_verify(self):
        good_trans = auto_bean.Transaction(
            [
                auto_bean.Leg(self.food, -100),
                auto_bean.Leg(self.life, 100),
            ]
        )
        bad_trans = auto_bean.Transaction([
            auto_bean.Leg(self.food, -100),
            auto_bean.Leg(self.life, 120),
        ])
        self.assertTrue(good_trans.verify())
        self.assertFalse(bad_trans.verify())

        self.assertEqual(
            self.dine.as_bean_str(),
            "expense:food:dine"
        )

        self.assertEqual(
            self.expense.root(),
            self.expense
        )

        self.assertEqual(
            self.life.root(),
            self.expense
        )


if __name__ == "__main__":
    unittest.main()
