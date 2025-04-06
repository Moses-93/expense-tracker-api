import os
import sys
import logging
from fastapi import FastAPI
from src.core.middleware.auth import AuthMiddleware
from src.api.expenses.expenses_router import ExpenseRouter
from src.api.expenses.expenses_handler import ExpenseHandler
from src.services.expense.expense_service import ExpenseService
from src.services.expense.expense_repository import ExpenseRepository
from src.services.expense.expense_manager import ExpenseManager


api_router = ExpenseRouter(
    expenses_handlers=ExpenseHandler(
        expenses_manager=ExpenseManager(
            expenses_service=ExpenseService(expenses_repository=ExpenseRepository())
        )
    )
).router

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

app = FastAPI()
app.add_middleware(AuthMiddleware)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
