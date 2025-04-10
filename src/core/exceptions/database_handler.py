import logging
from functools import wraps
from inspect import signature
from typing import Callable, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    ProgrammingError,
    InvalidRequestError,
)
from . import database_exc

logger = logging.getLogger(__name__)

exceptions = {
    "create": database_exc.DBCreateError,
    "read": database_exc.DBReadError,
    "update": database_exc.DBUpdateError,
    "delete": database_exc.DBDeleteError,
}


def get_session_from_args(func: Callable, *args, **kwargs) -> Optional[Session]:
    bound = signature(func).bind(*args, **kwargs)
    bound.apply_defaults()
    return bound.arguments.get("session")


def handle_db_exceptions(operation: str):
    """Decorator for handling database errors in CRUD methods."""

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):

            session: Session = get_session_from_args(func, *args, **kwargs)
            if not session:
                raise RuntimeError("Session not found in arguments")

            try:
                return func(*args, **kwargs)
            except IntegrityError as e:
                session.rollback()
                logger.error(f"Integrity error during {operation}: {e}", exc_info=True)
                raise database_exc.DBIntegrityError(
                    f"Integrity error during {operation}: {e}"
                )
            except (OperationalError, ProgrammingError, InvalidRequestError) as e:
                session.rollback()
                logger.error(f"Database error during {operation}: {e}", exc_info=True)
                exc_class = exceptions.get(
                    operation.lower(), database_exc.DatabaseError
                )
                raise exc_class(f"Database error during {operation}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error during {operation}: {e}", exc_info=True)
                raise

        return wrapper

    return decorator
