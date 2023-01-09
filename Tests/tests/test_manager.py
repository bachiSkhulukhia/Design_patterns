import unittest

from Core.Items.Item import Item, ItemWithAmount
from Core.Persistance.Database.database import InMemoryItemsDataBase
from Core.Persistance.Database.database_receipts import InMemoryReceiptDatabase
from Core.Receipt.Receipt import Receipt, ReceiptObject
from Core.Report.report import ReportMaker, Report
from Core.Shop.Manager import Manager


class TestManager(unittest.TestCase):
    def test_manager_has_report(self):
        item1=Item(2,"meat",10)
        item2=Item(1,"apple",20)
        sold_items = InMemoryItemsDataBase(items_with_amount=[ItemWithAmount(item=item2,quantity=22)])
        receipts = InMemoryReceiptDatabase()
        sold_items.add_items(item=item1,quantity=1)
        manager = Manager(report_maker=ReportMaker(sold_items=sold_items,
                                                   receipts=receipts))
        report:Report = manager.get_report()
        print(manager.get_report())
        self.assertNotEqual(report,None)


if __name__ == "__main__":
    unittest.main()
