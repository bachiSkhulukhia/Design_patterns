from dataclasses import dataclass
from enum import Enum
from random import randint
from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from Core.Customer.Customer import ICustomer, Customer, ItemWithAmount
from Core.Items.Item import IItem, Item
from Core.MainProtocols.MainProtocols import IRandomCodable
from Core.Payment.Payment import IPayable, Cash, Card
from Core.Persistance.Database.database_receipts import SQLiteReceiptDatabaseFactory, ReceiptItemsDatabase
from Core.Shop.Cashier import Cashier

shop_api = APIRouter()


@dataclass
class RandomCode(IRandomCodable):
    def get_random_code(self) -> int:
        return randint(a=0,b=1920982)


class ItemBaseModel(BaseModel):
    code: int
    description: str
    price: float


class ItemObjectBaseModel(BaseModel):
    item: ItemBaseModel
    quantity: float


class PaymentTypeBaseModel(str, Enum):
    cash = "Cash"
    card = "Card"


class PaymentBaseModel(BaseModel):
    amount: float
    payment_type: PaymentTypeBaseModel


class CustomerBaseModel(BaseModel):
    items: List[ItemObjectBaseModel]
    payment_method: PaymentBaseModel


@shop_api.post("/shop/cashier/serve-client")
async def serve_client(client: CustomerBaseModel):
    my_items: List[ItemWithAmount] = list()
    for curr_item in client.items:
        my_items.append(ItemWithAmount(item=Item(code=curr_item.item.code,
                                                 description=curr_item.item.description,
                                                 price=curr_item.item.price),
                                       amount=curr_item.quantity))
    payment_method: IPayable
    if client.payment_method.payment_type == PaymentTypeBaseModel.cash:
        payment_method = Cash(amount=client.payment_method.amount)
    if client.payment_method.payment_type == PaymentTypeBaseModel.card:
        payment_method = Card(amount=client.payment_method.amount)

    customer = Customer(payment_method=payment_method,
                        my_items=my_items)

    receipt_item_factory = SQLiteReceiptDatabaseFactory(receipt_item=ReceiptItemsDatabase())

    cashier = Cashier(customer=customer,
                      receipt_database=receipt_item_factory,
                      receipt_random_code_generator=RandomCode()
                      )

    code = cashier.open_receipt()
    if customer.pay_items():
        return {"paid_receipt_code": code}
    return HTTPException(status_code=404,
                         detail="Payment is not proceed...")

# serve_client(client=CustomerBaseModel(items = [], payment_method = PaymentTypeBaseModel(amount = 412,
#                                                                                         payment_method)))