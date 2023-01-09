# from dataclasses import dataclass
# from random import randint
# from typing import List
#
# from Core.Items.Item import IItem
# from Core.Persistance.Database.database import IItemDatabase
# from Core.Shop.Cashier import Cashier
# from Core.Shop.Manager import IManager
#
#
# @dataclass
# class Shop:
#     cashiers: List[Cashier]
#     manager: IManager
#     items_database: IItemDatabase
#
#     def get_random_cashier(self) -> Cashier:
#         index = randint(0, len(self.cashiers) - 1)
#         return self.cashiers[index]
#
#     def get_manager(self) -> IManager:
#         return self.manager
#
#     def add_new_item_in_stock(self, item: IItem, quantity: int):
#         self.items_database.add_items(item=item, quantity=quantity)
