from src.db.repository import CRUDRepository
from src.db.models import Expense
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from typing import List
from datetime import date


class ExpenseRepository:
    """
    This class manages expenses for a user.
    It provides methods to create, read, update, and delete expenses.
    """

    def get_expenses(
        self, user_id: int, start_date: date, end_date: date, session: Session
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
        user_id: int,
        name: str,
        uah_amount: float,
        usd_amount: float,
        date: date,
        session: Session,
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

    def update_expense(self, expense_id: int, session: Session, **kwargs) -> bool:
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

    def delete_expense(self, expense_id: int, session: Session) -> bool:
        """
        Delete an expense.
        """
        query = delete(Expense).where(
            Expense.id == expense_id,
        )

        return CRUDRepository.delete(query, session)
