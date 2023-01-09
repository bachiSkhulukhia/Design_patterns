from dataclasses import dataclass, field
from typing import Protocol, List

from Core.MainProtocols.MainProtocols import IRandomCodable
from Core.Persistance.Database.Queries.database_delete_queries import *
from Core.Persistance.Database.Queries.database_insert_queries import *
from Core.Persistance.Database.Queries.database_select_queries import *
from Core.Persistance.Database.Queries.database_update_queries import *
from Core.Persistance.Database.database import get_connection
from Core.Receipt.Receipt import IReceipt, IReceiptObject, ReceiptStatus


class ReceiptRandomCodeGenerator(IRandomCodable):
    def get_random_code(self) -> str:
        pass

class IReceiptDatabase(Protocol):
    def add_receipt(self, receipt: IReceipt) -> int:
        pass

    def close_receipt(self, code: int):
        pass

    def receipts_count(self, status: int) -> int:
        pass


class IReceiptItemsDatabase(Protocol):
    def add_receipt_item(self,
                         item_code: int,
                         receipt_code: int,
                         price: float,
                         quantity: float):
        pass

    def item_types_count(self, receipt_code: int, item_code: int, ) -> int:
        pass


class ReceiptItemsDatabase(IReceiptItemsDatabase):
    def add_receipt_item(self,
                         item_code: int,
                         receipt_code: int,
                         price: float,
                         quantity: float):
        con = get_connection()
        cur = con.cursor()

        cur.execute(INSERT_RECEIPT_ITEMS, [receipt_code, item_code, price, quantity])

        con.commit()
        cur.close()
        con.close()

    def item_types_count(self, receipt_code: int, item_code: int) -> int:
        con = get_connection()
        cur = con.cursor()
        cur.execute(SELECT_RECEIPT_ITEM_COUNT_WITH_CODE, [item_code, receipt_code])
        count = cur.fetchone()
        con.commit()
        cur.close()
        con.close()
        return count


@dataclass
class SQLiteReceiptDatabaseFactory(IReceiptDatabase):
    receipt_item: IReceiptItemsDatabase
    def add_receipt(self,receipt: IReceipt) -> int:
        con = get_connection()
        cur = con.cursor()

        receipt_status = 1 if receipt.is_closed() else 0
        cur.execute(INSERT_RECEIPT, [receipt.get_code(), receipt_status])

        con.commit()
        cur.close()
        con.close()

        for item in receipt.get_items():
            self.receipt_item.add_receipt_item(item_code=item.get_item().get_code(),
                                               receipt_code=receipt.get_code(),
                                               price=item.get_item_price(),
                                               quantity=item.get_amount())

        return receipt.get_code()

    def close_receipt(self, code: int):
        con = get_connection()
        cur = con.cursor()

        cur.execute(UPDATE_CLOSED_STATUS_BY_CODE, [ReceiptStatus.CLOSED, code])

        con.commit()
        cur.close()
        con.close()
        #TODO: გაყიდვის კლასი უნდა მქონდეს და რომ გაყიდის კაროჩე ყველა ეგ ნივთი უნდა მოაკლდეს და გაყიდულებში გადავარდეს

    def receipts_count(self, status: int) -> int:
        con = get_connection()
        cur = con.cursor()
        cur.execute(SELECT_DISTINCT_RECEIPTS_COUNT_BY_STATUS,[status])
        count = cur.fetchone()
        con.commit()
        cur.close()
        con.close()
        return count

@dataclass
class InMemoryReceiptDatabase(IReceiptDatabase):
    open_receipts: List[IReceipt] = field(default_factory=list)
    closed_receipts: List[IReceipt] = field(default_factory=list)
    def add_receipt(self, receipt: IReceipt) -> int:
        coded_list = list(filter(lambda x: x.get_code() == receipt.get_code(), self.open_receipts))
        if len(coded_list) != 0:
            return -1
        else:
            self.open_receipts.append(receipt)
        return receipt.get_code()

    def close_receipt(self, code: int):
        coded_list = list(filter(lambda x: x.get_code() == code, self.open_receipts))
        if len(coded_list) == 0:
            return False
        else:
            curr_receipt = coded_list[0]
            self.closed_receipts.append(curr_receipt)
            self.open_receipts.remove(curr_receipt)
        return True


    def receipts_count(self, status: int) -> int:
        return len(self.closed_receipts) + len(self.open_receipts)
