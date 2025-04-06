import logging
from typing import Optional
from fastapi import Query, Depends
from fastapi.responses import StreamingResponse

from src.services.user_service import get_current_user
from src.db.models import User
from src.core.database import get_db
from src.services.expense.expense_manager import ExpenseManager
from .schemas import ExpenseCreate, ExpenseUpdate


logger = logging.getLogger(__name__)


class ExpenseHandler:
    def __init__(self, expenses_manager: ExpenseManager):
        self.expenses_manager = expenses_manager

    def get_expense_by_id(
        self,
        expense_id: int,
        user: User = Depends(get_current_user),
        session=Depends(get_db),
    ):
        return self.expenses_manager.get_expense(
            session=session,
            user_id=user.id,
            expense_id=expense_id,
        )

    def get_expenses_excel_report(
        self,
        user: User = Depends(get_current_user),
        start_date: str = Query(..., description="Start date for the report"),
        end_date: str = Query(..., description="End date for the report"),
        session=Depends(get_db),
    ):

        expenses_report = self.expenses_manager.get_expenses_report(
            user_id=user.id,
            start_date=start_date,
            end_date=end_date,
            format_report="excel",
            session=session,
        )
        headers = {"Content-Disposition": "attachment; filename=expenses_report.xlsx"}

        return StreamingResponse(
            content=expenses_report,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers,
        )

    def create_expense(
        self,
        expense: ExpenseCreate,
        user: User = Depends(get_current_user),
        session=Depends(get_db),
    ):
        return self.expenses_manager.create_expense(
            user_id=user.id, expense=expense, session=session
        )

    def update_expense(
        self, expense_id: int, expense: ExpenseUpdate, session=Depends(get_db)
    ):
        return self.expenses_manager.update_expense(
            expense_id=expense_id, expense_update=expense, session=session
        )

    def delete_expense(self, expense_id: int, session=Depends(get_db)):
        self.expenses_manager.delete_expense(expense_id=expense_id, session=session)
