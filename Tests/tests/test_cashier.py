import unittest

from Core.Customer.Customer import Customer
from Core.Items.Item import ItemWithAmount, Item
from Core.MainProtocols.MainProtocols import IRandomCodable
from Core.Payment.Payment import Cash
from Core.Persistance.Database.database_receipts import InMemoryReceiptDatabase
from Core.Shop.Cashier import Cashier

class TestCodableFive(IRandomCodable):
    def get_random_code(self) -> int:
        return 5

class TestCashier(unittest.TestCase):
    cashier: Cashier

    def setUp(self):
        item1: ItemWithAmount = ItemWithAmount(item=Item(2, "meat", 10),
                                               quantity=3)
        item2: ItemWithAmount = ItemWithAmount(item=Item(4, "apple", 20),
                                               quantity=10)

        payment_method = Cash(amount=800)
        customer = Customer(payment_method=payment_method,
                                 my_items=[item1, item2])

        self.cashier = Cashier(customer=customer,
                               receipt_database=InMemoryReceiptDatabase([]),
                               receipt_random_code_generator=TestCodableFive())

    def test_code(self):
        self.assertEqual(self.cashier.open_receipt(),5)

    def test_is_closed(self):
        self.cashier.open_receipt()
        self.cashier.close_receipt()
        self.assertEqual(self.cashier.receipt_database.receipts_count(1), 1)


if __name__ == "__main__":
    unittest.main()
