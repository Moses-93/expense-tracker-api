from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response

from src.core.database import get_db
from src.services.user_service import UserService


class AuthMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request, call_next):
        chat_id = request.headers.get("X-Telegram-Chat-ID")

        if not chat_id:
            return Response({"error": "Missing Telegram Chat ID"}, status_code=400)
        
        for session in get_db():
            user = UserService.get_user_by_chat_id(chat_id, session)
            
            if not user:
                user = UserService.create_user(chat_id, session)
        
        request.state.user = user
        
        return await call_next(request)
