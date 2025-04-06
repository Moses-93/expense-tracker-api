from src.services.report.report_manager import ReportManager
from .expense_repository import ExpenseRepository
from src.services.exchange_rate_service import ExchangeRateService
from sqlalchemy.orm import Session
from datetime import date


class ExpenseService:

    def __init__(self, expenses_repository: ExpenseRepository):
        self.expenses_repository = expenses_repository

    def format_date_from_string(self, date_string: str) -> date:
        """
        Convert a string to a date object.
        """
        return date.fromisoformat(date_string)

    def create_expense(
        self, user_id: int, name: str, uah_amount: float, date: str, session: Session
    ):
        """
        Create a new expense.
        """
        exchange_rate = ExchangeRateService.get_usd_exchange_rate()
        usd_amount = uah_amount / exchange_rate
        return self.expenses_repository.create_expense(
            user_id, name, uah_amount, usd_amount, date, session
        )

    def get_expenses(self, user_id: int, session: Session):
        """
        Get expenses for a given date range.
        """

        return self.expenses_repository.get_expenses_by_user_id(user_id, session)

    def get_expenses_report(
        self,
        user_id: int,
        start_date: str,
        end_date: str,
        format_report: str,
        session: Session,
    ):
        """
        Get expenses report for a given date range.
        """
        start_date = self.format_date_from_string(start_date)
        end_date = self.format_date_from_string(end_date)

        expenses = self.expenses_repository.get_expenses(
            user_id, start_date, end_date, session
        )

        if not expenses:
            return {"message": "No expenses found for the given date range."}

        report_generator = ReportManager.get_report_generator(format_report)
        return report_generator.generate_report(expenses)

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
