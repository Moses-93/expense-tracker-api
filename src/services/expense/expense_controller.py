import logging
from fastapi import HTTPException
from typing import List, Optional, Union
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import date

from src.db.models import Expense
from src.services.report.excel_report import ExcelReport
from src.services.expense.expense_service import ExpenseService
from src.schemas.expense import schema, dto


ERROR_MESSAGES = {
    "create_error": "Щось пішло не так під час створення статті витрат. Спробуйте пізніше.",
    "read_error": "Ми не змогли знайти ваші витрати.",
    "read_error_by_id": "Стаття витрат із ID {id} не знайдена.",
    "update_error": "Не вдалося оновити ваші дані.\nМожливо статті із ID {id} не існує. Спробуйте пізніше.",
    "delete_error": "Сталася помилка під час видалення. Можливо статті із ID {id} не існує.\n"
    "Перевірте ваші дані та спробуйте пізніше.",
}

logger = logging.getLogger(__name__)


class ExpenseController:
    """
    This class manages expenses for a user.
    It provides methods to create, read, update, and delete expenses.
    """

    def __init__(self, expenses_service: ExpenseService):
        self.expenses_service = expenses_service

    def get_expense_by_id(self, session: Session, expense_id: int) -> Expense:
        expense = self.expenses_service.get_expense_by_id(session, expense_id)
        if not expense:
            logger.warning(f"Error during receipt of expense by id: {expense_id}.")
            raise HTTPException(
                404, ERROR_MESSAGES["read_error_by_id"].format(id=expense_id)
            )
        return expense

    def get_expenses_report(
        self,
        session: Session,
        user_id: int,
        start_date: Optional[date],
        end_date: Optional[date],
        all_expenses: Optional[bool],
        format_report: str,
    ) -> Union[List[Expense], bytes]:
        """
        Get expenses report for a given date range.
        """
        expense_params = dto.GetExpenseParams(
            user_id, start_date, end_date, all_expenses, format_report
        )
        expenses = self.expenses_service.get_expenses(session, expense_params)
        if not expenses:
            logger.warning(
                f"Error during receipt of expenses. Arguments: {expense_params}"
            )
            raise HTTPException(404, ERROR_MESSAGES["read_error"])
        return self._send_report(format_report, expenses)

    def _send_report(self, format_report: str, expenses: List[Expense]):
        match format_report:
            case "json":

                return JSONResponse(
                    content=[
                        schema.ExpenseResponse.model_validate(e).model_dump(mode="json")
                        for e in expenses
                    ]
                )
            case "xlsx":
                excel_report = ExcelReport()
                expenses_report = excel_report.generate_report(expenses)

                headers = {
                    "Content-Disposition": "attachment; filename=expenses_report.xlsx"
                }
                return StreamingResponse(
                    content=expenses_report,
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers=headers,
                )

    def create_expense(
        self, user_id: int, expense_schema: schema.ExpenseCreate, session: Session
    ) -> Expense:
        """
        Create a new expense.
        """

        expense = self.expenses_service.create_expense(session, user_id, expense_schema)
        if not expense:
            logger.warning(
                f"Error during creation of an expense. Arguments: {expense_schema}"
            )
            raise HTTPException(
                422,
                ERROR_MESSAGES["create_error"],
            )
        return expense

    def update_expense(
        self, expense_id: int, expense_update: schema.ExpenseUpdate, session: Session
    ) -> Expense:
        """
        Update an expense.
        """
        result = self.expenses_service.update_expense(
            session, expense_id, expense_update
        )
        if not result:
            logger.warning(f"Error during update of expense by ID {expense_id}")
            raise HTTPException(
                422, ERROR_MESSAGES["update_error"].format(id=expense_id)
            )
        return self.expenses_service.get_expense_by_id(session, expense_id)

    def delete_expense(self, expense_id: int, session: Session):
        """
        Delete an expense.
        """
        result = self.expenses_service.delete_expense(session, expense_id)
        if not result:
            logger.warning(f"Error during delete of expense by ID {expense_id}")
            raise HTTPException(
                422, ERROR_MESSAGES["delete_error"].format(id=expense_id)
            )
