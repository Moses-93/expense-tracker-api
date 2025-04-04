from abc import ABC, abstractmethod
from typing import Any


class ReportBase(ABC):

    @abstractmethod
    def generate_report(self) -> Any:
        pass