import os
import sys
import logging
from fastapi import FastAPI
from src.core.middleware.auth import AuthMiddleware
from src.core.exceptions.exception_handlers import register_exception_handlers
from src.api.api_factory import APIFactory


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
register_exception_handlers(app)
api_factory = APIFactory()
app.include_router(api_factory.get_main_router())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
