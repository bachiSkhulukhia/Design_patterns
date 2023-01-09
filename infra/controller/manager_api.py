from fastapi import APIRouter
from pydantic import BaseModel

from Core.Persistance.Database.database import SQLiteSoldItemDatabase
from Core.Persistance.Database.database_receipts import SQLiteReceiptDatabaseFactory, ReceiptItemsDatabase
from Core.Report.report import ReportMaker
from Core.Shop.Manager import Manager

manager_api = APIRouter()

class ItemBaseModel(BaseModel):
    id: int
    code: str
    description: str
    price: float
    quantity: int



@manager_api.get("/store/manager/get-report")
def get_report():
    manager = Manager(report_maker=ReportMaker(sold_items=SQLiteSoldItemDatabase(),
                                               receipts=SQLiteReceiptDatabaseFactory(receipt_item=ReceiptItemsDatabase())))
    print(manager.get_report())
    return manager.get_report()