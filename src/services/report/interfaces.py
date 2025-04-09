from abc import ABC, abstractmethod
from typing import Any, List

from src.db.models import Expense


class ReportBase(ABC):

    @abstractmethod
    def generate_report(self, expenses: List[Expense]) -> Any:
        pass
