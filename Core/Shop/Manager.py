from dataclasses import dataclass
from typing import Protocol, List

from Core.Receipt.Receipt import IReceipt
from Core.Report.report import IReportable, Report


class IManager(Protocol):
    def get_report(self,receipts: List[IReceipt]) -> Report:
        pass


@dataclass
class Manager:
    report_maker: IReportable

    def get_report(self) -> Report:
        return self.report_maker.get_x_report()
