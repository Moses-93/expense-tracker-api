from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from src.core.exceptions import database_exc


EXCEPTION_CONFIG = {
    database_exc.DBIntegrityError: {
        "status_code": 400,
        "message": "Упс! Схоже, дані не зовсім вірні. Можливо, такий запис уже є в системі. Перевірте, будь ласка, і спробуйте ще раз.",
    },
    database_exc.DBCreateError: {
        "status_code": 500,
        "message": "На жаль, не вдалося зберегти дані. Ми вже працюємо над вирішенням проблеми. Будь ласка, спробуйте трохи пізніше.",
    },
    database_exc.DBReadError: {
        "status_code": 500,
        "message": "Не вдалося завантажити дані. Зачекайте трохи та повторіть спробу — ми обов'язково все виправимо!",
    },
    database_exc.DBUpdateError: {
        "status_code": 500,
        "message": "Ой! Щось пішло не так під час оновлення. Дайте нам трохи часу, і спробуйте знову.",
    },
    database_exc.DBDeleteError: {
        "status_code": 500,
        "message": "Не вийшло видалити дані. Не хвилюйтеся, ми в курсі проблеми та скоро її виправимо. Спробуйте пізніше!",
    },
}


def register_exception_handlers(app: FastAPI):
    for exc_class, config in EXCEPTION_CONFIG.items():

        @app.exception_handler(exc_class)
        async def handler(request: Request, exc, config=config):
            return JSONResponse(
                status_code=config["status_code"],
                content={"detail": config["message"]},
            )
