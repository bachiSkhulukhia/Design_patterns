import unittest

from Core.Customer.Customer import Customer
from Core.Items.Item import ItemWithAmount, Item
from Core.Payment.Payment import Cash


class TestCustomer(unittest.TestCase):
    customer: Customer

    def setUp(self):
        item1: ItemWithAmount = ItemWithAmount(item=Item(2, "meat", 10),
                                              quantity=3)
        item2: ItemWithAmount = ItemWithAmount(item=Item(4, "apple", 20),
                                               quantity=10)

        payment_method = Cash(amount=800)
        self.customer = Customer(payment_method=payment_method,
                                 my_items=[item1,item2])

    def test_items_len(self):
        self.assertEqual(len(self.customer.get_items_with_quantity()),2)

    def test_items_add(self):
        self.customer.get_new_item(item=Item(9, "tro", 10),
                                              quantity=1)
        self.assertEqual(len(self.customer.get_items_with_quantity()),3)

    def test_items_remove(self):
        self.assertTrue(self.customer.pay_items())


if __name__ == "__main__":
    unittest.main()
