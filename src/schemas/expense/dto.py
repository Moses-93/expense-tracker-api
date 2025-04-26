from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class GetExpenseParams:
    user_id: int
    start_date: Optional[date]
    end_date: Optional[date]
    all_expenses: Optional[bool]
    format: str
