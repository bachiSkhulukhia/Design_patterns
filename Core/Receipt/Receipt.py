from dataclasses import dataclass
from enum import Enum
from typing import List, Protocol

from Core.Items.Item import IPriceable, IItem, ICountable, IIdentifiable
from Core.MainProtocols.MainProtocols import IDescriptable


class ReceiptStatus(int, Enum):
    CLOSED: 0
    OPEN: 1

class IReceiptObject(IDescriptable, IPriceable, ICountable, Protocol):
    def get_item(self) -> IItem:
        pass

    def get_item_price(self) -> float:
        pass


@dataclass
class ReceiptObject(IReceiptObject):
    item: IItem
    amount: float

    def get_description(self):
        return self.item.get_description()

    def get_amount(self):
        return self.amount

    def get_price(self) -> float:
        return self.item.get_price() * self.amount

    def get_item(self) -> IItem:
        return self.item

    def get_item_price(self) -> float:
        return self.item.get_price()


class IReceipt(IDescriptable, IIdentifiable, Protocol):
    def get_code(self) -> int:
        pass

    def get_items(self) -> List[IReceiptObject]:
        pass

    def get_total_amount(self) -> float:
        pass

    def is_closed(self) -> bool:
        pass

    def close(self):
        pass


@dataclass
class Receipt(IReceipt):
    is_open: bool
    code: int
    items: List[IReceiptObject]

    def get_code(self) -> int:
        return self.code

    def get_description(self) -> str:
        description = "Code    "
        description += "Description    "
        description += "Amount    "
        description += "Price    "
        description += "Total Price    "
        description += "\n"
        for item in self.items:
            description += str(item.get_item().get_code()) + "    "
            description += item.get_description() + "    "
            description += str(item.get_amount()) + "    "
            description += str(item.get_item_price()) + "    "
            description += str(item.get_price()) + "    "
            description += "\n"
        description += "Overall Price : " + str(self.get_total_amount())
        return description

    def get_total_amount(self) -> float:
        price = 0.0
        for item in self.items:
            price += item.get_price()
        return price

    def get_items(self) -> List[IReceiptObject]:
        return self.items

    def is_closed(self) -> bool:
        return not self.is_closed

    def close(self):
        self.is_open = False
