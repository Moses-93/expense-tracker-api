from src.db.repository import CRUDRepository
from src.db.models import Expense
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from typing import List, Optional, Union
from datetime import date


class ExpenseRepository:
    """
    This class manages expenses for a user.
    It provides methods to create, read, update, and delete expenses.
    """

    def get_by_filter(
        self, session: Session, single: Optional[bool] = False, **kwargs
    ) -> Union[List[Expense], Expense]:
        return CRUDRepository.read(select(Expense).filter_by(**kwargs), session, single)

    def get_by_date_range(
        self, session: Session, user_id: int, start_date: date, end_date: date
    ) -> List[Expense]:
        """
        Get expenses for a given date range.
        """
        query = select(Expense).where(
            Expense.user_id == user_id,
            Expense.date >= start_date,
            Expense.date <= end_date,
        )

        return CRUDRepository.read(query, session)

    def create_expense(
        self,
        session: Session,
        user_id: int,
        name: str,
        uah_amount: float,
        usd_amount: float,
        date: date,
    ) -> Expense:
        """
        Create a new expense.
        """
        expense = Expense(
            user_id=user_id,
            name=name,
            uah_amount=uah_amount,
            usd_amount=usd_amount,
            date=date,
        )

        return CRUDRepository.create(expense, session)

    def update_expense(self, session: Session, expense_id: int, **kwargs) -> bool:
        """
        Update an expense.
        """
        query = (
            update(Expense)
            .where(
                Expense.id == expense_id,
            )
            .values(**kwargs)
        )

        return CRUDRepository.update(query, session)

    def delete_expense(self, session: Session, expense_id: int) -> bool:
        """
        Delete an expense.
        """
        query = delete(Expense).where(
            Expense.id == expense_id,
        )

        return CRUDRepository.delete(query, session)
