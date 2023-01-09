import sqlite3
from dataclasses import dataclass, field
from enum import Enum
from sqlite3 import Connection, Cursor
from typing import Dict, List, Protocol

from Core.Items.Item import IItem, ItemWithAmount, Item
from Core.MainProtocols.MainProtocols import IRandomCodable
from Core.Persistance.Database.Queries.database_create_queries import *
from Core.Persistance.Database.Queries.database_delete_queries import *
from Core.Persistance.Database.Queries.database_insert_queries import *
from Core.Persistance.Database.Queries.database_insert_test import *
from Core.Persistance.Database.Queries.database_select_queries import *
from Core.Persistance.Database.Queries.database_update_queries import *
from Core.Persistance.Database.database_consts import *
from Core.Receipt.Receipt import IReceipt, IReceiptObject


def get_connection() -> Connection:
    return sqlite3.connect(STORE_DATABASE_NAME, timeout=10)


def execute(conn: Connection, queries: List[str]):
    cursor = conn.cursor()

    for query in queries:
        cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()


def commit_and_close(con: Connection, cur: Cursor):
    con.commit()
    cur.close()
    con.close()


def add_starting_tables_in_database():
    conn: Connection = get_connection()
    queries: List[str] = [
        CREATE_ITEMS_TABLE,
        CREATE_SOLD_ITEMS_TABLE,
        CREATE_RECEIPTS_TABLE,
        CREATE_RECEIPTS_ITEMS
    ]

    execute(conn=conn, queries=queries)


def add_test_items():
    conn: Connection = get_connection()
    queries: List[str] = [
        INSERT_ITEM_TEST_1,
        INSERT_ITEM_TEST_2,
        INSERT_ITEM_TEST_3,
        INSERT_ITEM_TEST_4,
        INSERT_SOLD_ITEM_TEST_1,
        INSERT_SOLD_ITEM_TEST_2,
        INSERT_SOLD_ITEM_TEST_3,
        INSERT_SOLD_ITEM_TEST_4

    ]

    execute(conn=conn, queries=queries)


if __name__ == "__main__":
    add_starting_tables_in_database()
    # add_test_items()


# class ItemRandomCodeGenerator(IRandomCodable):
#     def get_random_code(self) -> str:
#         pass

class IItemDatabase(Protocol):
    def add_items(self, item: IItem, quantity: float) -> bool:
        pass

    def remove_items(self, item: IItem, quantity: float) -> bool:
        pass

    def get_all_items(self) -> [ItemWithAmount]:
        pass


class SQLiteItemDatabase(IItemDatabase):
    def add_items(self, item: IItem, quantity: float) -> bool:
        con = get_connection()
        cur = con.cursor()

        cur.execute(SELECT_ITEM_ID_WITH_CODE, [item.get_code()])
        ids = cur.fetchall()
        if len(ids) == 0:
            cur.execute(INSERT_ITEM, [item.get_code(), item.get_description(), item.get_price(), quantity])
        else:
            cur.execute(UPDATE_INCREASE_EXISTING_ITEM_QUANTITY_BY_CODE, [quantity, item.get_code()])
        con.commit()
        cur.close()
        con.close()
        return True

    def remove_items(self, item: IItem, quantity: float) -> bool:
        con = get_connection()
        cur = con.cursor()

        cur.execute(SELECT_ITEM_ID_WITH_CODE, [item.get_code()])
        quantities = cur.fetchall()
        if len(quantities) == 0:
            if quantities[0] > quantity:
                cur.execute(DECREASE_EXISTING_ITEM_QUANTITY_BY_CODE, [quantity, item.get_code()])
            else:
                commit_and_close(con=con, cur=cur)
                Exception("Cant remove so much item. have (" +
                          str(quantities[0]) +
                          "), Want to be removed (" + str(quantity) + ")")
                return False
        else:
            commit_and_close(con=con, cur=cur)
            return False
        commit_and_close(con=con, cur=cur)
        return True

    def get_all_items(self) -> [ItemWithAmount]:
        con = get_connection()
        cur = con.cursor()

        cur.execute(SELECT_ITEMS)
        commit_and_close(con=con, cur=cur)

        records = cur.fetchall()
        answer = []
        for row in records:
            answer.append(ItemWithAmount(item=Item(code=row[0],
                                                   description=row[1],
                                                   price=row[2]),
                                         quantity=row[3]))

        return answer


class SQLiteSoldItemDatabase(IItemDatabase):
    def add_items(self, item: IItem, quantity: float) -> bool:
        con = get_connection()
        cur = con.cursor()

        cur.execute(SELECT_SOLD_ITEM_ID_WITH_CODE, [item.get_code()])
        ids = cur.fetchall()
        if len(ids) == 0:
            cur.execute(INSERT_SOLD_ITEMS, [item.get_code(), item.get_description(), item.get_price(), quantity])
        else:
            cur.execute(INCREASE_EXISTING_SOLD_ITEM_QUANTITY_BY_CODE, [quantity, item.get_code()])
        con.commit()
        cur.close()
        con.close()
        return True

    def remove_items(self, item: IItem, quantity: float) -> bool:
        con = get_connection()
        cur = con.cursor()

        cur.execute(SELECT_SOLD_ITEM_ID_WITH_CODE, [item.get_code()])
        quantities = cur.fetchall()
        if len(quantities) == 0:
            if quantities[0] > quantity:
                cur.execute(DECREASE_EXISTING_SOLD_ITEM_QUANTITY_BY_CODE, [quantity, item.get_code()])
            else:
                commit_and_close(con=con, cur=cur)
                Exception("Cant remove so much item. have (" +
                          str(quantities[0]) +
                          "), Want to be removed (" + str(quantity) + ")")
                return False
        else:
            commit_and_close(con=con, cur=cur)
            return False
        commit_and_close(con=con, cur=cur)
        return True

    def get_all_items(self) -> [ItemWithAmount]:
        con = get_connection()
        cur = con.cursor()

        cur.execute(SELECT_SOLD_ITEMS)

        records = cur.fetchall()
        commit_and_close(con=con, cur=cur)

        answer = []
        for row in records:
            answer.append(ItemWithAmount(item=Item(code=row[0],
                                                   description=row[1],
                                                   price=row[2]),
                                         quantity=row[3]))

        return answer

@dataclass
class InMemoryItemsDataBase(IItemDatabase):
    items_with_amount: [ItemWithAmount] = field(default_factory=List)
    def add_items(self, item: IItem, quantity: float) -> bool:
        self.items_with_amount.append(ItemWithAmount(item=item,quantity=quantity))
        return True

    def remove_items(self, item: IItem, quantity: float) -> bool:
        items_only = map(lambda x: x.item,self.items_with_amount)
        if item in items_only:
            curr_item = list(filter(lambda x: x.item == item,self.items_with_amount))[0]
            if curr_item.quantity > quantity:
                index = self.items_with_amount.index(curr_item)
                new_curr_item = ItemWithAmount(item=curr_item.item,
                                               quantity=curr_item-quantity)
                self.items_with_amount[index] = new_curr_item
            else:
                return False
        else:
            return False

    def get_all_items(self) -> [ItemWithAmount] :
        return self.items_with_amount
