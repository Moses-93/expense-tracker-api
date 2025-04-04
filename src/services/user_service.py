from fastapi import  HTTPException, Request, status
from src.db.repository import CRUDRepository
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.db.models import User
from typing import Optional




class UserService:

    @staticmethod
    def get_user_by_chat_id(chat_id: int, session: Session) -> User:
        """
        Get a user by their chat ID.
        """
        return CRUDRepository.read(
            select(User).filter_by(chat_id=chat_id), session, single=True
        )
    
    @staticmethod
    def create_user(chat_id: int, session: Session) -> User:
        """
        Create a new user.
        """
        user = User(chat_id=chat_id)
        CRUDRepository.create(user, session)
        return user


async def get_current_user(request: Request) -> Optional[User]:
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user