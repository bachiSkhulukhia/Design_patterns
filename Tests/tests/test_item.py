import unittest

from Core.Items.Item import Item


class TestItem(unittest.TestCase):
    def test_item_get_price(self):
        item = Item(code=1,description="MEAT", price=4)
        self.assertEqual(item.get_price(), 4)

    def test_item_get_description(self):
        item = Item(code=1,description="MEAT", price=4)
        self.assertEqual(item.get_description(), "MEAT")

    def test_item_get_code(self):
        item = Item(code=1,description="MEAT", price=4)
        self.assertEqual(item.get_code(), 1)


if __name__ == "__main__":
    unittest.main()
