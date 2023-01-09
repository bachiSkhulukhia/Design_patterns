from dataclasses import dataclass
from typing import Protocol, List

from Core.MainProtocols.MainProtocols import IDescriptable


class ICountable(Protocol):
    def get_amount(self) -> float:
        pass


class IIdentifiable(Protocol):
    def get_code(self) -> int:
        pass


class IPriceable(Protocol):
    def get_price(self) -> float:
        pass


class IItem(IIdentifiable, IDescriptable, IPriceable, Protocol):
    def __hash__(self):
        pass

    def __eq__(self, other):
        pass


class IBatchable(Protocol):
    def get_item(self) -> IItem:
        pass


@dataclass
class Item(IItem):
    code: int
    description: str
    price: float

    def __hash__(self):
        return hash(self.code) + hash(self.description) + hash(self.price)

    def __eq__(self, other):
        return self.code == other.code

    def get_code(self) -> int:
        return self.code

    def get_price(self) -> float:
        return self.price

    def get_description(self) -> str:
        return self.description


class Batch(ICountable, IBatchable, IItem):
    code: int
    item: IItem
    amount: float
    price: float
    description: str

    def __init__(
        self,
        code: int,
        item: IItem,
        amount: float,
        price: float = None,
        description: str = None,
    ):
        self.code = code
        self.item = item
        self.amount = amount
        if price is None:
            self.price = self.item.get_price() * self.amount
        if description is None:
            self.description = str(self.amount)
            self.description += " " + self.item.get_description()

    def get_code(self) -> int:
        return self.code

    def get_item_amount(self) -> float:
        return self.amount

    def get_item(self) -> IItem:
        return self.item

    def get_price(self) -> float:
        return self.price

    def get_description(self) -> str:
        return self.description

@dataclass
class ItemWithAmount:
    item: IItem
    quantity: float

    def __eq__(self, other):
        return self.item == other.item


@dataclass
class Cart(IDescriptable):
    items: List[ItemWithAmount]

    def count_price(self) -> float:
        return sum(item_with_amount.item.get_price() for item_with_amount in self.items)

    def get_description(self) -> str:
        result = ""

        for item_with_amount in self.items:
            result += f"{item_with_amount.amount} {item_with_amount.item}"

        return result