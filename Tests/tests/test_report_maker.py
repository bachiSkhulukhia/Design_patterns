import unittest

from Core.Items.Item import Item, ItemWithAmount
from Core.Persistance.Database.database import InMemoryItemsDataBase
from Core.Persistance.Database.database_receipts import InMemoryReceiptDatabase
from Core.Receipt.Receipt import Receipt, ReceiptObject
from Core.Report.report import ReportMaker, Report
from Core.Shop.Manager import Manager


class TestReportMaker(unittest.TestCase):
    report_maker: ReportMaker
    def setUp(self):
        item1 = Item(2, "meat", 10)
        item2 = Item(1, "apple", 20)
        receiptsObject: ReceiptObject = ReceiptObject(item=item1, amount=3)
        sold_items = InMemoryItemsDataBase(items_with_amount=[ItemWithAmount(item=item2, quantity=10)])
        receipts = InMemoryReceiptDatabase(open_receipts=[Receipt(is_open=False,
                                                             code=1,
                                                             items=[receiptsObject])],
                                           closed_receipts=[])
        sold_items.add_items(item=item1, quantity=2)
        self.report_maker = ReportMaker(sold_items=sold_items,
                                        receipts=receipts)

    def test_report_maker_not_none(self):
        self.assertNotEqual(self.report_maker,None)

    def test_item_items_len(self):
        report: Report = self.report_maker.get_x_report()
        self.assertEqual(len(report.items),2)

    def test_item_receipts_number(self):
        report: Report = self.report_maker.get_x_report()
        self.assertEqual(report.closed_receipts_number,1)

    def test_revenue(self):
        report: Report = self.report_maker.get_x_report()
        self.assertEqual(report.revenue,220)

    def test_not_none(self):
        report: Report = self.report_maker.get_x_report()
        self.assertNotEqual(report,None)


if __name__ == "__main__":
    unittest.main()
