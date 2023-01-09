from typing import Dict, Protocol

from Core.Items.Item import IItem


class IStoreItems(Protocol):
    def add_item(self, item: IItem, amount: float = 1) -> bool:
        pass

    def remove_item(self, item: IItem, amount: float = 1) -> bool:
        pass

    def has_item(self, item: IItem, amount: float = 1) -> bool:
        pass

    def get_items(self) -> Dict[IItem, float]:
        pass


class StoreItemsSqlLiteDataBase(IStoreItems):
    def add_item(self, item: IItem, amount: float = 1) -> bool:
        pass

    def remove_item(self, item: IItem, amount: float = 1) -> bool:
        pass

    def has_item(self, item: IItem, amount: float = 1) -> bool:
        pass

    def get_items(self) -> Dict[IItem, float]:
        pass


class StoreItemsLocal(IStoreItems):
    items: Dict[IItem, float]

    def add_item(self, item: IItem, amount: float = 1) -> bool:
        if amount < 1:
            return False

        if self.has_item(item=item):
            self.items[item] += amount
        else:
            self.items[item] = amount
        return True

    def remove_item(self, item: IItem, amount: float = 1) -> bool:
        if amount < 1:
            return False

        if self.has_item(item=item):
            self.items[item] -= amount
            return True
        else:
            return False

    def has_item(self, item: IItem, amount: float = 1) -> bool:
        if item.get_code() in map(lambda x: x.get_code(), self.items.keys()):
            return True
        return False

    def get_items(self) -> Dict[IItem, float]:
        return self.items
