from sqlalchemy.orm import Session

from src.services.expenses.expense_service import ExpenseService
from src.api.expenses.schemas import ExpenseCreate, ExpenseUpdate


class ExpenseManager:
    """
    This class manages expenses for a user.
    It provides methods to create, read, update, and delete expenses.
    """
    def __init__(self, expenses_service: ExpenseService):
        self.expenses_service = expenses_service

    def get_expenses(self, user_id: int, session: Session):
        return self.expenses_service.get_expenses(user_id, session)

    def get_expenses_report(
            self, 
            user_id: int, 
            start_date: str, 
            end_date: str, 
            format_report: str, 
            session: Session
            ):
        """
        Get expenses report for a given date range.
        """
        return self.expenses_service.get_expenses_report(
            user_id, start_date, end_date, format_report, session
        )
    
    def create_expense(self, user_id: int, expense: ExpenseCreate, session: Session):
        """
        Create a new expense.
        """

        return self.expenses_service.create_expense(
            user_id, 
            expense.name,
            expense.amount, 
            expense.date, 
            session
        )
        
    
    def update_expense(self, expense_id: int, expense_update: ExpenseUpdate, session: Session):
        """
        Update an expense.
        """
        # Convert the date string to a date object
        updating_expense = expense_update.model_dump(exclude_unset=True)
        return self.expenses_service.update_expense(
            expense_id, session, **updating_expense
        )
    
    def delete_expense(self, expense_id: int, session: Session):
        """
        Delete an expense.
        """
        return self.expenses_service.delete_expense(
            expense_id, session
        )