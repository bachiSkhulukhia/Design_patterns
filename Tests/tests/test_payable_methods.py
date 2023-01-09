import unittest

from Core.Logger.logger import Logger
from Core.Payment.Payment import Cash, Card


class TestPayableMethods(unittest.TestCase):
    def test_cash(self):
        cash = Cash(amount=100, logger=Logger(None))
        self.assertTrue(cash.pay(25))
        self.assertTrue(cash.pay(75))
        self.assertFalse(cash.pay(1))

    def test_card(self):
        card = Card(amount=100, logger=Logger(None))
        self.assertTrue(card.pay(25))
        self.assertTrue(card.pay(75))
        self.assertFalse(card.pay(1))


if __name__ == "__main__":
    unittest.main()
