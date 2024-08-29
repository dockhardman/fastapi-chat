import json
from contextlib import asynccontextmanager
from typing import Any, Text

from app.config import logger, settings
from app.deps.oauth import UserPermissionChecker
from app.schemas.oauth import Permission
from app.utils.common import is_json_serializable, run_as_coro
from fastapi import Depends, FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""

    print(f"Application '{settings.app_name}' is starting up.")

    # <SET_APP_STATE>
    # <SET_DB>
    from app.db._base import DatabaseBase

    _db = DatabaseBase.from_url(settings.DB_URL)
    logger.info(f"Connected to database: {_db}")
    await run_as_coro(_db.touch)
    set_app_state(app, key="db", value=_db)
    # </SET_DB>
    # </SET_APP_STATE>

    yield

    print(f"Application '{settings.app_name}' is shutting down.")


def create_app():
    app = FastAPI(
        title=settings.app_name.title(), version=settings.app_version, lifespan=lifespan
    )

    @app.get("/")
    async def root():
        return "OK"

    @app.get("/health")
    async def health():
        return {"status": "OK"}

    @app.get(
        "/echo",
        dependencies=[
            Depends(
                UserPermissionChecker(
                    [Permission.MANAGE_ALL_RESOURCES], depends_type="platform_user"
                )
            )
        ],
    )
    async def echo(request: Request):
        body = await request.body()
        return {
            "url": str(request.url),
            "method": request.method,
            "client": request.client.host if request.client else "",
            "query_params": dict(request.query_params),
            "body": json.loads(body) if is_json_serializable(body) else "",
            "headers": dict(request.headers),
            "cookies": request.cookies,
        }

    from .api._router import router as api_router

    app.include_router(api_router)

    return app


def set_app_state(app: FastAPI, *, key: Text, value: Any):
    setattr(app.state, key, value)
    app.extra[key] = value


app = create_app()
