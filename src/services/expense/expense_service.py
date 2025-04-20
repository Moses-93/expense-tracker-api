from sqlalchemy.orm import Session

from src.services.exchange_rate_service import ExchangeRateService
from src.schemas.expense import schema, dto
from .expense_repository import ExpenseRepository


class ExpenseService:

    def __init__(
        self,
        expenses_repository: ExpenseRepository,
        exchange_service: ExchangeRateService,
    ):
        self.expenses_repository = expenses_repository
        self.exchange_service = exchange_service

    def create_expense(
        self, session: Session, user_id: int, expense: schema.ExpenseCreate
    ):
        """
        Create a new expense.
        """
        usd_amount = self.exchange_service.convert_uah_to_usd(expense.uah_amount)
        return self.expenses_repository.create_expense(
            session, user_id, expense.name, expense.uah_amount, usd_amount, expense.date
        )

    def get_expense_by_id(self, session: Session, expense_id: int):
        return self.expenses_repository.get_by_filter(session, True, id=expense_id)

    def get_expenses(self, session: Session, params: dto.GetExpenseParams):
        """
        Get expenses for a given date range.
        """
        if params.all_expenses:
            return self.expenses_repository.get_by_filter(
                session, user_id=params.user_id
            )
        return self.expenses_repository.get_by_date_range(
            session, params.user_id, params.start_date, params.end_date
        )

    def update_expense(
        self, session: Session, expense_id: int, expense: schema.ExpenseUpdate
    ):
        """
        Update an expense.
        """
        updated_data = expense.model_dump(exclude_unset=True)
        return self.expenses_repository.update_expense(
            session, expense_id, **updated_data
        )

    def delete_expense(self, session: Session, expense_id: int):
        """
        Delete an expense.
        """
        return self.expenses_repository.delete_expense(session, expense_id)
