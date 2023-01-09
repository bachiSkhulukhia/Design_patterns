from dataclasses import dataclass
from typing import Protocol

from Core.Customer.Customer import ICustomer
from Core.MainProtocols.MainProtocols import IRandomCodable
from Core.Persistance.Database.database_receipts import IReceiptDatabase
from Core.Receipt.Receipt import IReceiptObject, ReceiptObject, Receipt, IReceipt


class ICashier(Protocol):
    def open_receipt(self) -> int:
        pass

    def close_receipt(self):
        pass


@dataclass
class Cashier(ICashier):
    customer: ICustomer
    receipt_database: IReceiptDatabase
    receipt_random_code_generator: IRandomCodable
    current_opened_code = None

    def open_receipt(self) -> str:
        receipt_objects: [IReceiptObject] = []
        for item_with_amount in self.customer.get_items_with_quantity():
            receipt_objects.append(ReceiptObject(item=item_with_amount.item, amount=item_with_amount.quantity))
        code = self.receipt_random_code_generator.get_random_code()
        self.current_opened_code = self.receipt_database.add_receipt(
            Receipt(is_open=True, code=code, items=receipt_objects)
        )
        return code



    def close_receipt(self):
        self.receipt_database.close_receipt(code=self.current_opened_code)
