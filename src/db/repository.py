import logging
from typing import List, Optional, Union
from sqlalchemy import Delete, Select, Update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)


class CRUDRepository:

    @staticmethod
    def create(query: DeclarativeBase, session: Session) -> DeclarativeBase:
        """Creates a new entry in the database.

        Args:
            query (DeclarativeBase): An instance of a SQLAlchemy model
            session (Session): Session to perform the operation

        Returns:
            DeclarativeBase: Created model object
        """
        session.add(query)
        session.commit()
        session.refresh(query)
        return query

    @staticmethod
    def read(
        query: Select, session: Session, single: bool = False
    ) -> Union[Optional[DeclarativeBase], List[DeclarativeBase]]:
        """Executes a SELECT query to the database

        Args:
            query (Select): SQLAlchemy Select-query
            session (Session): Session to perform the operation
            single (bool, optional):  if True, returns a single object (or None), otherwise - a list. Defaults to False.

        Returns:
            Union[Optional[DeclarativeBase], List[DeclarativeBase]]: One model object (single=True) or List of objects (single=False).
        """
        result = session.execute(query)
        return result.scalars().first() if single else result.scalars().all()

    @staticmethod
    def update(query: Update, session: Session) -> bool:
        """Executes a UPDATE query to the database

        Args:
            query (Update): SQLAlchemy Update-query
            session (Session): Session to perform the operation

        Returns:
            bool: A Boolean value indicating whether changes have occurred in the database
        """
        result = session.execute(query)
        session.commit()
        return result.rowcount > 0

    @staticmethod
    def delete(query: Delete, session: Session) -> bool:
        """Executes a UPDATE query to the database

        Args:
            query (Delete): SQLAlchemy Delete-query
            session (Session): Session to perform the operation

        Returns:
            bool: A Boolean value indicating whether changes have occurred in the database
        """
        result = session.execute(query)
        session.commit()
        return result.rowcount > 0