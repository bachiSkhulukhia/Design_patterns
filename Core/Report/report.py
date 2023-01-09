from dataclasses import dataclass
from typing import Protocol, List

from Core.Items.Item import IItem, ItemWithAmount
from Core.Persistance.Database.database import IItemDatabase
from Core.Persistance.Database.database_receipts import IReceiptDatabase
from Core.Receipt.Receipt import IReceiptObject, ReceiptStatus


@dataclass
class Report:
    items: List[ItemWithAmount]
    closed_receipts_number: int
    revenue: float


class IReportable(Protocol):
    def get_x_report(self) -> Report:
        pass

@dataclass
class ReportMaker(IReportable):
    sold_items: IItemDatabase
    receipts: IReceiptDatabase
    def get_x_report(self) -> Report:
        items: List[ItemWithAmount] = self.sold_items.get_all_items()
        closed_receipts_number = self.receipts.receipts_count(status=1)
        revenue = self._count_revenue(items=items)

        return Report(items=items, closed_receipts_number=closed_receipts_number, revenue=revenue)

    def _count_revenue(self, items: List[ItemWithAmount]) -> float:
        amount: float = 0.0
        if items is None:
            return amount
        for item in items:
            amount += (item.item.get_price() * item.quantity)
        return amount