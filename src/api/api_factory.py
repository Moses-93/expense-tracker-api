from fastapi import APIRouter
from src.api.expenses.expense_container import expense_container
from src.api.expenses.expenses_router import ExpenseRouter


class APIFactory:
    def __init__(self):
        self._router = APIRouter()
        self._register_expense_routes()

    def _register_expense_routes(self):
        router: ExpenseRouter = expense_container.resolve(ExpenseRouter)
        self._router.include_router(router.router)

    def get_main_router(self) -> APIRouter:
        return self._router
