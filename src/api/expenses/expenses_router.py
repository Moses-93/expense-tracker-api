from fastapi import APIRouter, status
from src.schemas.expense.schema import ExpenseResponse
from .expenses_handler import ExpenseHandler


class ExpenseRouter:
    def __init__(self, expenses_handlers: ExpenseHandler):
        self.router = APIRouter(prefix="/api/expenses", tags=["expenses"])
        self.register_handlers(expenses_handlers)

    def register_handlers(self, expenses_handlers: ExpenseHandler):
        self.router.add_api_route(
            path="/{expense_id}",
            endpoint=expenses_handlers.get_expense_by_id,
            response_model=ExpenseResponse,
            status_code=status.HTTP_200_OK,
            methods=["GET"],
            name="Get Expense",
        )
        self.router.add_api_route(
            path="/report/excel",
            endpoint=expenses_handlers.get_expenses_excel_report,
            methods=["GET"],
            name="Get Expenses Report",
        )
        self.router.add_api_route(
            path="/",
            endpoint=expenses_handlers.create_expense,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
            name="Create Expense",
        )
        self.router.add_api_route(
            path="/{expense_id}",
            endpoint=expenses_handlers.update_expense,
            status_code=status.HTTP_200_OK,
            methods=["PATCH"],
            name="Update Expense",
        )
        self.router.add_api_route(
            path="/{expense_id}",
            endpoint=expenses_handlers.delete_expense,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["DELETE"],
            name="Delete Expense",
        )
