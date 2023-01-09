SELECT_ITEMS = """
select CODE,DESCRIPTION,PRICE,QUANTITY from items
"""

SELECT_SOLD_ITEMS = """
select CODE,DESCRIPTION,PRICE,QUANTITY from sold_items
"""

SELECT_SOLD_ITEM_ID_WITH_CODE = """
select ID from sold_items
where CODE = ?
"""

SELECT_ITEM_QUANTITY_WITH_CODE = """
select QUANTITY from items
where CODE = ?
"""

SELECT_ITEM_ID_WITH_CODE = """
select ID from items
where CODE = ?
"""

SELECT_RECEIPT_STATUS_BY_CODE = """
select STATUS from receipts
where CODE = ?
"""


SELECT_CLOSED_RECEIPTS_QUANTITY = """
SELECT COUNT(*) FROM receipts WHERE STATUS = 1;
"""


SELECT_GET_ID_WITH_CODE_FROM_RECEIPTS = """
select ID from receipts
where CODE = ?
"""


SELECT_RECEIPT_ITEM_COUNT_WITH_CODE = """
SELECT COUNT(*) FROM receipts_items where ITEM_CODE = ? AND RECEIPT_CODE = ?
"""

SELECT_DISTINCT_RECEIPTS_COUNT_BY_STATUS = """
SELECT COUNT(DISTINCT CODE) FROM receipts  WHERE STATUS = ?"""