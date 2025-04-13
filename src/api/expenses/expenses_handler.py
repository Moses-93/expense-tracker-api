import logging
from typing import Optional
from fastapi import Query, Depends
from fastapi.responses import StreamingResponse
from datetime import date

from src.services.user_service import get_current_user
from src.db.models import User
from src.core.database import get_db
from src.services.expense.expense_controller import ExpenseController
from src.schemas.expense.schema import ExpenseCreate, ExpenseUpdate


logger = logging.getLogger(__name__)


class ExpenseHandler:
    def __init__(self, expense_controller: ExpenseController):
        self.expense_controller = expense_controller

    def get_expense_by_id(
        self,
        expense_id: int,
        session=Depends(get_db),
    ):
        return self.expense_controller.get_expense_by_id(
            session=session,
            expense_id=expense_id,
        )

    def get_expenses_excel_report(
        self,
        user: User = Depends(get_current_user),
        start_date: Optional[date] = Query(
            None, description="Start date for the report"
        ),
        end_date: Optional[date] = Query(None, description="End date for the report"),
        all_expenses: Optional[bool] = Query(
            None, description="Get all expenses if True"
        ),
        session=Depends(get_db),
    ):
        expenses_report = self.expense_controller.get_expenses_report(
            user_id=user.id,
            start_date=start_date,
            end_date=end_date,
            all_expenses=all_expenses,
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
        return self.expense_controller.create_expense(
            user_id=user.id, expense_schema=expense, session=session
        )

    def update_expense(
        self, expense_id: int, expense: ExpenseUpdate, session=Depends(get_db)
    ):
        self.expense_controller.update_expense(
            expense_id=expense_id, expense_update=expense, session=session
        )

    def delete_expense(self, expense_id: int, session=Depends(get_db)):
        self.expense_controller.delete_expense(expense_id=expense_id, session=session)
