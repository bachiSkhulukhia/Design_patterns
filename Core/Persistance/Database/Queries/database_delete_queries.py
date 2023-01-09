DELETE_OPEN_RECEIPT_ITEMS = """
DELETE FROM open_receipts_items
WHERE CODE = ?;
"""

DELETE_CLOSED_RECEIPT_ITEMS = """
DELETE FROM closed_receipts_items
WHERE CODE = ?;
"""

