from typing import Optional
from .expense_repository import ExpenseRepository
from src.services.exchange_rate_service import ExchangeRateService
from sqlalchemy.orm import Session
from datetime import date


class ExpenseService:

    def __init__(
        self,
        expenses_repository: ExpenseRepository,
        exchange_service: ExchangeRateService,
    ):
        self.expenses_repository = expenses_repository
        self.exchange_service = exchange_service

    def create_expense(
        self, user_id: int, name: str, uah_amount: float, date: str, session: Session
    ):
        """
        Create a new expense.
        """
        usd_amount = self.exchange_service.convert_uah_to_usd(expense.amount)
        return self.expenses_repository.create_expense(
            user_id, name, uah_amount, usd_amount, date, session
        )

    def get_expenses(
        self,
        session: Session,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        all_expenses: Optional[bool] = False,
        expense_id: Optional[int] = None,
    ):
        """
        Get expenses for a given date range.
        """
        if all_expenses:
            return self.expenses_repository.get_expense_with_filter(
                session, user_id=user_id
            )
        elif expense_id:
            return self.expenses_repository.get_expense_with_filter(
                session,
                single=True,
                user_id=user_id,
                id=expense_id,
            )
        return self.expenses_repository.get_expenses(
            user_id, start_date, end_date, session
        )

    def update_expense(self, expense_id: int, session: Session, **kwargs):
        """
        Update an expense.
        """
        return self.expenses_repository.update_expense(expense_id, session, **kwargs)

    def delete_expense(self, expense_id: int, session: Session):
        """
        Delete an expense.
        """
        return self.expenses_repository.delete_expense(expense_id, session)
