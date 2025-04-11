from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from datetime import date

from src.db.models import Expense
from src.services.report.report_factory import ReportFactory
from src.services.expense.expense_service import ExpenseService
from src.schemas.expense import schema, dto


class ExpenseController:
    """
    This class manages expenses for a user.
    It provides methods to create, read, update, and delete expenses.
    """

    def __init__(self, expenses_service: ExpenseService, report: ReportFactory):
        self.expenses_service = expenses_service
        self.report = report

    def get_expense_by_id(self, session: Session, expense_id: int) -> Expense:
        expense = self.expenses_service.get_expense_by_id(session, expense_id)
        if not expense:
            raise HTTPException(404, f"Стаття витрат із ID {expense_id} не знайдена.")
        return expense

    def get_expenses_report(
        self,
        session: Session,
        user_id: int,
        start_date: Optional[date],
        end_date: Optional[date],
        all_expenses: Optional[bool],
        format_report: str,
    ):
        """
        Get expenses report for a given date range.
        """
        expense_params = dto.GetExpenseParams(
            user_id, start_date, end_date, all_expenses, format_report
        )
        expenses = self.expenses_service.get_expenses(session, expense_params)
        if not expenses:
            raise HTTPException(404, "Ми не змогли знайти ваші витрати.")

        return self.report.get_report_generator(format_report).generate_report(expenses)

    def create_expense(
        self, user_id: int, expense: schema.ExpenseCreate, session: Session
    ):
        """
        Create a new expense.
        """

        expense = self.expenses_service.create_expense(session, user_id, expense)
        if not expense:
            raise HTTPException(
                422,
                "Щось пішло не так під час створення статті витрат. Спробуйте пізніше.",
            )
        return expense

    def update_expense(
        self, expense_id: int, expense_update: schema.ExpenseUpdate, session: Session
    ):
        """
        Update an expense.
        """
        result = self.expenses_service.update_expense(
            session, expense_id, expense_update
        )
        if not result:
            raise HTTPException(422, "Не вдалося оновити ваші дані. Спробуйте пізніше.")

    def delete_expense(self, expense_id: int, session: Session):
        """
        Delete an expense.
        """
        result = self.expenses_service.delete_expense(session, expense_id)
        if not result:
            raise HTTPException(
                422, "Сталася помилка під час видалення. Спробуйте пізніше."
            )
