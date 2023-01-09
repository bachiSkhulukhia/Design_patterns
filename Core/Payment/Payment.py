from dataclasses import dataclass
from typing import Protocol

from Core.Logger.logger import Logger


class IPayable(Protocol):
    def pay(self, amount: float) -> bool:
        pass


# class ICash(Protocol):
#     def get_currency(self) -> str:
#         pass
#
#
# class ICard(Protocol):
#     def get_info(self) -> str:
#         pass


@dataclass
class Cash(IPayable):#, ICash):
    amount: float
    # currency: str
    logger: Logger = Logger(next_logger=None)

    def pay(self, amount: float) -> bool:
        if amount > self.amount:
            self.logger.log(message="Failed to pay With cash!")
            return False
        else:
            self.amount -= amount
            self.logger.log(message="Paid with cash!")
            return True

    # def get_currency(self) -> str:
    #     return self.currency


@dataclass
class Card(IPayable):#, ICard):
    # code: str
    amount: float
    logger: Logger = Logger(next_logger=None)

    def pay(self, amount: float) -> bool:
        if amount > self.amount:
            self.logger.log(message="Failed to pay With card!")
            return False
        else:
            self.amount -= amount
            self.logger.log(message="Paid with card!")
            return True

    # def get_info(self) -> str:
    #     return self.code
