from Core.Persistance.Database.Queries.database_select_queries import SELECT_ITEM_ID_WITH_CODE

INSERT_SOLD_ITEM = (
    """
insert into sold_items(ITEM_ID,QUANTITY, PRICE, TIME_SOLD)
values ("""
    + SELECT_ITEM_ID_WITH_CODE
    + """), ?, ?, DATETIME('now','localtime')
"""
)

INSERT_CLOSED_RECEIPT_ITEM = """
insert into closed_receipts_items (RECEIPT_ID,SOLD_ITEM_ID)
values (?, ?)"""

INSERT_ITEM = """
insert into items (CODE,DESCRIPTION,PRICE,QUANTITY)
values (?, ?, ?, ?, ?)"""

INSERT_SOLD_ITEMS = """
insert into sold_items (CODE,DESCRIPTION,PRICE,QUANTITY)
values (?, ?, ?, ?, ?)"""

INSERT_RECEIPT = """
insert into receipts (CODE,STATUS,TIME_CREATED)
values (?, ?, DATETIME('now', 'localtime'))"""

INSERT_OPEN_RECEIPT_ITEM = """
insert into open_receipts_items (RECEIPT_ID,ITEM_ID)
values (?, ?)"""

INSERT_ITEM_TEST = """
insert into items (CODE,DESCRIPTION,PRICE,QUANTITY)
values (1, 'APPLE',13.232, 311)"""


##########################

INSERT_RECEIPT_ITEMS = """
INSERT INTO receipts_items(RECEIPT_CODE,ITEM_CODE,PRICE,QUANTITY)
VALUES(?, ?, ?, ?)
"""























