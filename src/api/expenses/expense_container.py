import punq
from src.services.exchange_rate_service import ExchangeRateService
from src.services.expense import expense_controller, expense_service, expense_repository
from . import expenses_handler, expenses_router

expense_container = punq.Container()

expense_container.register(expense_repository.ExpenseRepository)
expense_container.register(ExchangeRateService)
expense_container.register(expense_service.ExpenseService)
expense_container.register(expense_controller.ExpenseController)
expense_container.register(expenses_handler.ExpenseHandler)
expense_container.register(expenses_router.ExpenseRouter)
