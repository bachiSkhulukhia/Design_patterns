from dataclasses import dataclass
from typing import Dict, Protocol, List

from Core.Items.Item import IItem, ItemWithAmount
from Core.Payment.Payment import IPayable
from Core.Receipt.Receipt import IReceipt


class ICustomer(Protocol):
    # def pay_receipt(self, receipt: IReceipt) -> bool:
    #     pass

    def pay_items(self) -> bool:
        pass

    def get_new_item(self, item: IItem, quantity: float):
        pass

    def return_item(self, item: IItem, quantity: float):
        pass

    def get_items_with_quantity(self) -> List[ItemWithAmount]:
        pass



@dataclass
class Customer(ICustomer):
    payment_method: IPayable
    my_items: List[ItemWithAmount]

    def get_items_with_quantity(self) -> List[ItemWithAmount]:
        return self.my_items

    def get_new_item(self, item: IItem, quantity: float):
        item_with_amount = ItemWithAmount(item=item,quantity=quantity)
        if item_with_amount in self.my_items:
            index = self.my_items.index(item_with_amount)
            new_item = self.my_items[index]
            self.my_items.remove(new_item)
            new_item.quantity += quantity
            self.my_items.append(new_item.quantity)
        else:
            self.my_items.append(item_with_amount)

    def return_item(self, item: IItem, quantity: float):
        if item in self.my_items:
            index = self.my_items.index(item)
            new_item = self.my_items[index]
            self.my_items.remove(new_item)
            new_item.quantity -= quantity
            if new_item.quantity > 0:
                self.my_items.append(new_item.quantity)
        else:
            return

    #RECEIPT-ებით აღარ
    # def pay_receipt(self, receipt: IReceipt) -> bool:
    #     amount = receipt.get_total_amount()
    #     payed = self.payment_method.pay(amount=amount)
    #     if payed:
    #         receipt.close()
    #     return payed

    def pay_items(self) -> bool:
        amount = 0
        for pay_item in self.my_items:
            amount += pay_item.item.get_price() * pay_item.quantity
        return self.payment_method.pay(amount=amount)
